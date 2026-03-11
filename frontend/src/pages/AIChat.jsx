import { useState, useRef, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { chatWithAgent } from '../services/api'

export default function AIChat() {
  const navigate = useNavigate()
  const [messages, setMessages] = useState([
    { role: 'assistant', content: 'Hello! I am MedSync AI 🤖 I can help you log interactions, analyze HCP profiles, suggest followups, and more. How can I help you today?' }
  ])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const sendMessage = async () => {
    if (!input.trim() || loading) return

    const userMsg = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const res = await chatWithAgent(input)
      const aiMsg = { role: 'assistant', content: res.data.response }
      setMessages(prev => [...prev, aiMsg])
    } catch (err) {
      setMessages(prev => [...prev, { role: 'assistant', content: '❌ Error connecting to AI. Please try again.' }])
    } finally {
      setLoading(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white flex">
      {/* Sidebar */}
      <div className="fixed left-0 top-0 h-full w-64 bg-gray-900 border-r border-gray-800 flex flex-col">
        <div className="p-6 border-b border-gray-800">
          <div className="text-2xl mb-1">🏥</div>
          <h1 className="text-xl font-bold text-white">MedSync AI</h1>
          <p className="text-gray-400 text-xs">HCP Management</p>
        </div>
        <nav className="flex-1 p-4 space-y-2">
          <button onClick={() => navigate('/dashboard')} className="w-full text-left px-4 py-3 rounded-lg text-gray-400 hover:bg-gray-800 hover:text-white transition">
            📊 Dashboard
          </button>
          <button onClick={() => navigate('/hcps')} className="w-full text-left px-4 py-3 rounded-lg text-gray-400 hover:bg-gray-800 hover:text-white transition">
            👨‍⚕️ HCPs
          </button>
          <button onClick={() => navigate('/interactions')} className="w-full text-left px-4 py-3 rounded-lg text-gray-400 hover:bg-gray-800 hover:text-white transition">
            📋 Interactions
          </button>
          <button onClick={() => navigate('/chat')} className="w-full text-left px-4 py-3 rounded-lg bg-purple-600 text-white font-medium">
            🤖 AI Chat
          </button>
        </nav>
      </div>

      {/* Chat Area */}
      <div className="ml-64 flex flex-col flex-1 h-screen">
        {/* Header */}
        <div className="bg-gray-900 border-b border-gray-800 px-8 py-4 flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-purple-600 flex items-center justify-center text-xl">🤖</div>
          <div>
            <h2 className="text-white font-semibold">MedSync AI Agent</h2>
            <p className="text-green-400 text-xs">● Online</p>
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto px-8 py-6 space-y-4">
          {messages.map((msg, i) => (
            <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div className={`max-w-2xl px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                msg.role === 'user'
                  ? 'bg-blue-600 text-white rounded-br-sm'
                  : 'bg-gray-800 text-gray-100 rounded-bl-sm'
              }`}>
                {msg.content}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex justify-start">
              <div className="bg-gray-800 text-gray-400 px-4 py-3 rounded-2xl rounded-bl-sm text-sm">
                🤖 Thinking...
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>

        {/* Input */}
        <div className="bg-gray-900 border-t border-gray-800 px-8 py-4">
          <div className="flex gap-3">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask AI to log interaction, analyze HCP, suggest followup... (Enter to send)"
              className="flex-1 bg-gray-800 border border-gray-700 text-white rounded-xl px-4 py-3 focus:outline-none focus:border-purple-500 resize-none text-sm"
              rows={2}
            />
            <button
              onClick={sendMessage}
              disabled={loading || !input.trim()}
              className="bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white px-6 py-3 rounded-xl transition font-medium"
            >
              Send 🚀
            </button>
          </div>
          <p className="text-gray-500 text-xs mt-2">Try: "Show me Dr. Sharma's profile" or "Log a meeting with Dr. Sharma about oncology drugs"</p>
        </div>
      </div>
    </div>
  )
}