import React, { useState, useEffect } from 'react'
import {
  Card,
  Row,
  Col,
  Select,
  DatePicker,
  Button,
  Table,
  Typography,
  Space,
  Statistic,
  Progress,
  Tag,
  Tooltip,
  Divider
} from 'antd'
import {
  BarChartOutlined,
  LineChartOutlined,
  PieChartOutlined,
  ReloadOutlined,
  ArrowUpOutlined,
  ArrowDownOutlined,
  ExportOutlined
} from '@ant-design/icons'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip as RechartsTooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area
} from 'recharts'

// Store
import { useStatisticsStore } from '../store'

const { Title, Text } = Typography
const { RangePicker } = DatePicker
const { Option } = Select

interface ChartData {
  name: string
  value: number
  [key: string]: any
}

// 模拟数据 - 用于演示
const mockTrendData = [
  { date: '2024-11-01', tenders: 85, success_rate: 88.5, budget: 1250 },
  { date: '2024-11-02', tenders: 92, success_rate: 91.2, budget: 1480 },
  { date: '2024-11-03', tenders: 78, success_rate: 86.8, budget: 1120 },
  { date: '2024-11-04', tenders: 105, success_rate: 92.1, budget: 1650 },
  { date: '2024-11-05', tenders: 88, success_rate: 89.3, budget: 1320 },
  { date: '2024-11-06', tenders: 95, success_rate: 90.7, budget: 1420 },
  { date: '2024-11-07', tenders: 110, success_rate: 93.4, budget: 1780 }
]

const mockHospitalTypeData = [
  { name: '公立医院', value: 580, color: '#1890ff' },
  { name: '私立医院', value: 420, color: '#52c41a' },
  { name: '社区卫生', value: 280, color: '#722ed1' },
  { name: '专科医院', value: 120, color: '#faad14' }
]

const mockTenderTypeData = [
  { name: '医疗设备', value: 856 },
  { name: '药品采购', value: 642 },
  { name: '工程建设', value: 428 },
  { name: 'IT服务', value: 312 },
  { name: '咨询服务', value: 107 }
]

const mockRegionData = [
  {
    region: '北京',
    hospitals: 156,
    tenders: 423,
    budget: 285600,
    success_rate: 92.5
  },
  {
    region: '上海',
    hospitals: 142,
    tenders: 398,
    budget: 267800,
    success_rate: 90.8
  },
  {
    region: '广东',
    hospitals: 198,
    tenders: 567,
    budget: 342100,
    success_rate: 89.2
  },
  {
    region: '江苏',
    hospitals: 134,
    tenders: 334,
    budget: 198600,
    success_rate: 88.7
  },
  {
    region: '浙江',
    hospitals: 128,
    tenders: 312,
    budget: 186400,
    success_rate: 91.3
  }
]

