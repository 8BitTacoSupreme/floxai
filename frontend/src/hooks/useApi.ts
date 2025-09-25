import { useQuery } from '@tanstack/react-query'
import { systemApi, chatApi } from '../services/api'

export function useApi() {
  const { data: apiHealth, isLoading, error } = useQuery({
    queryKey: ['api-health'],
    queryFn: systemApi.getHealth,
    retry: 3,
    retryDelay: 1000,
    refetchInterval: 30000,
  })

  return {
    apiHealth,
    isLoading,
    isHealthy: apiHealth?.status === 'healthy',
    error,
    floxInfo: apiHealth?.flox_environment
  }
}

export function useFloxStats() {
  return useQuery({
    queryKey: ['flox-stats'],
    queryFn: chatApi.getFloxStats,
    refetchInterval: 60000, // Refresh every minute
    retry: false,
  })
}

export function useFloxEnvironment() {
  const { data: rootInfo } = useQuery({
    queryKey: ['flox-root-info'],
    queryFn: systemApi.getRoot,
    staleTime: 1000 * 60 * 10, // 10 minutes
  })

  return {
    environmentName: rootInfo?.flox_environment || 'unknown',
    platform: rootInfo?.platform || 'unknown',
    version: rootInfo?.version || '1.0.0'
  }
}
