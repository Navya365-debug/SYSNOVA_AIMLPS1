export interface SearchResult {
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
  personalization_score?: number
  final_score?: number
}

export interface UserProfile {
  user_id: string
  name?: string
  email?: string
  research_interests: string[]
  preferences: Record<string, any>
  created_at: string
  updated_at: string
}

export interface UserBehavior {
  user_id: string
  action: string
  paper_id: string
  timestamp: string
  metadata?: Record<string, any>
}

export interface GraphNode {
  id: string
  label: string
  type: string
  properties?: Record<string, any>
  weight: number
}

export interface GraphEdge {
  source: string
  target: string
  relationship: string
  weight: number
  properties?: Record<string, any>
}

export interface KnowledgeGraph {
  nodes: GraphNode[]
  edges: GraphEdge[]
  metadata?: Record<string, any>
}