const StatisticsPage: React.FC = () => {
  const { statistics, loading, fetchStatistics } = useStatisticsStore()
  const [dateRange, setDateRange] = useState<[any, any] | null>(null)
  const [granularity, setGranularity] = useState<string>('daily')

  useEffect(() => {
    loadData()
  }, [])

  const loadData = async () => {
    try {
      await fetchStatistics()
    } catch (error) {
      console.error('加载统计数据失败:', error)
    }
  }

  const regionColumns = [
    {
      title: '地区',
      dataIndex: 'region',
      key: 'region'
    },
    {
      title: '医院数量',
      dataIndex: 'hospitals',
      key: 'hospitals'
    },
    {
      title: '招投标数量',
      dataIndex: 'tenders',
      key: 'tenders'
    },
    {
      title: '预算总额(万元)',
      dataIndex: 'budget',
      key: 'budget',
      render: (value: number) => `${(value / 10000).toLocaleString()}`
    },
    {
      title: '成功率',
      dataIndex: 'success_rate',
      key: 'success_rate',
      render: (rate: number) => (
        <div>
          <Progress percent={rate} size="small" />
          <span className="text-xs text-gray-500">{rate}%</span>
        </div>
      )
    }
  ]

  const handleExport = () => {
    // 这里应该实现导出功能
    console.log('导出统计数据')
  }

  return (
    <div className="space-y-6">
      {/* 页面标题 */}
      <div className="flex items-center justify-between">
        <div>
          <Title level={2} className="mb-2">数据统计</Title>
          <Text type="secondary">
            全面分析系统运行数据和趋势
          </Text>
        </div>
        <Space>
          <Button
            icon={<ReloadOutlined />}
            onClick={loadData}
            loading={loading}
          >
            刷新
          </Button>
          <Button
            icon={<ExportOutlined />}
            onClick={handleExport}
          >
            导出报告
          </Button>
        </Space>
      </div>

      {/* 筛选控件 */}
      <Card>
        <Row gutter={[16, 16]} align="middle">
          <Col xs={24} sm={8}>
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-500">时间范围:</span>
              <RangePicker
                value={dateRange}
                onChange={setDateRange}
                format="YYYY-MM-DD"
                style={{ flex: 1 }}
              />
            </div>
          </Col>
          <Col xs={24} sm={6}>
            <div className="flex items-center space-x-2">
              <span className="text-sm text-gray-500">粒度:</span>
              <Select
                value={granularity}
                onChange={setGranularity}
                style={{ width: '100%' }}
              >
                <Option value="daily">按天</Option>
                <Option value="weekly">按周</Option>
                <Option value="monthly">按月</Option>
              </Select>
            </div>
          </Col>
        </Row>
      </Card>

      {/* 关键指标 */}
      <Row gutter={[16, 16]}>
        <Col xs={24} sm={6}>
          <Card>
            <Statistic
              title="总医院数"
              value={1400}
              prefix={<BarChartOutlined />}
              valueStyle={{ color: '#1890ff' }}
              formatter={(value) => (
                <span>
                  {value}家
                  <Tooltip title="相比上周">
                    <span className="text-sm ml-2">
                      <ArrowUpOutlined style={{ color: '#52c41a' }} /> +2.5%
                    </span>
                  </Tooltip>
                </span>
              )}
            />
          </Card>
        </Col>
        <Col xs={24} sm={6}>
          <Card>
            <Statistic
              title="本月招投标"
              value={2345}
              prefix={<LineChartOutlined />}
              valueStyle={{ color: '#52c41a' }}
              formatter={(value) => (
                <span>
                  {value}条
                  <Tooltip title="相比上月">
                    <span className="text-sm ml-2">
                      <ArrowUpOutlined style={{ color: '#52c41a' }} /> +15.2%
                    </span>
                  </Tooltip>
                </span>
              )}
            />
          </Card>
        </Col>
        <Col xs={24} sm={6}>
          <Card>
            <Statistic
              title="总预算金额"
              value={12.5}
              prefix={<PieChartOutlined />}
              precision={1}
              valueStyle={{ color: '#722ed1' }}
              formatter={(value) => (
                <span>
                  {value}亿元
                  <Tooltip title="相比上周">
                    <span className="text-sm ml-2">
                      <ArrowUpOutlined style={{ color: '#52c41a' }} /> +8.7%
                    </span>
                  </Tooltip>
                </span>
              )}
            />
          </Card>
        </Col>
        <Col xs={24} sm={6}>
          <Card>
            <Statistic
              title="平均成功率"
              value={89.2}
              prefix={<BarChartOutlined />}
              precision={1}
              valueStyle={{ color: '#faad14' }}
              formatter={(value) => (
                <span>
                  {value}%
                  <Tooltip title="相比上周">
                    <span className="text-sm ml-2">
                      <ArrowUpOutlined style={{ color: '#52c41a' }} /> +1.2%
                    </span>
                  </Tooltip>
                </span>
              )}
            />
          </Card>
        </Col>
      </Row>

      {/* 趋势图表 */}
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={16}>
          <Card title="招投标趋势分析" extra={
            <Space>
              <Button size="small" type="link">近7天</Button>
              <Button size="small" type="link">近30天</Button>
            </Space>
          }>
            <div style={{ width: '100%', height: 300 }}>
              <ResponsiveContainer>
                <LineChart data={mockTrendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis yAxisId="left" />
                  <YAxis yAxisId="right" orientation="right" />
                  <RechartsTooltip />
                  <Legend />
                  <Line
                    yAxisId="left"
                    type="monotone"
                    dataKey="tenders"
                    stroke="#1890ff"
                    strokeWidth={2}
                    name="招投标数量"
                  />
                  <Line
                    yAxisId="right"
                    type="monotone"
                    dataKey="success_rate"
                    stroke="#52c41a"
                    strokeWidth={2}
                    name="成功率(%)"
                  />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </Col>

        <Col xs={24} lg={8}>
          <Card title="预算金额分布">
            <div style={{ width: '100%', height: 300 }}>
              <ResponsiveContainer>
                <AreaChart data={mockTrendData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <RechartsTooltip />
                  <Area
                    type="monotone"
                    dataKey="budget"
                    stroke="#722ed1"
                    fill="#722ed1"
                    fillOpacity={0.3}
                    name="预算金额(万元)"
                  />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </Col>
      </Row>

      {/* 分类统计 */}
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <Card title="医院类型分布">
            <div style={{ width: '100%', height: 300 }}>
              <ResponsiveContainer>
                <PieChart>
                  <Pie
                    data={mockHospitalTypeData}
                    cx="50%"
                    cy="50%"
                    innerRadius={60}
                    outerRadius={100}
                    paddingAngle={5}
                    dataKey="value"
                  >
                    {mockHospitalTypeData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={entry.color} />
                    ))}
                  </Pie>
                  <RechartsTooltip />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </Col>

        <Col xs={24} lg={12}>
          <Card title="招投标类型分布">
            <div style={{ width: '100%', height: 300 }}>
              <ResponsiveContainer>
                <BarChart data={mockTenderTypeData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <RechartsTooltip />
                  <Bar dataKey="value" fill="#1890ff" />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </Card>
        </Col>
      </Row>

      {/* 地区统计 */}
      <Card title="地区统计排名">
        <Table
          columns={regionColumns}
          dataSource={mockRegionData}
          rowKey="region"
          pagination={{
            pageSize: 10,
            showSizeChanger: true,
            showQuickJumper: true,
            showTotal: (total, range) => `第 ${range[0]}-${range[1]} 条，共 ${total} 条`
          }}
          size="small"
        />
      </Card>

      {/* 详细分析 */}
      <Row gutter={[16, 16]}>
        <Col xs={24} lg={12}>
          <Card title="成功率分析">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <Text>整体成功率</Text>
                <Text strong>89.2%</Text>
              </div>
              <Progress percent={89.2} strokeColor="#52c41a" />
              
              <div className="flex items-center justify-between">
                <Text>本周成功率</Text>
                <Text strong>91.5%</Text>
              </div>
              <Progress percent={91.5} strokeColor="#52c41a" />
              
              <div className="flex items-center justify-between">
                <Text>本月成功率</Text>
                <Text strong>88.7%</Text>
              </div>
              <Progress percent={88.7} strokeColor="#faad14" />

              <Divider />

              <div className="text-sm text-gray-600">
                <p>• 公立医院成功率最高：94.2%</p>
                <p>• 私立医院成功率：86.8%</p>
                <p>• 社区卫生成功率：91.3%</p>
                <p>• 专科医院成功率：83.5%</p>
              </div>
            </div>
          </Card>
        </Col>

        <Col xs={24} lg={12}>
          <Card title="性能指标">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <Text>平均响应时间</Text>
                <Text strong>1.2秒</Text>
              </div>
              <Progress percent={85} strokeColor="#1890ff" />
              
              <div className="flex items-center justify-between">
                <Text>系统负载</Text>
                <Text strong>65%</Text>
              </div>
              <Progress percent={65} strokeColor="#52c41a" />
              
              <div className="flex items-center justify-between">
                <Text>并发处理能力</Text>
                <Text strong>85%</Text>
              </div>
              <Progress percent={85} strokeColor="#722ed1" />

              <Divider />

              <div className="text-sm text-gray-600">
                <p>• 数据更新频率：每15分钟</p>
                <p>• API响应时间：平均1.2秒</p>
                <p>• 系统可用性：99.9%</p>
                <p>• 错误率：0.3%</p>
              </div>
            </div>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default StatisticsPage