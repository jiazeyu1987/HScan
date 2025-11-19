"""
爬虫控制API

提供爬虫任务的启动、停止、状态查询等功能。

作者：MiniMax Agent
版本：v1.0
日期：2025-11-18
"""

from flask import request, current_app
from app.api import bp
from app.utils.response import success_response, error_response
# from app.services.crawler_manager import crawler_manager  # 暂时注释，避免导入问题

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

@bp.route('/crawler/status', methods=['GET'])
def get_crawler_status():
    """获取爬虫整体状态"""

    from flask import jsonify
    try:
        # 简化版本，返回基本状态信息
        # TODO: 集成实际的爬虫管理器后更新此接口

        return jsonify({
            'success': True,
            'data': {
                'status': 'stopped',
                'progress': 0,
                'current_task': None,
                'total_tasks': 0,
                'completed_tasks': 0
            },
            'message': '获取成功'
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': '获取爬虫状态失败'
        }), 500

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