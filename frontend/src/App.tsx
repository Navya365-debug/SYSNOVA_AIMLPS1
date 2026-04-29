import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom'
import SearchPage from './pages/SearchPage'
import ProfilePage from './pages/ProfilePage'
import KnowledgeGraphPage from './pages/KnowledgeGraphPage'
import LearningDashboard from './pages/LearningDashboard'
import Navbar from './components/Navbar'

function AppContent() {
  const location = useLocation()
  const showNavbar = location.pathname !== '/'

  return (
    <div className="min-h-screen bg-white">
      {showNavbar && <Navbar />}
      <main>
        <Routes>
          <Route path="/" element={<SearchPage />} />
          <Route path="/profile" element={<ProfilePage />} />
          <Route path="/graph" element={<KnowledgeGraphPage />} />
          <Route path="/learning" element={<LearningDashboard />} />
        </Routes>
      </main>
    </div>
  )
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  )
}

export default App
