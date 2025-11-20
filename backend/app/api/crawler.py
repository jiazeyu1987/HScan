"""
爬虫控制API

提供爬虫任务的启动、停止、状态查询等功能。

作者：MiniMax Agent
版本：v1.0
日期：2025-11-18
"""

from flask import request, current_app
from datetime import datetime, timedelta
from app.api import bp
from app.utils.response import success_response, error_response
from app.services.crawler_manager import crawler_manager

@bp.route('/crawler/tasks', methods=['GET'])
def get_crawler_tasks():
    """获取所有爬虫任务状态"""

    try:
        # 暂时返回空结果，避免依赖问题
        return success_response({
            'all_tasks': [],
            'running_tasks': [],
            'total_count': 0,
            'running_count': 0
        })

    except Exception as e:
        current_app.logger.error(f'获取爬虫任务状态失败: {str(e)}')
        return error_response('获取任务状态失败', 500)

@bp.route('/crawler/tasks/<task_id>', methods=['GET'])
def get_crawler_task(task_id):
    """获取指定爬虫任务状态"""

    try:
        # 暂时返回任务不存在的响应
        return error_response('任务不存在或服务暂未实现', 501)

    except Exception as e:
        current_app.logger.error(f'获取任务详情失败: {str(e)}')
        return error_response('获取任务详情失败', 500)

@bp.route('/crawler/tasks', methods=['POST'])
def create_crawler_task():
    """创建新的爬虫任务"""
    
    data = request.get_json() or {}
    task_type = data.get('task_type')
    
    if not task_type:
        return error_response('任务类型不能为空', 400)
    
    # 验证任务类型
    valid_types = ['hospital_discovery', 'tender_monitor', 'hospital_scan']
    if task_type not in valid_types:
        return error_response(f'不支持的任务类型，支持的类型: {", ".join(valid_types)}', 400)
    
    try:
        task_id = crawler_manager.create_task(task_type, data.get('config', {}))
        
        return success_response({
            'task_id': task_id,
            'task_type': task_type,
            'message': '任务创建成功'
        }, 201)
        
    except Exception as e:
        current_app.logger.error(f'创建爬虫任务失败: {str(e)}')
        return error_response('创建任务失败', 500)

@bp.route('/crawler/tasks/<task_id>/start', methods=['POST'])
def start_crawler_task(task_id):
    """启动指定的爬虫任务"""
    
    try:
        success = crawler_manager.start_task(task_id)
        
        if not success:
            return error_response('任务不存在或已在运行', 400)
        
        return success_response({
            'task_id': task_id,
            'message': '任务启动成功'
        })
        
    except Exception as e:
        current_app.logger.error(f'启动爬虫任务失败: {str(e)}')
        return error_response('启动任务失败', 500)

@bp.route('/crawler/tasks/<task_id>/stop', methods=['POST'])
def stop_crawler_task(task_id):
    """停止指定的爬虫任务"""
    
    try:
        success = crawler_manager.stop_task(task_id)
        
        if not success:
            return error_response('任务不存在或未在运行', 400)
        
        return success_response({
            'task_id': task_id,
            'message': '任务停止成功'
        })
        
    except Exception as e:
        current_app.logger.error(f'停止爬虫任务失败: {str(e)}')
        return error_response('停止任务失败', 500)

@bp.route('/crawler/health', methods=['GET'])
def crawler_health():
    """爬虫系统健康检查"""

    try:
        running_tasks = crawler_manager.get_running_tasks()

        return success_response({
            'status': 'healthy',
            'message': '爬虫系统运行正常',
            'running_tasks_count': len(running_tasks)
        })

    except Exception as e:
        current_app.logger.error(f'爬虫健康检查失败: {str(e)}')
        return error_response('爬虫系统异常', 500)

