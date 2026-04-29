import { useState, useEffect, useRef } from 'react'
import { Network, Search, ZoomIn, ZoomOut, RefreshCw } from 'lucide-react'

interface GraphNode {
  id: string
  label: string
  type: string
  properties?: Record<string, any>
  weight: number
}

interface GraphEdge {
  source: string
  target: string
  relationship: string
  weight: number
  properties?: Record<string, any>
}

interface KnowledgeGraph {
  nodes: GraphNode[]
  edges: GraphEdge[]
  metadata?: Record<string, any>
}

function KnowledgeGraphPage() {
  const [graph, setGraph] = useState<KnowledgeGraph | null>(null)
  const [loading, setLoading] = useState(true)
  const [query, setQuery] = useState('')
  const [zoom, setZoom] = useState(1)
  const svgRef = useRef<SVGSVGElement>(null)

  useEffect(() => {
    fetchGraph()
  }, [])

  const fetchGraph = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/graph/explore', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: query || 'machine learning',
          max_nodes: 50,
          max_depth: 3,
        }),
      })

      const data = await response.json()
      setGraph(data)
    } catch (error) {
      console.error('Failed to fetch graph:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e: React.FormEvent) => {
    e.preventDefault()
    fetchGraph()
  }

  const getNodeColor = (type: string) => {
    switch (type) {
      case 'concept':
        return '#0ea5e9'
      case 'paper':
        return '#f59e0b'
      case 'author':
        return '#10b981'
      case 'topic':
        return '#8b5cf6'
      default:
        return '#6b7280'
    }
  }

  const handleZoomIn = () => {
    setZoom((prev) => Math.min(prev + 0.2, 3))
  }

  const handleZoomOut = () => {
    setZoom((prev) => Math.max(prev - 0.2, 0.5))
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="max-w-6xl mx-auto">
      <div className="mb-8">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">
          Knowledge Graph
        </h1>
        <p className="text-gray-600">
          Explore relationships between concepts, papers, and authors
        </p>
      </div>

      <div className="mb-6">
        <form onSubmit={handleSearch} className="flex gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-gray-400 h-5 w-5" />
            <input
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search the knowledge graph..."
              className="w-full pl-10 pr-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            />
          </div>
          <button
            type="submit"
            className="px-6 py-3 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors flex items-center gap-2"
          >
            <Network className="h-5 w-5" />
            Explore
          </button>
          <button
            type="button"
            onClick={fetchGraph}
            className="px-4 py-3 bg-gray-200 text-gray-700 rounded-lg hover:bg-gray-300 transition-colors"
          >
            <RefreshCw className="h-5 w-5" />
          </button>
        </form>
      </div>

      <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600">
              {graph?.nodes.length || 0} nodes
            </span>
            <span className="text-sm text-gray-600">
              {graph?.edges.length || 0} edges
            </span>
          </div>
          <div className="flex items-center gap-2">
            <button
              onClick={handleZoomOut}
              className="p-2 text-gray-500 hover:text-gray-700 transition-colors"
            >
              <ZoomOut className="h-5 w-5" />
            </button>
            <span className="text-sm text-gray-600 w-12 text-center">
              {Math.round(zoom * 100)}%
            </span>
            <button
              onClick={handleZoomIn}
              className="p-2 text-gray-500 hover:text-gray-700 transition-colors"
            >
              <ZoomIn className="h-5 w-5" />
            </button>
          </div>
        </div>

        <div className="border border-gray-200 rounded-lg overflow-hidden" style={{ height: '500px' }}>
          <svg
            ref={svgRef}
            className="w-full h-full bg-gray-50"
            viewBox="0 0 800 600"
          >
            <g transform={`scale(${zoom})`}>
              {/* Draw edges */}
              {graph?.edges.map((edge, index) => {
                const sourceNode = graph.nodes.find((n) => n.id === edge.source)
                const targetNode = graph.nodes.find((n) => n.id === edge.target)
                if (!sourceNode || !targetNode) return null

                // Simple positioning - in production, use proper graph layout
                const sourceX = (parseInt(sourceNode.id.split('_')[1] || '0') % 10) * 80 + 50
                const sourceY = Math.floor(parseInt(sourceNode.id.split('_')[1] || '0') / 10) * 80 + 50
                const targetX = (parseInt(targetNode.id.split('_')[1] || '0') % 10) * 80 + 50
                const targetY = Math.floor(parseInt(targetNode.id.split('_')[1] || '0') / 10) * 80 + 50

                return (
                  <line
                    key={index}
                    x1={sourceX}
                    y1={sourceY}
                    x2={targetX}
                    y2={targetY}
                    stroke="#9ca3af"
                    strokeWidth={edge.weight * 2}
                    opacity={0.6}
                  />
                )
              })}

              {/* Draw nodes */}
              {graph?.nodes.map((node) => {
                const x = (parseInt(node.id.split('_')[1] || '0') % 10) * 80 + 50
                const y = Math.floor(parseInt(node.id.split('_')[1] || '0') / 10) * 80 + 50
                const radius = 20 + node.weight * 10

                return (
                  <g key={node.id}>
                    <circle
                      cx={x}
                      cy={y}
                      r={radius}
                      fill={getNodeColor(node.type)}
                      opacity={0.8}
                      className="cursor-pointer hover:opacity-100 transition-opacity"
                    />
                    <text
                      x={x}
                      y={y + radius + 15}
                      textAnchor="middle"
                      className="text-xs fill-gray-700"
                    >
                      {node.label}
                    </text>
                  </g>
                )
              })}
            </g>
          </svg>
        </div>

        {/* Legend */}
        <div className="mt-4 flex flex-wrap gap-4">
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-sky-500"></div>
            <span className="text-sm text-gray-600">Concept</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-amber-500"></div>
            <span className="text-sm text-gray-600">Paper</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-emerald-500"></div>
            <span className="text-sm text-gray-600">Author</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-4 h-4 rounded-full bg-violet-500"></div>
            <span className="text-sm text-gray-600">Topic</span>
          </div>
        </div>
      </div>
    </div>
  )
}

export default KnowledgeGraphPage
