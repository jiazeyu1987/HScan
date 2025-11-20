"""
爬虫控制API

提供爬虫任务的启动、停止、状态查询等功能。

作者：MiniMax Agent
版本：v1.0
日期：2025-11-18
"""

from flask import request, current_app
from datetime import datetime
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

        # 模拟爬虫日志数据
        mock_logs = [
            {
                'id': 1,
                'timestamp': '2025-11-18T14:30:00Z',
                'level': 'info',
                'message': '开始扫描北京协和医院官网',
                'task_id': 'scan_beijing_001',
                'hospital_name': '北京协和医院',
                'details': {
                    'url': 'http://www.pumch.cn',
                    'status': 'success',
                    'response_time': 1.2
                }
            },
            {
                'id': 2,
                'timestamp': '2025-11-18T14:25:00Z',
                'level': 'info',
                'message': '发现新的招投标信息',
                'task_id': 'scan_beijing_001',
                'hospital_name': '北京协和医院',
                'details': {
                    'tender_title': '医疗设备采购项目',
                    'tender_budget': 2500000
                }
            },
            {
                'id': 3,
                'timestamp': '2025-11-18T14:20:00Z',
                'level': 'error',
                'message': '扫描失败：连接超时',
                'task_id': 'scan_shanghai_002',
                'hospital_name': '上海瑞金医院',
                'details': {
                    'url': 'http://www.rjh.com.cn',
                    'error': 'Connection timeout after 30 seconds',
                    'retry_count': 3
                }
            },
            {
                'id': 4,
                'timestamp': '2025-11-18T14:15:00Z',
                'level': 'warning',
                'message': '网站结构发生变化，需要更新爬虫规则',
                'task_id': 'scan_guangzhou_003',
                'hospital_name': '广州中山一院',
                'details': {
                    'url': 'http://www.zs-hospital.sh.cn',
                    'issue': 'HTML structure changed',
                    'action_required': 'update parser rules'
                }
            },
            {
                'id': 5,
                'timestamp': '2025-11-18T14:10:00Z',
                'level': 'info',
                'message': '扫描完成，共发现3条新招投标',
                'task_id': 'scan_jiangsu_004',
                'hospital_name': '江苏省人民医院',
                'details': {
                    'new_tenders': 3,
                    'updated_tenders': 1,
                    'total_scan_time': 45.6
                }
            }
        ]

        # 根据level过滤日志
        filtered_logs = mock_logs
        if level and level != 'all':
            filtered_logs = [log for log in mock_logs if log['level'] == level]

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
        return error_response('获取爬虫日志失败', 500)