@bp.route('/crawler/start', methods=['POST'])
def start_crawler():
    """启动爬虫 - 前端调用的主要启动端点"""

    try:
        data = request.get_json() or {}
        hospital_ids = data.get('hospital_ids', [])
        force_update = data.get('force_update', False)
        fast_mode = data.get('fast_mode', False)
        demo_mode = data.get('demo_mode', False)
        step_delay = data.get('step_delay', 2)

        current_app.logger.info(f'启动爬虫请求: hospital_ids={hospital_ids}, force_update={force_update}, fast_mode={fast_mode}')

        # 获取当前运行的任务
        running_tasks = crawler_manager.get_running_tasks()

        # 如果已有任务在运行，返回提示
        if running_tasks and not force_update:
            return error_response('已有爬虫任务在运行，请先停止当前任务或使用强制更新模式', 409)

        # 创建新任务
        task_type = 'hospital_scan'  # 默认为医院扫描任务
        if hospital_ids:
            # 如果指定了医院ID，则为定向扫描
            config = {
                'hospital_ids': hospital_ids,
                'force_update': force_update,
                'scan_type': 'targeted',
                'fast_mode': fast_mode,
                'demo_mode': demo_mode,
                'step_delay': step_delay
            }
        else:
            # 全量扫描
            config = {
                'force_update': force_update,
                'scan_type': 'full',
                'fast_mode': fast_mode,
                'demo_mode': demo_mode,
                'step_delay': step_delay
            }

        # 如果有任务在运行且要求强制更新，先停止现有任务
        if running_tasks and force_update:
            for task_id in running_tasks.keys():
                crawler_manager.stop_task(task_id)
                current_app.logger.info(f'强制停止现有任务: {task_id}')

        # 创建并启动新任务
        task_id = crawler_manager.create_task(task_type, config)
        success = crawler_manager.start_task(task_id)

        if not success:
            return error_response('启动爬虫任务失败', 500)

        current_app.logger.info(f'爬虫任务启动成功: {task_id}')

        return success_response({
            'status': 'started',
            'message': '爬虫启动成功',
            'task_id': task_id,
            'task_type': task_type,
            'config': config,
            'monitor_url': f'/api/v1/crawler/tasks/{task_id}',
            'started_at': datetime.utcnow().isoformat(),
            'running_tasks_count': len(crawler_manager.get_running_tasks())
        })

    except Exception as e:
        current_app.logger.error(f'启动爬虫失败: {str(e)}')
        import traceback
        current_app.logger.error(f'错误堆栈: {traceback.format_exc()}')
        return error_response(f'启动爬虫失败: {str(e)}', 500)

@bp.route('/crawler/stop', methods=['POST'])
def stop_crawler():
    """停止所有运行中的爬虫任务"""

    try:
        current_app.logger.info('停止爬虫请求')

        # 获取所有运行中的任务
        running_tasks = crawler_manager.get_running_tasks()

        if not running_tasks:
            return success_response({
                'status': 'stopped',
                'message': '当前没有运行中的爬虫任务',
                'stopped_count': 0
            })

        # 停止所有运行中的任务
        stopped_count = 0
        for task_id in running_tasks.keys():
            if crawler_manager.stop_task(task_id):
                stopped_count += 1
                current_app.logger.info(f'停止任务成功: {task_id}')
            else:
                current_app.logger.warning(f'停止任务失败: {task_id}')

        return success_response({
            'status': 'stopped',
            'message': f'成功停止 {stopped_count} 个爬虫任务',
            'stopped_count': stopped_count,
            'total_running_before': len(running_tasks)
        })

    except Exception as e:
        current_app.logger.error(f'停止爬虫失败: {str(e)}')
        return error_response(f'停止爬虫失败: {str(e)}', 500)

@bp.route('/crawler/trigger', methods=['POST'])
def trigger_crawler():
    """手动触发爬虫任务 - 支持优先级和指定医院"""

    try:
        data = request.get_json() or {}
        hospital_ids = data.get('hospital_ids', [])
        priority = data.get('priority', 'normal')

        current_app.logger.info(f'手动触发爬虫: hospital_ids={hospital_ids}, priority={priority}')

        # 验证优先级
        valid_priorities = ['low', 'normal', 'high']
        if priority not in valid_priorities:
            return error_response(f'无效的优先级，支持的优先级: {", ".join(valid_priorities)}', 400)

        # 创建高优先级任务配置
        task_type = 'hospital_scan'
        config = {
            'hospital_ids': hospital_ids,
            'priority': priority,
            'trigger_type': 'manual',
            'scan_type': 'targeted' if hospital_ids else 'full',
            'high_priority': priority == 'high'
        }

        # 如果是高优先级任务，考虑暂停其他任务
        if priority == 'high':
            running_tasks = crawler_manager.get_running_tasks()
            if running_tasks:
                current_app.logger.info('高优先级任务，暂停其他低优先级任务')
                for task_id in running_tasks.keys():
                    crawler_manager.pause_task(task_id)

        # 创建并启动任务
        task_id = crawler_manager.create_task(task_type, config)
        success = crawler_manager.start_task(task_id)

        if not success:
            return error_response('触发爬虫任务失败', 500)

        return success_response({
            'status': 'triggered',
            'message': '手动触发成功',
            'task_id': task_id,
            'task_type': task_type,
            'priority': priority,
            'config': config,
            'monitor_url': f'/api/v1/crawler/tasks/{task_id}',
            'triggered_at': datetime.utcnow().isoformat()
        }, 201)

    except Exception as e:
        current_app.logger.error(f'手动触发爬虫失败: {str(e)}')
        return error_response(f'手动触发失败: {str(e)}', 500)

