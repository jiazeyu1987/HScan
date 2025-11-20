"""
统计数据API

提供系统的统计数据分析功能，包括医院信息、招投标数据、扫描统计等。

作者：MiniMax Agent
版本：v1.0
日期：2025-11-18
"""

from flask import request
from app.api import bp
from app.utils.response import success_response, error_response

@bp.route('/statistics', methods=['GET'])
def get_statistics():
    """获取系统统计数据"""

    try:
        # 模拟统计数据，实际应从数据库获取
        statistics = {
            'total_hospitals': 1250,
            'verified_hospitals': 890,
            'active_hospitals': 750,
            'total_tenders': 3456,
            'weekly_new_tenders': 45,
            'monthly_new_tenders': 180,
            'scan_success_rate': 87.5,
            'total_budget': 250000000,  # 2.5亿

            # 趋势数据
            'trend_data': {
                'daily': [
                    {'date': '2025-11-13', 'hospitals': 1200, 'tenders': 30},
                    {'date': '2025-11-14', 'hospitals': 1210, 'tenders': 35},
                    {'date': '2025-11-15', 'hospitals': 1220, 'tenders': 28},
                    {'date': '2025-11-16', 'hospitals': 1230, 'tenders': 42},
                    {'date': '2025-11-17', 'hospitals': 1240, 'tenders': 38},
                    {'date': '2025-11-18', 'hospitals': 1250, 'tenders': 45},
                ],
                'weekly': [
                    {'week': '2025-W45', 'hospitals': 1150, 'tenders': 180},
                    {'week': '2025-W46', 'hospitals': 1200, 'tenders': 220},
                    {'week': '2025-W47', 'hospitals': 1250, 'tenders': 195},
                ],
                'monthly': [
                    {'month': '2025-09', 'hospitals': 900, 'tenders': 650},
                    {'month': '2025-10', 'hospitals': 1100, 'tenders': 780},
                    {'month': '2025-11', 'hospitals': 1250, 'tenders': 820},
                ]
            },

            # 地区分布
            'region_distribution': [
                {'region': '北京市', 'hospital_count': 45, 'tender_count': 120},
                {'region': '上海市', 'hospital_count': 38, 'tender_count': 95},
                {'region': '广东省', 'hospital_count': 156, 'tender_count': 280},
                {'region': '江苏省', 'hospital_count': 142, 'tender_count': 210},
                {'region': '浙江省', 'hospital_count': 98, 'tender_count': 165},
            ],

            # 医院等级分布
            'hospital_levels': {
                '三甲医院': 320,
                '三乙医院': 280,
                '二甲医院': 410,
                '二乙医院': 180,
                '其他': 60
            }
        }

        return success_response(statistics)

    except Exception as e:
        return error_response('获取统计数据失败', 500)

@bp.route('/statistics/trend', methods=['GET'])
def get_trend_data():
    """获取趋势数据"""

    try:
        # 获取查询参数
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        granularity = request.args.get('granularity', 'daily')

        # 验证粒度参数
        if granularity not in ['daily', 'weekly', 'monthly']:
            granularity = 'daily'

        # 模拟趋势数据，实际应根据参数从数据库查询
        trend_data = {
            'granularity': granularity,
            'data': []
        }

        if granularity == 'daily':
            trend_data['data'] = [
                {'date': '2025-11-13', 'hospitals': 1200, 'tenders': 30, 'scans': 850},
                {'date': '2025-11-14', 'hospitals': 1210, 'tenders': 35, 'scans': 880},
                {'date': '2025-11-15', 'hospitals': 1220, 'tenders': 28, 'scans': 820},
                {'date': '2025-11-16', 'hospitals': 1230, 'tenders': 42, 'scans': 920},
                {'date': '2025-11-17', 'hospitals': 1240, 'tenders': 38, 'scans': 890},
                {'date': '2025-11-18', 'hospitals': 1250, 'tenders': 45, 'scans': 950},
            ]
        elif granularity == 'weekly':
            trend_data['data'] = [
                {'week': '2025-W45', 'hospitals': 1150, 'tenders': 180, 'scans': 4200},
                {'week': '2025-W46', 'hospitals': 1200, 'tenders': 220, 'scans': 4800},
                {'week': '2025-W47', 'hospitals': 1250, 'tenders': 195, 'scans': 4500},
            ]
        else:  # monthly
            trend_data['data'] = [
                {'month': '2025-09', 'hospitals': 900, 'tenders': 650, 'scans': 16000},
                {'month': '2025-10', 'hospitals': 1100, 'tenders': 780, 'scans': 18500},
                {'month': '2025-11', 'hospitals': 1250, 'tenders': 820, 'scans': 19800},
            ]

        return success_response(trend_data)

    except Exception as e:
        return error_response('获取趋势数据失败', 500)

@bp.route('/statistics/dashboard', methods=['GET'])
def get_dashboard_data():
    """获取仪表板数据"""

    try:
        # 仪表板需要的关键数据
        dashboard_data = {
            # 概览数据
            'overview': {
                'total_hospitals': 1250,
                'total_tenders': 3456,
                'active_scans': 45,
                'success_rate': 87.5
            },

            # 今日数据
            'today': {
                'new_hospitals': 10,
                'new_tenders': 12,
                'completed_scans': 156,
                'failed_scans': 22
            },

            # 最近扫描历史
            'recent_scans': [
                {'hospital_name': '北京协和医院', 'scan_time': '2025-11-18 14:30:00', 'status': 'success', 'new_tenders': 3},
                {'hospital_name': '上海瑞金医院', 'scan_time': '2025-11-18 14:25:00', 'status': 'success', 'new_tenders': 1},
                {'hospital_name': '广州中山一院', 'scan_time': '2025-11-18 14:20:00', 'status': 'failed', 'new_tenders': 0},
                {'hospital_name': '江苏人民医院', 'scan_time': '2025-11-18 14:15:00', 'status': 'success', 'new_tenders': 2},
                {'hospital_name': '浙大一院', 'scan_time': '2025-11-18 14:10:00', 'status': 'success', 'new_tenders': 4},
            ],

            # 最新招投标信息
            'latest_tenders': [
                {
                    'hospital_name': '北京协和医院',
                    'title': '医疗设备采购项目',
                    'budget': 2500000,
                    'publish_date': '2025-11-18',
                    'deadline': '2025-12-05'
                },
                {
                    'hospital_name': '上海瑞金医院',
                    'title': '信息化建设招标',
                    'budget': 1800000,
                    'publish_date': '2025-11-18',
                    'deadline': '2025-12-03'
                },
                {
                    'hospital_name': '广州中山一院',
                    'title': '药品集中采购',
                    'budget': 5200000,
                    'publish_date': '2025-11-17',
                    'deadline': '2025-12-10'
                }
            ],

            # 扫描进度
            'scan_progress': {
                'total': 1250,
                'completed': 1080,
                'in_progress': 45,
                'failed': 125
            }
        }

        return success_response(dashboard_data)

    except Exception as e:
        return error_response('获取仪表板数据失败', 500)