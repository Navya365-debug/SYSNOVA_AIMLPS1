import { useState } from 'react'
import { Search, ExternalLink, Bookmark, Star, FileText } from 'lucide-react'

interface SearchResult {
  id: string
  title: string
  authors: string[]
  abstract: string
  source: string
  url: string
  published_date?: string
  relevance_score: number
  citation_count?: number
  metadata?: Record<string, any>
}

function SearchPage() {
  const [query, setQuery] = useState('')
  const [results, setResults] = useState<SearchResult[]>([])
  const [loading, setLoading] = useState(false)
  const [usePersonalization, setUsePersonalization] = useState(true)
  const [userId] = useState('user123') // In production, get from auth

  const trackInteraction = async (type: string, paperId: string, metadata?: Record<string, any>) => {
    try {
      await fetch('/api/learning/interaction', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: userId,
          paper_id: paperId,
          interaction_type: type,
          metadata: {
            timestamp: new Date().toISOString(),
            ...metadata
          }
        })
      })
    } catch (error) {
      console.error('Failed to track interaction:', error)
    }
  }

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!query.trim()) return

    setLoading(true)
    try {
      const response = await fetch('/api/search/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query,
          sources: ['arxiv', 'pubmed', 'scholar'],
          max_results: 10,
          use_personalization: usePersonalization,
        }),
      })

      const data = await response.json()
      setResults(data.results || [])

      // Track search query
      if (data.results && data.results.length > 0) {
        await trackInteraction('search', 'search_query', {
          query,
          results_count: data.results.length,
          topics: data.results.map((r: SearchResult) => r.metadata?.topics || []).flat()
        })
      }
    } catch (error) {
      console.error('Search failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const handlePaperClick = async (paperId: string, paper: SearchResult) => {
    await trackInteraction('click', paperId, {
      title: paper.title,
      source: paper.source,
      topics: paper.metadata?.topics || []
    })
  }

  const handleSavePaper = async (paperId: string, paper: SearchResult) => {
    await trackInteraction('save', paperId, {
      title: paper.title,
      source: paper.source,
      topics: paper.metadata?.topics || []
    })
  }

  const getSourceLabel = (source: string) => {
    switch (source) {
      case 'arxiv':
        return '[arXiv]'
      case 'pubmed':
        return '[PubMed]'
      case 'scholar':
        return '[PDF]'
      default:
        return `[${source}]`
    }
  }

  const getSourceColor = (source: string) => {
    switch (source) {
      case 'arxiv':
        return 'text-orange-600'
      case 'pubmed':
        return 'text-blue-600'
      case 'scholar':
        return 'text-green-600'
      default:
        return 'text-gray-600'
    }
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <div className="border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center gap-4 mb-4">
            <div className="flex items-center gap-2">
              <FileText className="h-6 w-6 text-blue-600" />
              <span className="text-xl font-normal text-gray-700">NeuroQuest</span>
            </div>
            <div className="flex-1"></div>
            <div className="text-sm text-gray-600">
              <a href="#" className="text-blue-600 hover:underline">My Library</a>
              <span className="mx-2">|</span>
              <a href="#" className="text-blue-600 hover:underline">My Alerts</a>
            </div>
          </div>

          {/* Search Bar */}
          <form onSubmit={handleSearch} className="relative">
            <div className="flex items-center border border-gray-300 rounded-full hover:shadow-md transition-shadow">
              <div className="flex-1 flex items-center">
                <Search className="h-5 w-5 text-gray-400 ml-4" />
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search for research papers..."
                  className="flex-1 px-4 py-3 outline-none text-gray-700"
                />
              </div>
              <button
                type="submit"
                disabled={loading}
                className="px-6 py-3 bg-blue-600 text-white rounded-r-full hover:bg-blue-700 disabled:bg-gray-400 transition-colors"
              >
                {loading ? (
                  <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                ) : (
                  'Search'
                )}
              </button>
            </div>
          </form>

          {/* Search Options */}
          <div className="flex items-center gap-4 mt-3 text-sm text-gray-600">
            <label className="flex items-center gap-2 cursor-pointer">
              <input
                type="checkbox"
                checked={usePersonalization}
                onChange={(e) => setUsePersonalization(e.target.checked)}
                className="rounded"
              />
              <span>Personalized results</span>
            </label>
            <a href="#" className="text-blue-600 hover:underline">Advanced search</a>
          </div>
        </div>
      </div>

      {/* Results */}
      <div className="max-w-4xl mx-auto px-4 py-6">
        {results.length > 0 && (
          <div className="text-sm text-gray-600 mb-4">
            About {results.length} results ({(0.3).toFixed(2)} seconds)
          </div>
        )}

        {results.map((result, index) => (
          <div key={result.id} className="mb-8">
            {/* Title */}
            <h3 className="text-xl mb-1">
              <a
                href={result.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-800 hover:underline visited:text-purple-800"
                onClick={() => handlePaperClick(result.id, result)}
              >
                {result.title}
              </a>
            </h3>

            {/* Authors and Source */}
            <div className="text-sm text-gray-700 mb-1">
              <span className="text-green-700">{result.authors.join(', ')}</span>
              <span className="text-gray-500"> - </span>
              <span className="text-gray-600">
                {result.metadata?.journal || result.metadata?.venue || 'Unknown Venue'}
                {result.published_date && `, ${new Date(result.published_date).getFullYear()}`}
              </span>
              <span className="text-gray-500"> - </span>
              <span className={getSourceColor(result.source)}>
                {getSourceLabel(result.source)}
              </span>
            </div>

            {/* Abstract */}
            <p className="text-sm text-gray-800 mb-2 leading-relaxed">
              {result.abstract}
            </p>

            {/* Citations and Links */}
            <div className="text-sm">
              {result.citation_count !== undefined && result.citation_count > 0 && (
                <span className="text-green-700 mr-4">
                  Cited by {result.citation_count}
                </span>
              )}
              <a
                href={result.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline mr-4"
              >
                [HTML]
              </a>
              <a
                href={result.url}
                target="_blank"
                rel="noopener noreferrer"
                className="text-blue-600 hover:underline mr-4"
              >
                [PDF]
              </a>
              <button className="text-blue-600 hover:underline mr-4">
                Cite
              </button>
              <button
                className="text-blue-600 hover:underline"
                onClick={() => handleSavePaper(result.id, result)}
              >
                <Bookmark className="h-4 w-4 inline" /> Save
              </button>
            </div>

            {/* Related */}
            <div className="text-sm text-gray-600 mt-1">
              <span className="text-blue-600 hover:underline cursor-pointer">
                Related articles
              </span>
              <span className="text-gray-500">, </span>
              <span className="text-blue-600 hover:underline cursor-pointer">
                All {result.citation_count || 0} versions
              </span>
            </div>
          </div>
        ))}

        {results.length === 0 && query && !loading && (
          <div className="text-center py-12">
            <p className="text-gray-600">No results found for "{query}"</p>
            <p className="text-sm text-gray-500 mt-2">
              Try different keywords or check your spelling
            </p>
          </div>
        )}

        {results.length === 0 && !query && (
          <div className="text-center py-12">
            <FileText className="h-16 w-16 text-gray-300 mx-auto mb-4" />
            <h2 className="text-xl font-normal text-gray-700 mb-2">
              NeuroQuest AI Research Assistant
            </h2>
            <p className="text-gray-600">
              Search across arXiv, PubMed, and Google Scholar with AI-powered insights
            </p>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="border-t border-gray-200 mt-12">
        <div className="max-w-4xl mx-auto px-4 py-4 text-sm text-gray-600">
          <div className="flex justify-between items-center">
            <div>
              <a href="#" className="text-blue-600 hover:underline mr-4">About</a>
              <a href="#" className="text-blue-600 hover:underline mr-4">Privacy</a>
              <a href="#" className="text-blue-600 hover:underline">Terms</a>
            </div>
            <div className="text-gray-500">
              Powered by NVIDIA NIM AI
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SearchPage