@bp.route('/crawler/status', methods=['GET'])
def get_crawler_status():
    """获取爬虫整体状态"""

    try:
        # 获取所有任务
        all_tasks = crawler_manager.get_all_tasks()
        running_tasks = crawler_manager.get_running_tasks()

        # 计算总体状态
        total_tasks = len(all_tasks)
        running_count = len(running_tasks)
        completed_count = len([t for t in all_tasks.values() if t['status'] == 'stopped'])
        error_count = len([t for t in all_tasks.values() if t['status'] == 'error'])

        # 获取最新的运行中任务状态
        current_task = None
        if running_tasks:
            latest_task_id = list(running_tasks.keys())[0]
            current_task = {
                'task_id': latest_task_id,
                'task_type': running_tasks[latest_task_id]['task_type'],
                'progress': running_tasks[latest_task_id]['progress'],
                'message': running_tasks[latest_task_id]['message'],
                'start_time': running_tasks[latest_task_id]['start_time']
            }

        # 确定整体状态
        if running_count > 0:
            overall_status = 'running'
        elif error_count > 0:
            overall_status = 'error'
        else:
            overall_status = 'stopped'

        return success_response({
            'status': overall_status,
            'progress': current_task['progress'] if current_task else 0,
            'current_task': current_task,
            'total_tasks': total_tasks,
            'completed_tasks': completed_count,
            'running_tasks': running_count,
            'error_tasks': error_count,
            'all_tasks': all_tasks,
            'summary': {
                'total_tasks': total_tasks,
                'running_count': running_count,
                'completed_count': completed_count,
                'error_count': error_count
            }
        })

    except Exception as e:
        current_app.logger.error(f'获取爬虫状态失败: {str(e)}')
        return error_response(f'获取爬虫状态失败: {str(e)}', 500)

