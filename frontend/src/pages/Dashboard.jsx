import { useSelector, useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { logout } from '../store/authSlice'

export default function Dashboard() {
  const { user } = useSelector((state) => state.auth)
  const dispatch = useDispatch()
  const navigate = useNavigate()

  const handleLogout = () => {
    dispatch(logout())
    navigate('/login')
  }

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      
      {/* Sidebar */}
      <div className="fixed left-0 top-0 h-full w-64 bg-gray-900 border-r border-gray-800 flex flex-col">
        <div className="p-6 border-b border-gray-800">
          <div className="text-2xl mb-1">🏥</div>
          <h1 className="text-xl font-bold text-white">MedSync AI</h1>
          <p className="text-gray-400 text-xs">HCP Management</p>
        </div>

        <nav className="flex-1 p-4 space-y-2">
          <button onClick={() => navigate('/dashboard')} className="w-full text-left px-4 py-3 rounded-lg bg-blue-600 text-white font-medium">
            📊 Dashboard
          </button>
          <button onClick={() => navigate('/hcps')} className="w-full text-left px-4 py-3 rounded-lg text-gray-400 hover:bg-gray-800 hover:text-white transition">
            👨‍⚕️ HCPs
          </button>
          <button onClick={() => navigate('/interactions')} className="w-full text-left px-4 py-3 rounded-lg text-gray-400 hover:bg-gray-800 hover:text-white transition">
            📋 Interactions
          </button>
          <button onClick={() => navigate('/chat')} className="w-full text-left px-4 py-3 rounded-lg text-gray-400 hover:bg-gray-800 hover:text-white transition">
            🤖 AI Chat
          </button>
        </nav>

        <div className="p-4 border-t border-gray-800">
          <div className="flex items-center gap-3 mb-3">
            <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-sm font-bold">
              {user?.name?.charAt(0) || 'S'}
            </div>
            <div>
              <p className="text-white text-sm font-medium">{user?.name || 'Shobhit Singh'}</p>
              <p className="text-gray-400 text-xs">{user?.role || 'sales_rep'}</p>
            </div>
          </div>
          <button onClick={handleLogout} className="w-full text-left px-4 py-2 rounded-lg text-red-400 hover:bg-red-900/20 transition text-sm">
            🚪 Logout
          </button>
        </div>
      </div>

      {/* Main Content */}
      <div className="ml-64 p-8">
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-white">Welcome back, {user?.name?.split(' ')[0] || 'Shobhit'}! 👋</h2>
          <p className="text-gray-400 mt-1">Here's your HCP activity overview</p>
        </div>

        {/* Stats Cards */}
        <div className="grid grid-cols-4 gap-6 mb-8">
          {[
            { label: 'Total HCPs', value: '1', icon: '👨‍⚕️' },
            { label: 'Interactions', value: '0', icon: '📋' },
            { label: 'Pending Followups', value: '0', icon: '⏰' },
            { label: 'AI Summaries', value: '0', icon: '🤖' },
          ].map((stat) => (
            <div key={stat.label} className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <div className="text-3xl mb-3">{stat.icon}</div>
              <div className="text-3xl font-bold text-white">{stat.value}</div>
              <div className="text-gray-400 text-sm mt-1">{stat.label}</div>
            </div>
          ))}
        </div>

        {/* Quick Actions */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
          <h3 className="text-lg font-semibold text-white mb-4">Quick Actions</h3>
          <div className="grid grid-cols-3 gap-4">
            <button onClick={() => navigate('/hcps')} className="bg-blue-600 hover:bg-blue-700 text-white py-3 px-4 rounded-lg transition font-medium">
              + Add HCP
            </button>
            <button onClick={() => navigate('/interactions')} className="bg-green-600 hover:bg-green-700 text-white py-3 px-4 rounded-lg transition font-medium">
              + Log Interaction
            </button>
            <button onClick={() => navigate('/chat')} className="bg-purple-600 hover:bg-purple-700 text-white py-3 px-4 rounded-lg transition font-medium">
              🤖 Ask AI Agent
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}