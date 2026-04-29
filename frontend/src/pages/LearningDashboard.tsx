import { useState, useEffect } from 'react'
import { Brain, TrendingUp, Zap, Target, BookOpen, Clock, Award } from 'lucide-react'

interface LearningInsights {
  status: string
  learning_progress: number
  total_interactions: number
  top_topics: Array<{ topic: string; score: number }>
  interaction_patterns: Record<string, number>
  preferred_sources: Record<string, number>
  last_interaction: string
}

interface SessionSummary {
  session_id: string
  duration_minutes: number
  total_interactions: number
  total_queries: number
  papers_viewed: number
  unique_topics: string[]
  goals_achieved: {
    papers_explored: number
    topics_learned: number
    connections_made: number
  }
  learning_progress: number
}

function LearningDashboard() {
  const [insights, setInsights] = useState<LearningInsights | null>(null)
  const [sessionSummary, setSessionSummary] = useState<SessionSummary | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchLearningData()
  }, [])

  const fetchLearningData = async () => {
    try {
      // Get learning insights
      const insightsResponse = await fetch('/api/learning/learning/user123')
      const insightsData = await insightsResponse.json()
      setInsights(insightsData)

      // Get session summary (mock session ID for demo)
      const sessionResponse = await fetch('/api/learning/session/session_demo')
      const sessionData = await sessionResponse.json()
      setSessionSummary(sessionData)

    } catch (error) {
      console.error('Failed to fetch learning data:', error)
    } finally {
      setLoading(false)
    }
  }

  const trackInteraction = async (type: string, paperId: string) => {
    try {
      await fetch('/api/learning/interaction', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          user_id: 'user123',
          paper_id,
          interaction_type: type,
          metadata: { timestamp: new Date().toISOString() }
        })
      })
    } catch (error) {
      console.error('Failed to track interaction:', error)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <div className="border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center gap-2 mb-4">
            <Brain className="h-6 w-6 text-blue-600" />
            <span className="text-xl font-normal text-gray-700">Self-Learning Dashboard</span>
          </div>
        </div>
      </div>

      {/* Learning Progress Banner */}
      <div className="bg-gradient-to-r from-blue-50 to-purple-50 border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h2 className="text-lg font-normal text-gray-900 mb-1">
                Your Learning Progress
              </h2>
              <p className="text-sm text-gray-600">
                The system is learning your preferences and improving recommendations
              </p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-blue-600">
                {insights?.learning_progress ? Math.round(insights.learning_progress * 100) : 0}%
              </div>
              <div className="text-xs text-gray-500">Learning Complete</div>
            </div>
          </div>

          {/* Progress Bar */}
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-blue-600 h-2 rounded-full transition-all duration-500"
              style={{ width: `${insights?.learning_progress ? insights.learning_progress * 100 : 0}%` }}
            ></div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-4 gap-4 mt-6">
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {insights?.total_interactions || 0}
              </div>
              <div className="text-xs text-gray-500">Interactions</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {sessionSummary?.papers_viewed || 0}
              </div>
              <div className="text-xs text-gray-500">Papers Viewed</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {insights?.top_topics?.length || 0}
              </div>
              <div className="text-xs text-gray-500">Topics Learned</div>
            </div>
            <div className="text-center">
              <div className="text-2xl font-bold text-gray-900">
                {sessionSummary?.duration_minutes ? Math.round(sessionSummary.duration_minutes) : 0}
              </div>
              <div className="text-xs text-gray-500">Minutes Active</div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-4xl mx-auto px-4 py-6">
        {/* What the System Has Learned */}
        <div className="mb-8">
          <h3 className="text-lg font-normal text-gray-900 mb-4 flex items-center gap-2">
            <Brain className="h-5 w-5 text-blue-600" />
            What the System Has Learned About You
          </h3>

          <div className="grid grid-cols-2 gap-4">
            {/* Top Topics */}
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center gap-2">
                <Target className="h-4 w-4 text-blue-600" />
                Your Research Interests
              </h4>
              <div className="space-y-2">
                {insights?.top_topics?.slice(0, 5).map((topic, index) => (
                  <div key={index} className="flex items-center justify-between">
                    <span className="text-sm text-gray-700">{topic.topic}</span>
                    <div className="flex items-center gap-2">
                      <div className="w-20 bg-gray-200 rounded-full h-2">
                        <div
                          className="bg-blue-600 h-2 rounded-full"
                          style={{ width: `${topic.score * 100}%` }}
                        ></div>
                      </div>
                      <span className="text-xs text-gray-500">{Math.round(topic.score * 100)}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Interaction Patterns */}
            <div className="border border-gray-200 rounded-lg p-4">
              <h4 className="text-sm font-medium text-gray-900 mb-3 flex items-center gap-2">
                <TrendingUp className="h-4 w-4 text-blue-600" />
                Your Behavior Patterns
              </h4>
              <div className="space-y-2">
                {Object.entries(insights?.interaction_patterns || {}).map(([type, percentage]) => (
                  <div key={type} className="flex items-center justify-between">
                    <span className="text-sm text-gray-700 capitalize">{type}</span>
                    <span className="text-xs text-gray-500">{Math.round(percentage * 100)}%</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Session Goals */}
        <div className="mb-8">
          <h3 className="text-lg font-normal text-gray-900 mb-4 flex items-center gap-2">
            <Award className="h-5 w-5 text-blue-600" />
            Session Goals Achieved
          </h3>

          <div className="grid grid-cols-3 gap-4">
            <div className="border border-gray-200 rounded-lg p-4 text-center">
              <BookOpen className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">
                {sessionSummary?.goals_achieved?.papers_explored || 0}
              </div>
              <div className="text-xs text-gray-500">Papers Explored</div>
            </div>
            <div className="border border-gray-200 rounded-lg p-4 text-center">
              <Zap className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">
                {sessionSummary?.goals_achieved?.topics_learned || 0}
              </div>
              <div className="text-xs text-gray-500">Topics Learned</div>
            </div>
            <div className="border border-gray-200 rounded-lg p-4 text-center">
              <Clock className="h-8 w-8 text-blue-600 mx-auto mb-2" />
              <div className="text-2xl font-bold text-gray-900">
                {sessionSummary?.goals_achieved?.connections_made || 0}
              </div>
              <div className="text-xs text-gray-500">Connections Made</div>
            </div>
          </div>
        </div>

        {/* How It Works */}
        <div className="mb-8">
          <h3 className="text-lg font-normal text-gray-900 mb-4 flex items-center gap-2">
            <Zap className="h-5 w-5 text-blue-600" />
            How the Self-Learning System Works
          </h3>

          <div className="space-y-3">
            <div className="flex items-start gap-3 p-3 bg-blue-50 rounded-lg">
              <div className="bg-blue-600 text-white rounded-full p-1 mt-1">
                <span className="text-xs font-bold">1</span>
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-900">Track Your Interactions</h4>
                <p className="text-xs text-gray-600">Every click, save, and paper view teaches the system about your preferences</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 bg-purple-50 rounded-lg">
              <div className="bg-purple-600 text-white rounded-full p-1 mt-1">
                <span className="text-xs font-bold">2</span>
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-900">Build Your Interest Profile</h4>
                <p className="text-xs text-gray-600">The system identifies your research interests and expertise areas</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 bg-green-50 rounded-lg">
              <div className="bg-green-600 text-white rounded-full p-1 mt-1">
                <span className="text-xs font-bold">3</span>
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-900">Improve Recommendations</h4>
                <p className="text-xs text-gray-600">Results get more personalized as the system learns more about you</p>
              </div>
            </div>

            <div className="flex items-start gap-3 p-3 bg-orange-50 rounded-lg">
              <div className="bg-orange-600 text-white rounded-full p-1 mt-1">
                <span className="text-xs font-bold">4</span>
              </div>
              <div>
                <h4 className="text-sm font-medium text-gray-900">Remember Across Sessions</h4>
                <p className="text-xs text-gray-600">Your learning persists and improves every time you use the system</p>
              </div>
            </div>
          </div>
        </div>

        {/* Call to Action */}
        <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-lg p-6 text-white">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-medium mb-2">
                Continue Learning
              </h3>
              <p className="text-sm opacity-90">
                The more you interact, the smarter the system becomes
              </p>
            </div>
            <button
              onClick={() => window.location.href = '/'}
              className="px-4 py-2 bg-white text-blue-600 rounded-lg hover:bg-gray-100 text-sm font-medium"
            >
              Start Searching
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}

export default LearningDashboard
