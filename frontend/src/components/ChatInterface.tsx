import React, { useState, useRef, useEffect } from 'react'
import { useMutation } from '@tanstack/react-query'
import { Send, Bot, User, CheckCircle, Loader2, Zap, Cpu, Globe } from 'lucide-react'
import toast from 'react-hot-toast'
import ReactMarkdown from 'react-markdown'
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter'
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism'

import { chatApi, ChatRequest, ChatResponse, FeedbackRequest } from '../services/api'
import { useFloxEnvironment, useFloxStats } from '../hooks/useApi'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: string
  sources?: any[]
  model?: string
  response_time?: number
  worked?: boolean
  flox_info?: any
}

export default function ChatInterface() {
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [sessionId, setSessionId] = useState<string | null>(null)
  const messagesEndRef = useRef<HTMLDivElement>(null)
  
  const { environmentName, platform } = useFloxEnvironment()
  const { data: floxStats } = useFloxStats()

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages])

  const chatMutation = useMutation({
    mutationFn: (request: ChatRequest) => chatApi.query(request),
    onSuccess: (data: ChatResponse) => {
      const assistantMessage: Message = {
        id: data.message_id.toString(),
        role: 'assistant',
        content: data.response,
        timestamp: new Date().toISOString(),
        sources: data.sources,
        model: data.model,
        response_time: data.response_time,
        flox_info: data.flox_info
      }
      
      setMessages(prev => [...prev, assistantMessage])
      
      if (!sessionId) {
        setSessionId(data.session_id)
      }
    },
    onError: (error: any) => {
      toast.error(error.message || 'Failed to send message')
    }
  })

  const feedbackMutation = useMutation({
    mutationFn: (request: FeedbackRequest) => chatApi.submitFeedback(request),
    onSuccess: (data) => {
      toast.success(data.message || 'Feedback submitted!')
    }
  })

  const handleSend = () => {
    if (!input.trim() || chatMutation.isPending) return

    const userMessage: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date().toISOString()
    }

    setMessages(prev => [...prev, userMessage])

    chatMutation.mutate({
      message: input.trim(),
      session_id: sessionId || undefined,
      mode: 'flox_expert'
    })

    setInput('')
  }

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleWorkedFeedback = (messageId: string) => {
    if (!sessionId) return

    feedbackMutation.mutate({
      message_id: parseInt(messageId),
      session_id: sessionId,
      worked: true
    })

    setMessages(prev => prev.map(msg => 
      msg.id === messageId ? { ...msg, worked: true } : msg
    ))
  }

  const quickPrompts = [
    {
      icon: <Zap className="w-4 h-4" />,
      title: "Getting Started",
      prompt: "How do I create a new Flox environment for a Python web app?"
    },
    {
      icon: <Cpu className="w-4 h-4" />,
      title: "Cross-Platform",
      prompt: "Show me how Flox ensures my environment works on macOS and Linux"
    },
    {
      icon: <Globe className="w-4 h-4" />,
      title: "Best Practices", 
      prompt: "What are the Flox best practices for a full-stack JavaScript project?"
    }
  ]

  return (
    <div className="flex flex-col h-screen flox-gradient-bg">
      {/* Enhanced Header with Flox Branding */}
      <div className="p-4 border-b border-slate-700 bg-slate-800/30 backdrop-blur-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 flox-gradient rounded-xl flex items-center justify-center animate-flox-pulse">
              <Bot className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-white text-xl font-bold">FloxAI</h1>
              <p className="text-slate-400 text-sm">The Flox Development Co-pilot</p>
            </div>
          </div>
          
          {/* Flox Environment Info */}
          <div className="hidden md:flex items-center gap-4 text-xs">
            <div className="flox-card px-3 py-2 rounded-lg">
              <span className="text-slate-400">Environment:</span>
              <span className="text-flox-400 ml-1 font-mono">{environmentName}</span>
            </div>
            <div className="flox-card px-3 py-2 rounded-lg">
              <span className="text-slate-400">Platform:</span>
              <span className="text-purple-400 ml-1 font-mono">{platform}</span>
            </div>
          </div>
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.length === 0 && (
          <div className="text-center py-12">
            <div className="w-20 h-20 flox-gradient rounded-2xl flex items-center justify-center mx-auto mb-6 animate-bounce-slow">
              <Bot className="w-10 h-10 text-white" />
            </div>
            <h3 className="text-white text-2xl font-bold mb-3">Welcome to FloxAI! 🚀</h3>
            <p className="text-slate-300 max-w-2xl mx-auto mb-8 leading-relaxed">
              I'm your <span className="text-flox-400 font-semibold">Flox development co-pilot</span>, designed to showcase the incredible power of 
              <span className="text-purple-400 font-semibold"> reproducible, cross-platform development environments</span>. 
              Ask me anything about Flox, upload files for analysis, or explore what makes Flox special!
            </p>
            
            {/* Flox Stats */}
            {floxStats && (
              <div className="mb-8 grid grid-cols-1 md:grid-cols-3 gap-4 max-w-md mx-auto">
                <div className="flox-card p-3 rounded-lg">
                  <div className="text-flox-400 text-2xl font-bold">{floxStats.usage_stats?.total_messages || 0}</div>
                  <div className="text-slate-400 text-xs">Messages</div>
                </div>
                <div className="flox-card p-3 rounded-lg">
                  <div className="text-purple-400 text-2xl font-bold">{floxStats.usage_stats?.success_rate || 0}%</div>
                  <div className="text-slate-400 text-xs">Success Rate</div>
                </div>
                <div className="flox-card p-3 rounded-lg">
                  <div className="text-green-400 text-2xl font-bold">{floxStats.usage_stats?.unique_sessions || 0}</div>
                  <div className="text-slate-400 text-xs">Sessions</div>
                </div>
              </div>
            )}

            {/* Quick Action Prompts */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 max-w-4xl mx-auto">
              {quickPrompts.map((prompt, index) => (
                <button
                  key={index}
                  onClick={() => setInput(prompt.prompt)}
                  className="flox-card p-4 rounded-xl text-left hover:scale-105 transform transition-all group"
                >
                  <div className="flex items-center gap-3 mb-2">
                    <div className="text-flox-400 group-hover:text-flox-300">
                      {prompt.icon}
                    </div>
                    <h4 className="text-white font-semibold group-hover:text-flox-300">
                      {prompt.title}
                    </h4>
                  </div>
                  <p className="text-slate-400 text-sm group-hover:text-slate-300">
                    {prompt.prompt}
                  </p>
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((message) => (
          <div key={message.id} className="flex gap-4">
            <div className="flex-shrink-0">
              {message.role === 'user' ? (
                <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-full flex items-center justify-center">
                  <User className="w-4 h-4 text-white" />
                </div>
              ) : (
                <div className="w-8 h-8 flox-gradient rounded-full flex items-center justify-center">
                  <Bot className="w-4 h-4 text-white" />
                </div>
              )}
            </div>

            <div className="flex-1 min-w-0">
              <div className="flex items-center gap-2 mb-2">
                <span className="text-slate-300 font-medium">
                  {message.role === 'user' ? 'You' : 'FloxAI'}
                </span>
                <span className="text-slate-500 text-xs">
                  {new Date(message.timestamp).toLocaleTimeString()}
                </span>
                {message.response_time && (
                  <span className="text-slate-500 text-xs">
                    ({message.response_time.toFixed(1)}s)
                  </span>
                )}
                {message.model && message.model !== 'floxai-local' && (
                  <span className="text-flox-400 text-xs bg-flox-400/10 px-2 py-1 rounded">
                    {message.model}
                  </span>
                )}
              </div>

              <div className="flox-card rounded-lg p-4">
                <ReactMarkdown
                  components={{
                    code({ className, children, ...props }: any) {
                      const match = /language-(\w+)/.exec(className || '')
                      const inline = !match
                      return !inline && match ? (
                        <div className="my-4">
                          <div className="bg-slate-800 px-3 py-2 text-xs text-slate-400 border-b border-slate-600">
                            {match[1]} {match[1] === 'toml' && '(Flox manifest)'}
                          </div>
                          <SyntaxHighlighter
                            style={oneDark as any}
                            language={match[1]}
                            PreTag="div"
                            customStyle={{
                              margin: 0,
                              borderRadius: '0 0 0.375rem 0.375rem',
                              background: '#0f172a'
                            }}
                          >
                            {String(children).replace(/\n$/, '')}
                          </SyntaxHighlighter>
                        </div>
                      ) : (
                        <code className="bg-slate-700 text-flox-300 px-1.5 py-0.5 rounded text-sm font-mono" {...props}>
                          {children}
                        </code>
                      )
                    },
                    h1: ({ children }) => (
                      <h1 className="text-xl font-bold text-white mb-3">{children}</h1>
                    ),
                    h2: ({ children }) => (
                      <h2 className="text-lg font-semibold text-white mb-2">{children}</h2>
                    ),
                    h3: ({ children }) => (
                      <h3 className="text-base font-medium text-white mb-2">{children}</h3>
                    ),
                    p: ({ children }) => (
                      <p className="text-slate-200 mb-3 leading-relaxed">{children}</p>
                    ),
                    ul: ({ children }) => (
                      <ul className="text-slate-200 mb-3 pl-6 space-y-1 list-disc">{children}</ul>
                    ),
                    ol: ({ children }) => (
                      <ol className="text-slate-200 mb-3 pl-6 space-y-1 list-decimal">{children}</ol>
                    ),
                    blockquote: ({ children }) => (
                      <blockquote className="border-l-4 border-flox-500 pl-4 italic text-slate-300 my-3 bg-flox-500/5 py-2">
                        {children}
                      </blockquote>
                    ),
                    a: ({ href, children }) => (
                      <a 
                        href={href} 
                        className="text-flox-400 hover:text-flox-300 underline"
                        target="_blank"
                        rel="noopener noreferrer"
                      >
                        {children}
                      </a>
                    ),
                  }}
                  className="prose prose-invert prose-flox max-w-none"
                >
                  {message.content}
                </ReactMarkdown>
              </div>

              {/* Enhanced Sources with Doc Type Labels */}
              {message.sources && message.sources.length > 0 && (
                <div className="mt-3 text-xs">
                  <details className="cursor-pointer">
                    <summary className="text-slate-400 hover:text-slate-300 flex items-center gap-1">
                      📚 Sources used ({message.sources.length})
                    </summary>
                    <div className="mt-2 space-y-2">
                      {message.sources.slice(0, 3).map((source, index) => (
                        <div key={index} className="bg-slate-800/50 border border-slate-600 rounded-lg p-3">
                          <div className="flex items-center gap-2 mb-1">
                            <span className="font-mono text-flox-400 text-xs">{source.source}</span>
                            {source.doc_type && (
                              <span className={`px-2 py-1 rounded text-xs ${
                                source.doc_type === 'flox_knowledge' ? 'bg-flox-500/20 text-flox-300' :
                                source.doc_type === 'best_practices' ? 'bg-purple-500/20 text-purple-300' :
                                'bg-slate-500/20 text-slate-300'
                              }`}>
                                {source.doc_type.replace('_', ' ')}
                              </span>
                            )}
                          </div>
                          <div className="text-slate-400 text-xs leading-relaxed">
                            {source.content.substring(0, 200)}...
                          </div>
                          <div className="text-slate-500 text-xs mt-1">
                            Relevance: {Math.round(source.relevance_score * 100)}%
                          </div>
                        </div>
                      ))}
                    </div>
                  </details>
                </div>
              )}

              {/* Enhanced Feedback for assistant messages */}
              {message.role === 'assistant' && sessionId && (
                <div className="flex items-center gap-2 mt-3">
                  <button
                    onClick={() => handleWorkedFeedback(message.id)}
                    className={`px-3 py-1.5 text-xs rounded-lg transition-all transform hover:scale-105 ${
                      message.worked
                        ? 'bg-green-500/20 text-green-400 border border-green-400/30'
                        : 'bg-slate-700 text-slate-400 hover:text-green-400 hover:bg-green-500/10 border border-slate-600'
                    }`}
                    disabled={feedbackMutation.isPending}
                  >
                    <CheckCircle className="w-3 h-3 inline mr-1" />
                    {message.worked ? 'Marked as helpful!' : 'This worked!'}
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}

        {/* Loading indicator */}
        {chatMutation.isPending && (
          <div className="flex gap-4">
            <div className="w-8 h-8 flox-gradient rounded-full flex items-center justify-center animate-flox-pulse">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="flox-card rounded-lg p-4 min-w-0 flex-1">
              <div className="flex items-center gap-2 text-slate-400">
                <Loader2 className="w-4 h-4 animate-spin text-flox-400" />
                <span>FloxAI is thinking...</span>
                <div className="ml-2 flex gap-1">
                  <div className="w-1 h-1 bg-flox-400 rounded-full animate-pulse"></div>
                  <div className="w-1 h-1 bg-flox-400 rounded-full animate-pulse" style={{animationDelay: '0.2s'}}></div>
                  <div className="w-1 h-1 bg-flox-400 rounded-full animate-pulse" style={{animationDelay: '0.4s'}}></div>
                </div>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Enhanced Input */}
      <div className="p-4 border-t border-slate-700 bg-slate-800/30 backdrop-blur-sm">
        <div className="flex gap-3">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}
            placeholder="Ask FloxAI anything about Flox development, or try: 'How do I create a manifest.toml?'"
            className="flex-1 bg-slate-700/50 text-white placeholder-slate-400 border border-slate-600 focus:border-flox-500/50 rounded-xl px-4 py-3 resize-none focus:outline-none focus:ring-2 focus:ring-flox-500/20 min-h-[3rem] max-h-32 transition-colors"
            rows={1}
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || chatMutation.isPending}
            className="flox-button rounded-xl flex items-center justify-center disabled:opacity-50 disabled:cursor-not-allowed disabled:hover:scale-100"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  )
}
