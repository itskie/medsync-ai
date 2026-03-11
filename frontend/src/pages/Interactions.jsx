import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getAllInteractions, createInteraction, getAllHCPs } from '../services/api'

export default function Interactions() {
  const navigate = useNavigate()
  const [interactions, setInteractions] = useState([])
  const [hcps, setHcps] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    hcp_id: '',
    interaction_type: 'meeting',
    date: '',
    topics_discussed: '',
    outcomes: '',
    sentiment: 'neutral'
  })

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [intRes, hcpRes] = await Promise.all([getAllInteractions(), getAllHCPs()])
      setInteractions(intRes.data)
      setHcps(hcpRes.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async () => {
    try {
      // Date format fix: MM/DD/YYYY → YYYY-MM-DD
      const dateFixed = form.date ? new Date(form.date).toISOString().split('T')[0] : ''
      await createInteraction({ ...form, date: dateFixed })
      setShowForm(false)
      setForm({ hcp_id: '', interaction_type: 'meeting', date: '', topics_discussed: '', outcomes: '', sentiment: 'neutral' })
      fetchData()
    } catch (err) {
      console.error(err)
    }
  }

  const sentimentColor = (s) => {
    if (s === 'positive') return 'text-green-400'
    if (s === 'negative') return 'text-red-400'
    return 'text-yellow-400'
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
          <button onClick={() => navigate('/dashboard')} className="w-full text-left px-4 py-3 rounded-lg text-gray-400 hover:bg-gray-800 hover:text-white transition">
            📊 Dashboard
          </button>
          <button onClick={() => navigate('/hcps')} className="w-full text-left px-4 py-3 rounded-lg text-gray-400 hover:bg-gray-800 hover:text-white transition">
            👨‍⚕️ HCPs
          </button>
          <button onClick={() => navigate('/interactions')} className="w-full text-left px-4 py-3 rounded-lg bg-blue-600 text-white font-medium">
            📋 Interactions
          </button>
        </nav>
      </div>

      {/* Main Content */}
      <div className="ml-64 p-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h2 className="text-3xl font-bold">Interactions 📋</h2>
            <p className="text-gray-400 mt-1">{interactions.length} interactions logged</p>
          </div>
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-lg font-medium transition"
          >
            + Log Interaction
          </button>
        </div>

        {/* Add Interaction Form */}
        {showForm && (
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 mb-6">
            <h3 className="text-lg font-semibold mb-4">Log New Interaction</h3>
            <div className="grid grid-cols-2 gap-4">
              <select
                value={form.hcp_id}
                onChange={(e) => setForm({ ...form, hcp_id: e.target.value })}
                className="bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
              >
                <option value="">Select HCP</option>
                {hcps.map((hcp) => (
                  <option key={hcp.id} value={hcp.id}>{hcp.name}</option>
                ))}
              </select>

              <select
                value={form.interaction_type}
                onChange={(e) => setForm({ ...form, interaction_type: e.target.value })}
                className="bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
              >
                <option value="meeting">Meeting</option>
                <option value="call">Call</option>
                <option value="email">Email</option>
                <option value="conference">Conference</option>
              </select>

              <input
                type="date"
                value={form.date}
                onChange={(e) => setForm({ ...form, date: e.target.value })}
                className="bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
              />

              <select
                value={form.sentiment}
                onChange={(e) => setForm({ ...form, sentiment: e.target.value })}
                className="bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
              >
                <option value="positive">😊 Positive</option>
                <option value="neutral">😐 Neutral</option>
                <option value="negative">😞 Negative</option>
              </select>

              <textarea
                placeholder="Topics discussed..."
                value={form.topics_discussed}
                onChange={(e) => setForm({ ...form, topics_discussed: e.target.value })}
                className="bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500 col-span-2"
                rows={2}
              />

              <textarea
                placeholder="Outcomes..."
                value={form.outcomes}
                onChange={(e) => setForm({ ...form, outcomes: e.target.value })}
                className="bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500 col-span-2"
                rows={2}
              />
            </div>
            <div className="flex gap-3 mt-4">
              <button onClick={handleCreate} className="bg-green-600 hover:bg-green-700 text-white px-6 py-2 rounded-lg transition">
                Save Interaction
              </button>
              <button onClick={() => setShowForm(false)} className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-2 rounded-lg transition">
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* Interactions List */}
        {loading ? (
          <p className="text-gray-400">Loading...</p>
        ) : interactions.length === 0 ? (
          <div className="text-center py-20 text-gray-500">
            <div className="text-6xl mb-4">📋</div>
            <p className="text-xl">No interactions yet — log your first one!</p>
          </div>
        ) : (
          <div className="space-y-4">
            {interactions.map((interaction) => (
              <div key={interaction.id} className="bg-gray-900 border border-gray-800 rounded-xl p-6">
                <div className="flex justify-between items-start">
                  <div>
                    <div className="flex items-center gap-3 mb-2">
                      <span className="bg-blue-600 text-white text-xs px-3 py-1 rounded-full capitalize">
                        {interaction.interaction_type}
                      </span>
                      <span className={`text-sm font-medium ${sentimentColor(interaction.sentiment)}`}>
                        {interaction.sentiment === 'positive' ? '😊' : interaction.sentiment === 'negative' ? '😞' : '😐'} {interaction.sentiment}
                      </span>
                    </div>
                    <p className="text-gray-300 text-sm">📅 {interaction.date}</p>
                    <p className="text-gray-300 text-sm mt-1">💬 {interaction.topics_discussed}</p>
                    {interaction.ai_summary && (
                      <p className="text-blue-300 text-sm mt-2 bg-blue-900/20 px-3 py-2 rounded-lg">
                        🤖 {interaction.ai_summary}
                      </p>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}