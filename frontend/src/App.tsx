import { Bot, AlertTriangle, Zap } from 'lucide-react'
import ChatInterface from './components/ChatInterface'
import { useApi } from './hooks/useApi'

function App() {
  const { apiHealth, isLoading } = useApi()

  if (isLoading) {
    return (
      <div className="min-h-screen flox-gradient-bg flex items-center justify-center">
        <div className="text-center">
          <div className="w-16 h-16 flox-gradient rounded-2xl flex items-center justify-center mx-auto mb-6 animate-flox-pulse">
            <Bot className="w-8 h-8 text-white" />
          </div>
          <h2 className="text-2xl text-white mb-3 font-bold">Starting FloxAI...</h2>
          <p className="text-slate-400 mb-4">Initializing your Flox development co-pilot</p>
          <div className="flex justify-center gap-1">
            <div className="w-2 h-2 bg-flox-400 rounded-full animate-pulse"></div>
            <div className="w-2 h-2 bg-flox-400 rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
            <div className="w-2 h-2 bg-flox-400 rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
          </div>
        </div>
      </div>
    )
  }

  if (!apiHealth?.status || apiHealth.status !== 'healthy') {
    return (
      <div className="min-h-screen flox-gradient-bg flex items-center justify-center">
        <div className="text-center max-w-lg">
          <div className="w-16 h-16 bg-red-500/20 border-2 border-red-500 rounded-2xl flex items-center justify-center mx-auto mb-6">
            <AlertTriangle className="w-8 h-8 text-red-400" />
          </div>
          <h2 className="text-2xl text-white mb-3 font-bold">FloxAI Backend Not Ready</h2>
          <p className="text-slate-300 mb-6 leading-relaxed">
            The FloxAI backend is not responding. This could mean:
          </p>
          
          <div className="bg-slate-800/50 border border-slate-600 rounded-xl p-6 mb-6 text-left">
            <h3 className="text-white font-semibold mb-3 flex items-center gap-2">
              <Zap className="w-4 h-4 text-flox-400" />
              Quick Fix Steps:
            </h3>
            <ol className="text-slate-300 space-y-2 text-sm list-decimal list-inside">
              <li>Make sure the backend is running: <code className="bg-slate-700 px-2 py-1 rounded text-flox-300">./start-floxai.sh</code></li>
              <li>Set your Claude API key in the script or environment</li>
              <li>Wait for both backend (port 8000) and frontend (port 3000) to start</li>
            </ol>
          </div>
          
          <div className="flex flex-col sm:flex-row gap-3 justify-center">
            <a href="http://localhost:8000/health" target="_blank" rel="noopener noreferrer" className="flox-button text-center">
              Check Backend Health
            </a>
            <a href="http://localhost:8000/docs" target="_blank" rel="noopener noreferrer" className="bg-slate-700 hover:bg-slate-600 text-white font-medium px-4 py-2 rounded-lg transition-colors text-center">
              View API Docs
            </a>
          </div>
          
          <p className="text-slate-500 text-sm mt-6">
            FloxAI should be running at <code>http://localhost:8000</code>
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen">
      <ChatInterface />
    </div>
  )
}

export default App
