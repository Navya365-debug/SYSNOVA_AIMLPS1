import { Link } from 'react-router-dom'
import { FileText, Network, User, Brain, Search } from 'lucide-react'

function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
      <div className="max-w-6xl mx-auto px-4">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center space-x-2 group">
            <div className="bg-blue-600 rounded-lg p-2 group-hover:bg-blue-700 transition-colors">
              <FileText className="h-5 w-5 text-white" />
            </div>
            <span className="text-lg font-semibold text-gray-800">NeuroQuest</span>
          </Link>

          <div className="flex items-center space-x-1">
            <Link
              to="/"
              className="flex items-center space-x-1 px-3 py-2 rounded-lg text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-colors"
            >
              <Search className="h-4 w-4" />
              <span>Search</span>
            </Link>
            <Link
              to="/learning"
              className="flex items-center space-x-1 px-3 py-2 rounded-lg text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-colors"
            >
              <Brain className="h-4 w-4" />
              <span>Learning</span>
            </Link>
            <Link
              to="/graph"
              className="flex items-center space-x-1 px-3 py-2 rounded-lg text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-colors"
            >
              <Network className="h-4 w-4" />
              <span>Knowledge Graph</span>
            </Link>
            <Link
              to="/profile"
              className="flex items-center space-x-1 px-3 py-2 rounded-lg text-sm font-medium text-gray-700 hover:text-blue-600 hover:bg-blue-50 transition-colors"
            >
              <User className="h-4 w-4" />
              <span>My Library</span>
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
