import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getAllHCPs, createHCP, deleteHCP } from '../services/api'

export default function HCPs() {
  const navigate = useNavigate()
  const [hcps, setHcps] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({
    name: '', specialization: '', hospital: '', city: '', email: '', phone: ''
  })

  // Fetch all HCPs on load
  useEffect(() => {
    fetchHCPs()
  }, [])

  const fetchHCPs = async () => {
    try {
      const res = await getAllHCPs()
      setHcps(res.data)
    } catch (err) {
      console.error(err)
    } finally {
      setLoading(false)
    }
  }

  const handleCreate = async () => {
    try {
      await createHCP(form)
      setShowForm(false)
      setForm({ name: '', specialization: '', hospital: '', city: '', email: '', phone: '' })
      fetchHCPs()
    } catch (err) {
      console.error(err)
    }
  }

  const handleDelete = async (id) => {
    if (confirm('Delete this HCP?')) {
      await deleteHCP(id)
      fetchHCPs()
    }
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
          <button onClick={() => navigate('/hcps')} className="w-full text-left px-4 py-3 rounded-lg bg-blue-600 text-white font-medium">
            👨‍⚕️ HCPs
          </button>
          <button onClick={() => navigate('/interactions')} className="w-full text-left px-4 py-3 rounded-lg text-gray-400 hover:bg-gray-800 hover:text-white transition">
            📋 Interactions
          </button>
        </nav>
      </div>

      {/* Main Content */}
      <div className="ml-64 p-8">
        <div className="flex justify-between items-center mb-8">
          <div>
            <h2 className="text-3xl font-bold">Healthcare Professionals 👨‍⚕️</h2>
            <p className="text-gray-400 mt-1">{hcps.length} HCPs registered</p>
          </div>
          <button
            onClick={() => setShowForm(!showForm)}
            className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-lg font-medium transition"
          >
            + Add HCP
          </button>
        </div>

        {/* Add HCP Form */}
        {showForm && (
          <div className="bg-gray-900 border border-gray-800 rounded-xl p-6 mb-6">
            <h3 className="text-lg font-semibold mb-4">Add New HCP</h3>
            <div className="grid grid-cols-2 gap-4">
              {[
                { key: 'name', placeholder: 'Dr. Full Name' },
                { key: 'specialization', placeholder: 'Specialization' },
                { key: 'hospital', placeholder: 'Hospital Name' },
                { key: 'city', placeholder: 'City' },
                { key: 'email', placeholder: 'Email' },
                { key: 'phone', placeholder: 'Phone' },
              ].map(({ key, placeholder }) => (
                <input
                  key={key}
                  placeholder={placeholder}
                  value={form[key]}
                  onChange={(e) => setForm({ ...form, [key]: e.target.value })}
                  className="bg-gray-800 border border-gray-700 text-white rounded-lg px-4 py-3 focus:outline-none focus:border-blue-500"
                />
              ))}
            </div>
            <div className="flex gap-3 mt-4">
              <button onClick={handleCreate} className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg transition">
                Save HCP
              </button>
              <button onClick={() => setShowForm(false)} className="bg-gray-700 hover:bg-gray-600 text-white px-6 py-2 rounded-lg transition">
                Cancel
              </button>
            </div>
          </div>
        )}

        {/* HCPs List */}
        {loading ? (
          <p className="text-gray-400">Loading...</p>
        ) : hcps.length === 0 ? (
          <div className="text-center py-20 text-gray-500">
            <div className="text-6xl mb-4">👨‍⚕️</div>
            <p className="text-xl">No HCPs yet — add your first one!</p>
          </div>
        ) : (
          <div className="grid grid-cols-2 gap-6">
            {hcps.map((hcp) => (
              <div key={hcp.id} className="bg-gray-900 border border-gray-800 rounded-xl p-6">
                <div className="flex justify-between items-start">
                  <div>
                    <h3 className="text-xl font-bold text-white">{hcp.name}</h3>
                    <p className="text-blue-400 text-sm mt-1">{hcp.specialization}</p>
                    <p className="text-gray-400 text-sm mt-2">🏥 {hcp.hospital}</p>
                    <p className="text-gray-400 text-sm">📍 {hcp.city}</p>
                    <p className="text-gray-400 text-sm">📧 {hcp.email}</p>
                    <p className="text-gray-400 text-sm">📞 {hcp.phone}</p>
                  </div>
                  <button
                    onClick={() => handleDelete(hcp.id)}
                    className="text-red-400 hover:text-red-300 text-sm transition"
                  >
                    🗑️ Delete
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}