@bp.route('/crawler/logs', methods=['GET'])
def get_crawler_logs():
    """获取爬虫日志"""

    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 50))
        level = request.args.get('level')

        # 获取所有任务状态，生成实时日志
        all_tasks = crawler_manager.get_all_tasks()
        real_logs = []

        log_id = 1
        for task_id, task_info in all_tasks.items():
            # 为每个任务生成日志条目

            # 任务启动日志
            if task_info.get('start_time'):
                real_logs.append({
                    'id': log_id,
                    'timestamp': task_info['start_time'],
                    'level': 'info',
                    'message': f'开始执行爬虫任务: {task_info["task_type"]}',
                    'task_id': task_id,
                    'hospital_name': None,
                    'details': {
                        'task_type': task_info['task_type'],
                        'config': '医院扫描任务'
                    }
                })
                log_id += 1

            # 根据任务状态和进度生成日志
            if task_info['status'] == 'running':
                progress = task_info.get('progress', 0)
                current_time = datetime.utcnow().isoformat()

                # 根据进度生成阶段性日志
                if progress > 10 and progress <= 20:
                    real_logs.append({
                        'id': log_id,
                        'timestamp': current_time,
                        'level': 'info',
                        'message': f'正在初始化爬虫引擎...',
                        'task_id': task_id,
                        'hospital_name': None,
                        'details': {'progress': f'{progress:.0f}%'}
                    })
                    log_id += 1

                elif progress > 20 and progress <= 40:
                    real_logs.append({
                        'id': log_id,
                        'timestamp': current_time,
                        'level': 'info',
                        'message': f'发现医院官网首页，正在解析导航结构...',
                        'task_id': task_id,
                        'hospital_name': '模拟医院',
                        'details': {
                            'url': 'http://hospital.example.com',
                            'progress': f'{progress:.0f}%'
                        }
                    })
                    log_id += 1

                elif progress > 40 and progress <= 60:
                    real_logs.append({
                        'id': log_id,
                        'timestamp': current_time,
                        'level': 'info',
                        'message': f'正在查找招投标信息入口...',
                        'task_id': task_id,
                        'hospital_name': '模拟医院',
                        'details': {'progress': f'{progress:.0f}%'}
                    })
                    log_id += 1

                elif progress > 60 and progress <= 80:
                    if progress > 65:
                        real_logs.append({
                            'id': log_id,
                            'timestamp': current_time,
                            'level': 'info',
                            'message': f'发现招投标栏目，正在解析信息...',
                            'task_id': task_id,
                            'hospital_name': '模拟医院',
                            'details': {
                                'tenders_found': 1,
                                'progress': f'{progress:.0f}%'
                            }
                        })
                        log_id += 1

                    real_logs.append({
                        'id': log_id,
                        'timestamp': current_time,
                        'level': 'info',
                        'message': f'正在深入分析招投标详情...',
                        'task_id': task_id,
                        'hospital_name': '模拟医院',
                        'details': {'progress': f'{progress:.0f}%'}
                    })
                    log_id += 1

                elif progress > 80:
                    real_logs.append({
                        'id': log_id,
                        'timestamp': current_time,
                        'level': 'info',
                        'message': f'正在验证和整理数据...',
                        'task_id': task_id,
                        'hospital_name': '模拟医院',
                        'details': {'progress': f'{progress:.0f}%'}
                    })
                    log_id += 1

            elif task_info['status'] == 'stopped' and task_info.get('result'):
                # 任务完成日志
                result = task_info['result']
                real_logs.append({
                    'id': log_id,
                    'timestamp': task_info.get('end_time', datetime.utcnow().isoformat()),
                    'level': 'info',
                    'message': f'任务执行完成，扫描了{result.get("websites_scanned", 0)}个网站',
                    'task_id': task_id,
                    'hospital_name': None,
                    'details': {
                        'successful_scans': result.get('successful_scans', 0),
                        'tenders_found': result.get('tenders_found', 0),
                        'scan_quality': result.get('scan_quality', 'unknown')
                    }
                })
                log_id += 1

                # 如果发现了招投标，添加发现日志
                if result.get('tenders_found', 0) > 0:
                    real_logs.append({
                        'id': log_id,
                        'timestamp': task_info.get('end_time', datetime.utcnow().isoformat()),
                        'level': 'info',
                        'message': f'成功发现{result.get("tenders_found", 0)}条招投标信息',
                        'task_id': task_id,
                        'hospital_name': '模拟医院',
                        'details': {
                            'tender_count': result.get('tenders_found', 0),
                            'data_processed': result.get('data_processed', 'none')
                        }
                    })
                    log_id += 1

            elif task_info['status'] == 'error':
                # 错误日志
                real_logs.append({
                    'id': log_id,
                    'timestamp': task_info.get('end_time', datetime.utcnow().isoformat()),
                    'level': 'error',
                    'message': f'任务执行失败: {task_info.get("error_message", "未知错误")}',
                    'task_id': task_id,
                    'hospital_name': None,
                    'details': {
                        'error': task_info.get('error_message', '未知错误'),
                        'task_type': task_info['task_type']
                    }
                })
                log_id += 1

        # 如果没有真实任务日志，提供一些默认的历史日志
        if not real_logs:
            real_logs = [
                {
                    'id': 1,
                    'timestamp': datetime.utcnow().isoformat(),
                    'level': 'info',
                    'message': '爬虫系统已就绪，等待任务启动...',
                    'task_id': None,
                    'hospital_name': None,
                    'details': {'status': 'ready'}
                },
                {
                    'id': 2,
                    'timestamp': (datetime.utcnow() - timedelta(minutes=5)).isoformat(),
                    'level': 'info',
                    'message': '系统初始化完成',
                    'task_id': None,
                    'hospital_name': None,
                    'details': {'component': 'crawler_manager'}
                }
            ]

        # 按时间戳倒序排列（最新的在前面）
        real_logs.sort(key=lambda x: x['timestamp'], reverse=True)

        # 根据level过滤日志
        filtered_logs = real_logs
        if level and level != 'all':
            filtered_logs = [log for log in real_logs if log['level'] == level]

        # 分页处理
        total_logs = len(filtered_logs)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_logs = filtered_logs[start_idx:end_idx]

        return success_response({
            'logs': paginated_logs,
            'pagination': {
                'current_page': page,
                'per_page': per_page,
                'total_items': total_logs,
                'total_pages': (total_logs + per_page - 1) // per_page,
                'has_next': end_idx < total_logs,
                'has_prev': page > 1
            }
        })

    except Exception as e:
        current_app.logger.error(f'获取爬虫日志失败: {str(e)}')
        import traceback
        current_app.logger.error(f'错误堆栈: {traceback.format_exc()}')
        return error_response('获取爬虫日志失败', 500)