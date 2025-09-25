import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
    'X-FloxAI-Client': 'web-frontend-1.0.0',
  },
})

// Enhanced request interceptor
api.interceptors.request.use(
  (config) => {
    console.log(`🚀 FloxAI API Request: ${config.method?.toUpperCase()} ${config.url}`)
    return config
  },
  (error) => {
    console.error('❌ FloxAI API Request Error:', error)
    return Promise.reject(error)
  }
)

// Enhanced response interceptor
api.interceptors.response.use(
  (response) => {
    console.log(`✅ FloxAI API Response: ${response.status} ${response.config.url}`)
    return response
  },
  (error) => {
    console.error('❌ FloxAI API Response Error:', error.response?.data || error.message)
    
    if (error.response?.status === 503) {
      throw new Error('FloxAI services are initializing. Please wait a moment and try again.')
    }
    
    if (error.code === 'ECONNABORTED') {
      throw new Error('The AI is taking longer than usual to respond. Please try again.')
    }
    
    if (error.response?.status >= 500) {
      throw new Error('FloxAI server error. Please check that the backend is running.')
    }
    
    throw error
  }
)

export interface ChatRequest {
  message: string
  session_id?: string
  mode: string
}

export interface ChatResponse {
  response: string
  session_id: string
  message_id: number
  sources: Array<{
    content: string
    source: string
    relevance_score: number
    doc_type?: string
  }>
  model: string
  response_time: number
  flox_info: {
    environment_name: string
    project_directory: string
    floxai_version: string
    is_flox_env: boolean
    system_info: {
      platform: string
      architecture: string
    }
  }
}

export interface FeedbackRequest {
  message_id: number
  session_id: string
  worked: boolean
}

export interface HealthResponse {
  status: string
  service: string
  version: string
  flox_environment: {
    name: string
    is_flox_env: boolean
    platform: string
  }
  services: {
    rag: boolean
    llm: boolean
  }
  endpoints: {
    chat: string
    docs: string
    flox_stats: string
  }
}

export const chatApi = {
  async query(request: ChatRequest): Promise<ChatResponse> {
    const response = await api.post('/api/chat/query', request)
    return response.data
  },

  async submitFeedback(feedback: FeedbackRequest): Promise<{status: string; message: string}> {
    const response = await api.post('/api/chat/feedback', feedback)
    return response.data
  },

  async getHistory(sessionId: string): Promise<any> {
    const response = await api.get(`/api/chat/history/${sessionId}`)
    return response.data
  },

  async getFloxStats(): Promise<any> {
    const response = await api.get('/api/chat/flox-stats')
    return response.data
  }
}

export const systemApi = {
  async getHealth(): Promise<HealthResponse> {
    const response = await api.get('/health')
    return response.data
  },

  async getRoot(): Promise<any> {
    const response = await api.get('/')
    return response.data
  }
}

export default api
