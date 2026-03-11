import { Routes, Route, Navigate } from 'react-router-dom'
import { useSelector } from 'react-redux'
import Login from './pages/Login'
import Dashboard from './pages/Dashboard'
import HCPs from './pages/HCPs'
import Interactions from './pages/Interactions'
import AIChat from './pages/AIChat'

// Protected route — agar login nahi hai toh Login pe bhejo
function ProtectedRoute({ children }) {
  const { token } = useSelector((state) => state.auth)
  return token ? children : <Navigate to="/login" />
}

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={
        <ProtectedRoute><Dashboard /></ProtectedRoute>
      } />
      <Route path="/hcps" element={
        <ProtectedRoute><HCPs /></ProtectedRoute>
      } />
      <Route path="/interactions" element={
        <ProtectedRoute><Interactions /></ProtectedRoute>
      } />
      <Route path="/chat" element={
        <ProtectedRoute><AIChat /></ProtectedRoute>
      } />
      <Route path="*" element={<Navigate to="/login" />} />
    </Routes>
  )
}