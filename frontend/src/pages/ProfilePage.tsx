import { useState, useEffect } from 'react'
import { User, Settings, Shield, TrendingUp, Clock, FileText } from 'lucide-react'

interface UserProfile {
  user_id: string
  name?: string
  email?: string
  research_interests: string[]
  preferences: Record<string, any>
  created_at: string
  updated_at: string
}

function ProfilePage() {
  const [profile, setProfile] = useState<UserProfile | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      const response = await fetch('/api/user/profile?user_id=demo_user')
      const data = await response.json()
      setProfile(data)
    } catch (error) {
      console.error('Failed to fetch profile:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center py-12">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  if (!profile) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Failed to load profile</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <div className="border-b border-gray-200">
        <div className="max-w-4xl mx-auto px-4 py-4">
          <div className="flex items-center gap-2 mb-4">
            <FileText className="h-6 w-6 text-blue-600" />
            <span className="text-xl font-normal text-gray-700">My Library</span>
          </div>

          {/* Tabs */}
          <div className="flex gap-6 text-sm border-b border-gray-200">
            <button className="pb-2 border-b-2 border-blue-600 text-blue-600">
              My Profile
            </button>
            <button className="pb-2 text-gray-600 hover:text-blue-600">
              My Articles
            </button>
            <button className="pb-2 text-gray-600 hover:text-blue-600">
              My Citations
            </button>
            <button className="pb-2 text-gray-600 hover:text-blue-600">
              Alerts
            </button>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-4 py-6">
        {/* User Info */}
        <div className="mb-8">
          <div className="flex items-start gap-4 mb-4">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center">
              <User className="h-8 w-8 text-blue-600" />
            </div>
            <div className="flex-1">
              <h1 className="text-xl font-normal text-gray-900 mb-1">
                {profile.name || 'Demo User'}
              </h1>
              <p className="text-sm text-gray-600 mb-2">
                {profile.email || 'demo@example.com'}
              </p>
              <div className="text-sm text-gray-500">
                <span className="flex items-center gap-1">
                  <Clock className="h-4 w-4" />
                  Joined {new Date(profile.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>
          </div>
        </div>

        {/* Research Interests */}
        <div className="mb-8">
          <h2 className="text-lg font-normal text-gray-900 mb-3">Research Interests</h2>
          <div className="flex flex-wrap gap-2">
            {profile.research_interests.map((interest, index) => (
              <span
                key={index}
                className="px-3 py-1 bg-blue-50 text-blue-700 rounded text-sm border border-blue-200"
              >
                {interest}
              </span>
            ))}
            {profile.research_interests.length === 0 && (
              <p className="text-sm text-gray-500">No interests set yet</p>
            )}
          </div>
        </div>

        {/* Preferences */}
        <div className="mb-8">
          <h2 className="text-lg font-normal text-gray-900 mb-3">Preferences</h2>
          <div className="space-y-2">
            {Object.entries(profile.preferences).map(([key, value]) => (
              <div key={key} className="flex justify-between items-center py-2 border-b border-gray-100">
                <span className="text-sm text-gray-700 capitalize">
                  {key.replace(/_/g, ' ')}
                </span>
                <span className="text-sm text-gray-900">
                  {String(value)}
                </span>
              </div>
            ))}
            {Object.keys(profile.preferences).length === 0 && (
              <p className="text-sm text-gray-500">No preferences set yet</p>
            )}
          </div>
        </div>

        {/* Privacy Settings */}
        <div className="mb-8">
          <h2 className="text-lg font-normal text-gray-900 mb-3">Privacy & Security</h2>
          <div className="space-y-3">
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <div>
                <p className="text-sm text-gray-900">Data Encryption</p>
                <p className="text-xs text-gray-500">
                  Your data is encrypted at rest
                </p>
              </div>
              <span className="text-xs text-green-700 bg-green-50 px-2 py-1 rounded">
                Enabled
              </span>
            </div>
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <div>
                <p className="text-sm text-gray-900">Personalization</p>
                <p className="text-xs text-gray-500">
                  Improve results based on your behavior
                </p>
              </div>
              <span className="text-xs text-green-700 bg-green-50 px-2 py-1 rounded">
                Enabled
              </span>
            </div>
            <div className="flex items-center justify-between py-2 border-b border-gray-100">
              <div>
                <p className="text-sm text-gray-900">Analytics</p>
                <p className="text-xs text-gray-500">
                  Anonymous usage analytics
                </p>
              </div>
              <span className="text-xs text-green-700 bg-green-50 px-2 py-1 rounded">
                Enabled
              </span>
            </div>
          </div>
        </div>

        {/* Actions */}
        <div className="flex gap-4">
          <button className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm">
            Edit Profile
          </button>
          <button className="px-4 py-2 border border-gray-300 text-gray-700 rounded hover:bg-gray-50 text-sm">
            Export Data
          </button>
        </div>
      </div>
    </div>
  )
}

export default ProfilePage
