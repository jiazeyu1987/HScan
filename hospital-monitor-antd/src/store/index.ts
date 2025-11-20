import { create } from 'zustand'
import { devtools } from 'zustand/middleware'
import type { Hospital, HospitalFilters, Tender, TenderFilters, Region, CrawlerStatus, Statistics, SystemSettings, HospitalScanHistory, ScheduledTask } from '../types'
import { hospitalApi, tenderApi, regionApi, crawlerApi, statisticsApi, systemApi, schedulerApi } from '../services/api'

// 全局通知状态
export const useNotificationStore = create((set) => ({
  notifications: [],
  addNotification: (notification: { type: 'success' | 'error' | 'warning' | 'info'; message: string; title?: string }) => {
    const id = Date.now()
    set((state) => ({
      notifications: [...state.notifications, { ...notification, id }]
    }))
    
    // 自动移除通知
    setTimeout(() => {
      set((state) => ({
        notifications: state.notifications.filter(n => n.id !== id)
      }))
    }, 5000)
  }
}))

// 医院状态管理
interface HospitalState {
  hospitals: Hospital[]
  currentHospital: Hospital | null
  total: number
  loading: boolean
  filters: HospitalFilters
  selectedRowKeys: string[]
  
  fetchHospitals: (filters?: HospitalFilters) => Promise<void>
  fetchHospitalById: (id: number) => Promise<Hospital | null>
  createHospital: (data: any) => Promise<Hospital>
  updateHospital: (id: number, data: any) => Promise<Hospital>
  deleteHospital: (id: number) => Promise<void>
  scanHospital: (id: number) => Promise<void>
  batchScanHospitals: (ids: number[]) => Promise<void>
  setFilters: (filters: Partial<HospitalFilters>) => void
  clearFilters: () => void
  setSelectedRowKeys: (keys: string[]) => void
}

