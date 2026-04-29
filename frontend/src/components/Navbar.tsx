import { Link } from 'react-router-dom'
import { FileText, Network, User, Brain } from 'lucide-react'

function Navbar() {
  return (
    <nav className="bg-white border-b border-gray-200">
      <div className="max-w-4xl mx-auto px-4">
        <div className="flex items-center justify-between h-14">
          <Link to="/" className="flex items-center space-x-2">
            <FileText className="h-6 w-6 text-blue-600" />
            <span className="text-lg font-normal text-gray-700">NeuroQuest</span>
          </Link>

          <div className="flex items-center space-x-6 text-sm">
            <Link
              to="/"
              className="text-gray-700 hover:text-blue-600 transition-colors"
            >
              Search
            </Link>
            <Link
              to="/learning"
              className="text-gray-700 hover:text-blue-600 transition-colors"
            >
              Learning
            </Link>
            <Link
              to="/graph"
              className="text-gray-700 hover:text-blue-600 transition-colors"
            >
              Knowledge Graph
            </Link>
            <Link
              to="/profile"
              className="text-gray-700 hover:text-blue-600 transition-colors"
            >
              My Library
            </Link>
          </div>
        </div>
      </div>
    </nav>
  )
}

export default Navbar