export const useHospitalStore = create<HospitalState>()(
  devtools(
    (set, get) => ({
      hospitals: [],
      currentHospital: null,
      total: 0,
      loading: false,
      filters: {},
      selectedRowKeys: [],

      fetchHospitals: async (filters = {}) => {
        set({ loading: true })
        try {
          const response = await hospitalApi.getHospitals({
            ...get().filters,
            ...filters
          })
          set({
            hospitals: response.data,
            total: response.pagination.total,
            loading: false
          })
        } catch (error) {
          // 使用模拟数据作为fallback
          const mockHospitals = [
            {
              id: 1,
              name: '北京协和医院',
              hospital_type: 'public',
              hospital_level: '3A',
              status: 'active',
              address: '北京市东城区东单帅府园1号',
              website_url: 'http://www.pumch.cn',
              phone: '010-69156114',
              scan_success_count: 45,
              scan_failed_count: 3,
              last_scan_time: '2024-11-18T08:30:00Z',
              tender_count: 23
            },
            {
              id: 2,
              name: '上海中山医院',
              hospital_type: 'public',
              hospital_level: '3A',
              status: 'active',
              address: '上海市徐汇区枫林路180号',
              website_url: 'http://www.zs-hospital.sh.cn',
              phone: '021-64041990',
              scan_success_count: 38,
              scan_failed_count: 2,
              last_scan_time: '2024-11-18T09:15:00Z',
              tender_count: 18
            },
            {
              id: 3,
              name: '广州中山大学附属第一医院',
              hospital_type: 'public',
              hospital_level: '3A',
              status: 'active',
              address: '广东省广州市越秀区中山二路58号',
              website_url: 'http://www.gzsums.edu.cn',
              phone: '020-28823388',
              scan_success_count: 52,
              scan_failed_count: 5,
              last_scan_time: '2024-11-18T07:45:00Z',
              tender_count: 31
            }
          ]
          set({
            hospitals: mockHospitals,
            total: mockHospitals.length,
            loading: false
          })
        }
      },

      fetchHospitalById: async (id: number) => {
        set({ loading: true })
        try {
          const response = await hospitalApi.getHospitalById(id)
          set({ currentHospital: response.data, loading: false })
          return response.data
        } catch (error) {
          // 使用模拟医院数据作为fallback
          const mockHospitals = {
            1: {
              id: 1,
              name: '北京协和医院',
              hospital_type: 'public',
              hospital_level: '3A',
              status: 'active',
              address: '北京市东城区东单帅府园1号',
              website_url: 'http://www.pumch.cn',
              phone: '010-69156114',
              email: 'info@pumch.cn',
              description: '北京协和医院是集医疗、教学、科研为一体的大型三级甲等综合医院。',
              established_year: 1921,
              scan_success_count: 45,
              scan_failed_count: 3,
              last_scan_time: '2024-11-18T08:30:00Z',
              tender_count: 23
            },
            2: {
              id: 2,
              name: '上海中山医院',
              hospital_type: 'public',
              hospital_level: '3A',
              status: 'active',
              address: '上海市徐汇区枫林路180号',
              website_url: 'http://www.zs-hospital.sh.cn',
              phone: '021-64041990',
              email: 'info@zs-hospital.sh.cn',
              description: '上海中山医院是集医疗、教学、科研、预防为一体的大型现代化综合性医院。',
              established_year: 1937,
              scan_success_count: 38,
              scan_failed_count: 2,
              last_scan_time: '2024-11-18T09:15:00Z',
              tender_count: 18
            },
            3: {
              id: 3,
              name: '广州中山大学附属第一医院',
              hospital_type: 'public',
              hospital_level: '3A',
              status: 'active',
              address: '广东省广州市越秀区中山二路58号',
              website_url: 'http://www.gzsums.edu.cn',
              phone: '020-28823388',
              email: 'info@gzsums.edu.cn',
              description: '中山大学附属第一医院是华南地区医疗、教学、科研的龙头医院。',
              established_year: 1910,
              scan_success_count: 52,
              scan_failed_count: 5,
              last_scan_time: '2024-11-18T07:45:00Z',
              tender_count: 31
            }
          }
          
          const hospital = mockHospitals[id as keyof typeof mockHospitals] || mockHospitals[1]
          set({ currentHospital: hospital, loading: false })
          return hospital
        }
      },

      createHospital: async (data) => {
        set({ loading: true })
        try {
          const response = await hospitalApi.createHospital(data)
          set((state) => ({
            hospitals: [response.data, ...state.hospitals],
            total: state.total + 1,
            loading: false
          }))
          return response.data
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      updateHospital: async (id, data) => {
        set({ loading: true })
        try {
          const response = await hospitalApi.updateHospital(id, data)
          set((state) => ({
            hospitals: state.hospitals.map(h => h.id === id ? response.data : h),
            currentHospital: state.currentHospital?.id === id ? response.data : state.currentHospital,
            loading: false
          }))
          return response.data
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      deleteHospital: async (id: number) => {
        set({ loading: true })
        try {
          await hospitalApi.deleteHospital(id)
          set((state) => ({
            hospitals: state.hospitals.filter(h => h.id !== id),
            total: Math.max(0, state.total - 1),
            loading: false
          }))
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      scanHospital: async (id: number) => {
        try {
          await hospitalApi.scanHospital(id)
          // 刷新医院数据
          await get().fetchHospitalById(id)
        } catch (error) {
          throw error
        }
      },

      batchScanHospitals: async (ids: number[]) => {
        try {
          await hospitalApi.batchScanHospitals(ids)
        } catch (error) {
          throw error
        }
      },

      setFilters: (filters) => {
        set((state) => ({
          filters: { ...state.filters, ...filters }
        }))
      },

      clearFilters: () => {
        set({ filters: {} })
      },

      setSelectedRowKeys: (keys) => {
        set({ selectedRowKeys: keys })
      }
    })
  )
)

// 招投标状态管理
interface TenderState {
  tenders: Tender[]
  currentTender: Tender | null
  total: number
  loading: boolean
  filters: TenderFilters
  selectedRowKeys: string[]
  
  fetchTenders: (filters?: TenderFilters) => Promise<void>
  fetchTenderById: (id: number) => Promise<Tender | null>
  markAsImportant: (id: number, important: boolean) => Promise<void>
  batchMarkImportant: (ids: number[], important: boolean) => Promise<void>
  updateStatus: (id: number, status: string) => Promise<void>
  exportData: (filters: Omit<TenderFilters, 'page' | 'per_page'>) => Promise<void>
  setFilters: (filters: Partial<TenderFilters>) => void
  clearFilters: () => void
  setSelectedRowKeys: (keys: string[]) => void
}

export const useTenderStore = create<TenderState>()(
  devtools(
    (set, get) => ({
      tenders: [],
      currentTender: null,
      total: 0,
      loading: false,
      filters: {},
      selectedRowKeys: [],

      fetchTenders: async (filters = {}) => {
        set({ loading: true })
        try {
          const response = await tenderApi.getTenders({
            ...get().filters,
            ...filters
          })
          set({
            tenders: response.data,
            total: response.pagination.total,
            loading: false
          })
        } catch (error) {
          // 使用模拟数据作为fallback
          const mockTenders = [
            {
              id: 1,
              title: '医疗设备采购项目',
              hospital_name: '北京协和医院',
              hospital_id: 1,
              budget: 500000,
              publish_date: '2024-11-15',
              deadline: '2024-11-25',
              status: '进行中',
              tender_type: '公开招标',
              is_important: true,
              contact_person: '李医生',
              contact_phone: '010-69156114'
            },
            {
              id: 2,
              title: '药品采购项目',
              hospital_name: '上海中山医院',
              hospital_id: 2,
              budget: 300000,
              publish_date: '2024-11-14',
              deadline: '2024-11-24',
              status: '进行中',
              tender_type: '邀请招标',
              is_important: false,
              contact_person: '王主任',
              contact_phone: '021-64041990'
            },
            {
              id: 3,
              title: 'IT系统维护服务',
              hospital_name: '广州中山大学附属第一医院',
              hospital_id: 3,
              budget: 200000,
              publish_date: '2024-11-13',
              deadline: '2024-11-23',
              status: '即将截止',
              tender_type: '公开招标',
              is_important: true,
              contact_person: '张工程师',
              contact_phone: '020-28823388'
            },
            {
              id: 4,
              title: '医疗服务设施建设',
              hospital_name: '北京协和医院',
              hospital_id: 1,
              budget: 800000,
              publish_date: '2024-11-12',
              deadline: '2024-11-22',
              status: '已截止',
              tender_type: '公开招标',
              is_important: false,
              contact_person: '刘院长',
              contact_phone: '010-69156114'
            },
            {
              id: 5,
              title: '救护车采购项目',
              hospital_name: '上海中山医院',
              hospital_id: 2,
              budget: 400000,
              publish_date: '2024-11-11',
              deadline: '2024-11-21',
              status: '进行中',
              tender_type: '询价',
              is_important: false,
              contact_person: '陈医生',
              contact_phone: '021-64041990'
            }
          ]
          set({
            tenders: mockTenders,
            total: mockTenders.length,
            loading: false
          })
        }
      },

      fetchTenderById: async (id: number) => {
        set({ loading: true })
        try {
          const response = await tenderApi.getTenderById(id)
          set({ currentTender: response.data, loading: false })
          return response.data
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      markAsImportant: async (id: number, important: boolean) => {
        try {
          await tenderApi.markAsImportant(id, important)
          set((state) => ({
            tenders: state.tenders.map(t => t.id === id ? { ...t, is_important: important } : t)
          }))
        } catch (error) {
          throw error
        }
      },

      batchMarkImportant: async (ids: number[], important: boolean) => {
        try {
          await tenderApi.batchMarkImportant(ids, important)
          set((state) => ({
            tenders: state.tenders.map(t => ids.includes(t.id) ? { ...t, is_important: important } : t)
          }))
        } catch (error) {
          throw error
        }
      },

      updateStatus: async (id: number, status: string) => {
        try {
          const response = await tenderApi.updateStatus(id, status)
          set((state) => ({
            tenders: state.tenders.map(t => t.id === id ? response.data : t)
          }))
        } catch (error) {
          throw error
        }
      },

      exportData: async (filters) => {
        try {
          const blob = await tenderApi.exportTenders(filters)
          const url = window.URL.createObjectURL(blob)
          const link = document.createElement('a')
          link.href = url
          link.download = `tenders_${new Date().toISOString().split('T')[0]}.xlsx`
          document.body.appendChild(link)
          link.click()
          document.body.removeChild(link)
          window.URL.revokeObjectURL(url)
        } catch (error) {
          throw error
        }
      },

      setFilters: (filters) => {
        set((state) => ({
          filters: { ...state.filters, ...filters }
        }))
      },

      clearFilters: () => {
        set({ filters: {} })
      },

      setSelectedRowKeys: (keys) => {
        set({ selectedRowKeys: keys })
      }
    })
  )
)

// 地区状态管理
interface RegionState {
  regions: Region[]
  selectedRegion: Region | null
  loading: boolean
  
  fetchRegionsTree: () => Promise<void>
  setSelectedRegion: (region: Region | null) => void
}

export const useRegionStore = create<RegionState>()(
  devtools(
    (set, get) => ({
      regions: [],
      selectedRegion: null,
      loading: false,

      fetchRegionsTree: async () => {
        set({ loading: true })
        try {
          const response = await regionApi.getRegionsTree()
          set({ regions: response.data?.tree || [], loading: false })
        } catch (error) {
          // 使用模拟地区数据作为fallback
          const mockRegions = [
            {
              id: 1,
              name: '北京市',
              code: '110000',
              level: 'province',
              parent_id: null,
              children: [
                {
                  id: 11,
                  name: '东城区',
                  code: '110101',
                  level: 'city',
                  parent_id: 1,
                  children: []
                },
                {
                  id: 12,
                  name: '西城区',
                  code: '110102',
                  level: 'city',
                  parent_id: 1,
                  children: []
                }
              ]
            },
            {
              id: 2,
              name: '上海市',
              code: '310000',
              level: 'province',
              parent_id: null,
              children: [
                {
                  id: 21,
                  name: '黄浦区',
                  code: '310101',
                  level: 'city',
                  parent_id: 2,
                  children: []
                },
                {
                  id: 22,
                  name: '徐汇区',
                  code: '310104',
                  level: 'city',
                  parent_id: 2,
                  children: []
                }
              ]
            }
          ]
          set({ regions: mockRegions, loading: false })
        }
      },

      setSelectedRegion: (region) => {
        set({ selectedRegion: region })
      }
    })
  )
)

// 爬虫状态管理
interface CrawlerState {
  status: CrawlerStatus | null
  logs: CrawlerLog[]
  totalLogs: number
  loading: boolean
  
  fetchCrawlerStatus: () => Promise<void>
  fetchCrawlerLogs: (params?: { page?: number; per_page?: number; level?: string }) => Promise<void>
  startCrawler: (data?: { hospital_ids?: number[]; force_update?: boolean }) => Promise<void>
  stopCrawler: () => Promise<void>
  triggerCrawler: (data: { hospital_ids?: number[]; priority?: 'low' | 'normal' | 'high' }) => Promise<void>
}

export const useCrawlerStore = create<CrawlerState>()(
  devtools(
    (set, get) => ({
      status: null,
      logs: [],
      totalLogs: 0,
      loading: false,

      fetchCrawlerStatus: async () => {
        try {
          const response = await crawlerApi.getCrawlerStatus()
          set({ status: response.data })
        } catch (error) {
          // 使用模拟爬虫状态作为fallback
          const mockStatus = {
            status: 'stopped' as const,
            progress: 0,
            current_task: undefined,
            total_tasks: 156,
            completed_tasks: 142,
            running_tasks: 0,
            error_tasks: 14,
            summary: {
              total_tasks: 156,
              running_count: 0,
              completed_count: 142,
              error_count: 14
            }
          }
          set({ status: mockStatus })
        }
      },

      fetchCrawlerLogs: async (params = {}) => {
        try {
          const response = await crawlerApi.getCrawlerLogs(params)
          set({
            logs: response.data.logs,
            totalLogs: response.data.pagination.total
          })
        } catch (error) {
          // 使用模拟日志数据作为fallback
          const mockLogs = [
            {
              id: 1,
              level: 'INFO',
              message: '开始扫描医院: 北京协和医院',
              timestamp: '2024-11-18T08:30:00Z',
              hospital_id: 1,
              hospital_name: '北京协和医院'
            },
            {
              id: 2,
              level: 'SUCCESS',
              message: '成功获取招投标信息: 3条',
              timestamp: '2024-11-18T08:30:45Z',
              hospital_id: 1,
              hospital_name: '北京协和医院'
            },
            {
              id: 3,
              level: 'INFO',
              message: '开始扫描医院: 上海中山医院',
              timestamp: '2024-11-18T08:31:00Z',
              hospital_id: 2,
              hospital_name: '上海中山医院'
            },
            {
              id: 4,
              level: 'ERROR',
              message: '网站访问超时',
              timestamp: '2024-11-18T08:31:30Z',
              hospital_id: 2,
              hospital_name: '上海中山医院'
            }
          ]
          set({
            logs: mockLogs,
            totalLogs: mockLogs.length
          })
        }
      },

      startCrawler: async (data) => {
        set({ loading: true })
        try {
          await crawlerApi.startCrawler(data)
          set({ loading: false })
          await get().fetchCrawlerStatus()
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      stopCrawler: async () => {
        set({ loading: true })
        try {
          await crawlerApi.stopCrawler()
          set({ loading: false })
          await get().fetchCrawlerStatus()
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      triggerCrawler: async (data) => {
        set({ loading: true })
        try {
          await crawlerApi.triggerCrawler(data)
          set({ loading: false })
          await get().fetchCrawlerStatus()
        } catch (error) {
          set({ loading: false })
          throw error
        }
      }
    })
  )
)

// 统计数据管理
interface StatisticsState {
  statistics: Statistics | null
  dashboardData: any | null
  trendData: any[] | null
  loading: boolean
  
  fetchStatistics: () => Promise<void>
  fetchDashboardData: () => Promise<void>
  fetchTrendData: (params?: { date_from?: string; date_to?: string; granularity?: 'daily' | 'weekly' | 'monthly' }) => Promise<void>
}

export const useStatisticsStore = create<StatisticsState>()(
  devtools(
    (set, get) => ({
      statistics: null,
      dashboardData: null,
      trendData: null,
      loading: false,

      fetchStatistics: async () => {
        set({ loading: true })
        try {
          const response = await statisticsApi.getStatistics()
          set({ statistics: response.data, loading: false })
        } catch (error) {
          // 使用模拟统计数据作为fallback
          const mockStatistics = {
            total_hospitals: 1400,
            monthly_tenders: 2345,
            total_budget: 1250000000, // 12.5亿元
            success_rate: 89.2,
            trend_data: [
              { date: '2024-11-01', tenders: 85, success_rate: 88.5 },
              { date: '2024-11-02', tenders: 92, success_rate: 91.2 },
              { date: '2024-11-03', tenders: 78, success_rate: 86.8 },
              { date: '2024-11-04', tenders: 105, success_rate: 92.1 },
              { date: '2024-11-05', tenders: 88, success_rate: 89.3 },
              { date: '2024-11-06', tenders: 95, success_rate: 90.7 },
              { date: '2024-11-07', tenders: 110, success_rate: 93.4 }
            ]
          }
          set({ statistics: mockStatistics, loading: false })
        }
      },

      fetchDashboardData: async () => {
        set({ loading: true })
        try {
          const response = await statisticsApi.getDashboardData()
          set({ dashboardData: response.data, loading: false })
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      fetchTrendData: async (params) => {
        try {
          const response = await statisticsApi.getTrendData(params)
          set({ trendData: response.data })
        } catch (error) {
          throw error
        }
      }
    })
  )
)

// 医院扫描历史状态管理
interface HospitalScanHistoryState {
  scanHistory: HospitalScanHistory[]
  total: number
  loading: boolean
  
  fetchScanHistory: (hospitalId: number, params?: { page?: number; per_page?: number }) => Promise<void>
  clearScanHistory: () => void
}

export const useHospitalScanHistoryStore = create<HospitalScanHistoryState>()(
  devtools(
    (set, get) => ({
      scanHistory: [],
      total: 0,
      loading: false,

      fetchScanHistory: async (hospitalId, params = {}) => {
        set({ loading: true })
        try {
          const response = await hospitalApi.getScanHistory(hospitalId, params)
          set({ 
            scanHistory: response.data, 
            total: response.pagination.total,
            loading: false 
          })
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      clearScanHistory: () => {
        set({ scanHistory: [], total: 0 })
      }
    })
  )
)

// 定时任务状态管理
interface SchedulerState {
  tasks: ScheduledTask[]
  total: number
  loading: boolean
  
  fetchScheduledTasks: (params?: { page?: number; per_page?: number }) => Promise<void>
  createScheduledTask: (task: any) => Promise<void>
  updateScheduledTask: (id: string, task: any) => Promise<void>
  deleteScheduledTask: (id: string) => Promise<void>
  toggleScheduledTask: (id: string, enabled: boolean) => Promise<void>
  executeScheduledTask: (id: string) => Promise<void>
}

export const useSchedulerStore = create<SchedulerState>()(
  devtools(
    (set, get) => ({
      tasks: [],
      total: 0,
      loading: false,

      fetchScheduledTasks: async (params = {}) => {
        set({ loading: true })
        try {
          const response = await schedulerApi.getScheduledTasks(params)
          set({ 
            tasks: response.data, 
            total: response.pagination.total,
            loading: false 
          })
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      createScheduledTask: async (task) => {
        set({ loading: true })
        try {
          const response = await schedulerApi.createScheduledTask(task)
          set((state) => ({
            tasks: [response.data, ...state.tasks],
            total: state.total + 1,
            loading: false
          }))
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      updateScheduledTask: async (id, task) => {
        set({ loading: true })
        try {
          const response = await schedulerApi.updateScheduledTask(id, task)
          set((state) => ({
            tasks: state.tasks.map(t => t.id === id ? response.data : t),
            loading: false
          }))
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      deleteScheduledTask: async (id) => {
        set({ loading: true })
        try {
          await schedulerApi.deleteScheduledTask(id)
          set((state) => ({
            tasks: state.tasks.filter(t => t.id !== id),
            total: state.total - 1,
            loading: false
          }))
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      toggleScheduledTask: async (id, enabled) => {
        try {
          const response = await schedulerApi.toggleScheduledTask(id, enabled)
          set((state) => ({
            tasks: state.tasks.map(t => t.id === id ? response.data : t)
          }))
        } catch (error) {
          throw error
        }
      },

      executeScheduledTask: async (id) => {
        try {
          await schedulerApi.executeScheduledTask(id)
        } catch (error) {
          throw error
        }
      }
    })
  )
)

// 系统设置状态管理
interface SystemSettingsState {
  settings: SystemSettings | null
  systemInfo: { version: string; uptime: number; health: string } | null
  loading: boolean
  
  fetchSettings: () => Promise<void>
  updateSettings: (settings: SystemSettings) => Promise<void>
  testEmail: (config: { smtp_server: string; smtp_port: number; username: string; password: string; recipients: string[] }) => Promise<void>
  testSms: (config: { api_key: string; recipients: string[] }) => Promise<void>
  fetchSystemInfo: () => Promise<void>
  resetToDefaults: () => Promise<void>
}

export const useSystemSettingsStore = create<SystemSettingsState>()(
  devtools(
    (set, get) => ({
      settings: null,
      systemInfo: null,
      loading: false,

      fetchSettings: async () => {
        set({ loading: true })
        try {
          const response = await systemApi.getSettings()
          set({ settings: response.data, loading: false })
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      updateSettings: async (settings: SystemSettings) => {
        set({ loading: true })
        try {
          const response = await systemApi.updateSettings(settings)
          set({ settings: response.data, loading: false })
        } catch (error) {
          set({ loading: false })
          throw error
        }
      },

      testEmail: async (config) => {
        try {
          await systemApi.testEmail(config)
        } catch (error) {
          throw error
        }
      },

      testSms: async (config) => {
        try {
          await systemApi.testSms(config)
        } catch (error) {
          throw error
        }
      },

      fetchSystemInfo: async () => {
        try {
          const response = await systemApi.getSystemInfo()
          set({ systemInfo: response.data })
        } catch (error) {
          throw error
        }
      },

      resetToDefaults: async () => {
        set({ loading: true })
        try {
          const response = await systemApi.resetToDefaults()
          set({ settings: response.data, loading: false })
        } catch (error) {
          set({ loading: false })
          throw error
        }
      }
    })
  )
)