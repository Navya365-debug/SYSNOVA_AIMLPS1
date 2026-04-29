"""
Advanced Self-Learning Personalization Engine
"""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import numpy as np
from collections import defaultdict
import json


class SelfLearningEngine:
    """
    Advanced personalization engine that learns from user behavior
    and continuously improves recommendations.
    """

    def __init__(self):
        """Initialize the self-learning engine."""
        self.user_profiles: Dict[str, Dict[str, Any]] = {}
        self.behavior_history: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
        self.topic_models: Dict[str, Dict[str, float]] = defaultdict(dict)
        self.interaction_weights = {
            'click': 0.2,
            'save': 0.5,
            'share': 0.3,
            'time_spent': 0.4,
            'scroll_depth': 0.3,
            'return_visit': 0.6,
        }

        # Learning parameters
        self.learning_rate = 0.1
        self.decay_factor = 0.95
        self.min_interactions_for_learning = 5

    def track_interaction(
        self,
        user_id: str,
        paper_id: str,
        interaction_type: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Track user interaction for learning.

        Args:
            user_id: User identifier
            paper_id: Paper identifier
            interaction_type: Type of interaction (click, save, share, etc.)
            metadata: Additional interaction metadata
        """
        interaction = {
            'paper_id': paper_id,
            'interaction_type': interaction_type,
            'timestamp': datetime.utcnow(),
            'metadata': metadata or {},
            'weight': self.interaction_weights.get(interaction_type, 0.1),
        }

        self.behavior_history[user_id].append(interaction)

        # Update user profile immediately
        self._update_user_profile(user_id, interaction)

        # Update topic models
        if metadata and 'topics' in metadata:
            self._update_topic_model(user_id, metadata['topics'], interaction['weight'])

    def _update_user_profile(self, user_id: str, interaction: Dict[str, Any]):
        """
        Update user profile based on interaction.

        Args:
            user_id: User identifier
            interaction: Interaction data
        """
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'total_interactions': 0,
                'interaction_weights': defaultdict(float),
                'preferred_sources': defaultdict(int),
                'preferred_topics': defaultdict(float),
                'active_hours': defaultdict(int),
                'session_count': 0,
                'last_interaction': None,
                'learning_progress': 0.0,
            }

        profile = self.user_profiles[user_id]
        profile['total_interactions'] += 1
        profile['interaction_weights'][interaction['interaction_type']] += interaction['weight']
        profile['last_interaction'] = interaction['timestamp']

        # Update learning progress
        if profile['total_interactions'] >= self.min_interactions_for_learning:
            profile['learning_progress'] = min(
                profile['total_interactions'] / 50.0,  # Cap at 50 interactions
                1.0
            )

    def _update_topic_model(self, user_id: str, topics: List[str], weight: float):
        """
        Update topic model for user.

        Args:
            user_id: User identifier
            topics: List of topics
            weight: Interaction weight
        """
        for topic in topics:
            # Apply learning rate and decay
            current_score = self.topic_models[user_id].get(topic, 0.0)
            new_score = current_score * self.decay_factor + weight * self.learning_rate
            self.topic_models[user_id][topic] = new_score

    def get_personalized_ranking(
        self,
        user_id: str,
        papers: List[Dict[str, Any]]
    ) -> List[Tuple[Dict[str, Any], float]]:
        """
        Get personalized ranking of papers for user.

        Args:
            user_id: User identifier
            papers: List of papers to rank

        Returns:
            List of (paper, score) tuples sorted by score
        """
        if user_id not in self.user_profiles:
            # No profile yet, return default ranking
            return [(paper, 0.5) for paper in papers]

        profile = self.user_profiles[user_id]
        topic_model = self.topic_models[user_id]

        scored_papers = []

        for paper in papers:
            score = self._calculate_paper_score(paper, profile, topic_model)
            scored_papers.append((paper, score))

        # Sort by score (descending)
        scored_papers.sort(key=lambda x: x[1], reverse=True)

        return scored_papers

    def _calculate_paper_score(
        self,
        paper: Dict[str, Any],
        profile: Dict[str, Any],
        topic_model: Dict[str, float]
    ) -> float:
        """
        Calculate personalized score for a paper.

        Args:
            paper: Paper data
            profile: User profile
            topic_model: User's topic model

        Returns:
            Personalized score (0-1)
        """
        base_score = 0.5  # Default score

        # Topic relevance
        paper_topics = self._extract_topics(paper)
        topic_score = 0.0

        for topic in paper_topics:
            if topic in topic_model:
                topic_score += topic_model[topic]

        if paper_topics:
            topic_score /= len(paper_topics)  # Normalize

        # Source preference
        source = paper.get('source', '')
        source_preference = profile['preferred_sources'].get(source, 0)
        source_score = min(source_preference / max(profile['preferred_sources'].values(), 1), 1.0)

        # Recency preference (if user prefers recent papers)
        recency_score = self._calculate_recency_score(paper, profile)

        # Citation count preference
        citation_score = self._calculate_citation_score(paper, profile)

        # Combine scores with learning progress
        learning_progress = profile['learning_progress']
        final_score = (
            base_score * (1 - learning_progress) +
            (topic_score * 0.4 + source_score * 0.2 + recency_score * 0.2 + citation_score * 0.2) * learning_progress
        )

        return min(final_score, 1.0)

    def _extract_topics(self, paper: Dict[str, Any]) -> List[str]:
        """
        Extract topics from paper.

        Args:
            paper: Paper data

        Returns:
            List of topics
        """
        topics = []

        # From metadata
        metadata = paper.get('metadata', {})
        if 'topics' in metadata:
            topics.extend(metadata['topics'])
        if 'categories' in metadata:
            topics.extend(metadata['categories'])

        # From title and abstract
        title = paper.get('title', '').lower()
        abstract = paper.get('abstract', '').lower()

        # Common ML/AI topics
        common_topics = [
            'machine learning', 'deep learning', 'neural networks',
            'natural language processing', 'computer vision',
            'reinforcement learning', 'transformer', 'attention',
            'graph neural networks', 'federated learning',
            'convolutional neural networks', 'recurrent neural networks',
            'generative adversarial networks', 'autoencoder',
            'transfer learning', 'few-shot learning', 'meta learning',
            'self-supervised learning', 'unsupervised learning',
            'supervised learning', 'semi-supervised learning',
        ]

        for topic in common_topics:
            if topic in title or topic in abstract:
                topics.append(topic)

        return list(set(topics))

    def _calculate_recency_score(self, paper: Dict[str, Any], profile: Dict[str, Any]) -> float:
        """
        Calculate recency score based on user preferences.

        Args:
            paper: Paper data
            profile: User profile

        Returns:
            Recency score (0-1)
        """
        # Check if user prefers recent papers
        recent_papers = sum(
            1 for interaction in self.behavior_history.get(profile.get('user_id', ''), [])
            if interaction.get('metadata', {}).get('is_recent', False)
        )

        if recent_papers < 3:
            return 0.5  # No strong preference

        published_date = paper.get('published_date')
        if not published_date:
            return 0.5

        try:
            pub_date = datetime.strptime(published_date, '%Y-%m-%d')
            days_old = (datetime.utcnow() - pub_date).days

            # Prefer papers from last 2 years
            if days_old < 730:
                return 1.0 - (days_old / 730) * 0.5
            else:
                return 0.5
        except:
            return 0.5

    def _calculate_citation_score(self, paper: Dict[str, Any], profile: Dict[str, Any]) -> float:
        """
        Calculate citation score based on user preferences.

        Args:
            paper: Paper data
            profile: User profile

        Returns:
            Citation score (0-1)
        """
        citation_count = paper.get('citation_count', 0)

        if citation_count == 0:
            return 0.5

        # Normalize citation count (log scale)
        import math
        normalized_citations = math.log10(citation_count + 1) / 4.0  # Assume max ~10k citations

        return min(normalized_citations, 1.0)

    def get_learning_insights(self, user_id: str) -> Dict[str, Any]:
        """
        Get insights about what the system has learned about the user.

        Args:
            user_id: User identifier

        Returns:
            Dictionary of learning insights
        """
        if user_id not in self.user_profiles:
            return {
                'status': 'no_profile',
                'message': 'Start interacting with papers to begin learning',
            }

        profile = self.user_profiles[user_id]
        topic_model = self.topic_models[user_id]

        # Get top topics
        top_topics = sorted(
            topic_model.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

        # Get interaction patterns
        interaction_patterns = {
            interaction_type: count / profile['total_interactions']
            for interaction_type, count in profile['interaction_weights'].items()
        }

        return {
            'status': 'learning',
            'learning_progress': profile['learning_progress'],
            'total_interactions': profile['total_interactions'],
            'top_topics': [{'topic': topic, 'score': score} for topic, score in top_topics],
            'interaction_patterns': interaction_patterns,
            'preferred_sources': dict(profile['preferred_sources']),
            'last_interaction': profile['last_interaction'].isoformat() if profile['last_interaction'] else None,
        }

    def get_adaptive_recommendations(
        self,
        user_id: str,
        num_recommendations: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get adaptive recommendations based on learned preferences.

        Args:
            user_id: User identifier
            num_recommendations: Number of recommendations

        Returns:
            List of recommended papers with explanations
        """
        if user_id not in self.user_profiles:
            return []

        profile = self.user_profiles[user_id]
        topic_model = self.topic_models[user_id]

        # Get top topics
        top_topics = sorted(
            topic_model.items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]

        recommendations = []

        for i, (topic, score) in enumerate(top_topics):
            recommendations.append({
                'id': f'rec_{i}',
                'topic': topic,
                'reason': f'Based on your interest in {topic}',
                'confidence': score,
                'learning_source': 'behavior_analysis',
            })

        return recommendations[:num_recommendations]

    def save_learning_state(self, filepath: str):
        """
        Save learning state to disk.

        Args:
            filepath: Path to save learning state
        """
        state = {
            'user_profiles': {
                user_id: {
                    **profile,
                    'interaction_weights': dict(profile['interaction_weights']),
                    'preferred_sources': dict(profile['preferred_sources']),
                    'preferred_topics': dict(profile['preferred_topics']),
                    'active_hours': dict(profile['active_hours']),
                }
                for user_id, profile in self.user_profiles.items()
            },
            'topic_models': dict(self.topic_models),
            'behavior_history': {
                user_id: [
                    {
                        **interaction,
                        'timestamp': interaction['timestamp'].isoformat(),
                    }
                    for interaction in interactions
                ]
                for user_id, interactions in self.behavior_history.items()
            },
        }

        with open(filepath, 'w') as f:
            json.dump(state, f, indent=2)

    def load_learning_state(self, filepath: str):
        """
        Load learning state from disk.

        Args:
            filepath: Path to load learning state from
        """
        try:
            with open(filepath, 'r') as f:
                state = json.load(f)

            # Restore user profiles
            for user_id, profile_data in state['user_profiles'].items():
                self.user_profiles[user_id] = {
                    **profile_data,
                    'interaction_weights': defaultdict(float, profile_data['interaction_weights']),
                    'preferred_sources': defaultdict(int, profile_data['preferred_sources']),
                    'preferred_topics': defaultdict(float, profile_data['preferred_topics']),
                    'active_hours': defaultdict(int, profile_data['active_hours']),
                    'last_interaction': datetime.fromisoformat(profile_data['last_interaction']) if profile_data.get('last_interaction') else None,
                }

            # Restore topic models
            self.topic_models = defaultdict(dict, state['topic_models'])

            # Restore behavior history
            for user_id, interactions_data in state['behavior_history'].items():
                self.behavior_history[user_id] = [
                    {
                        **interaction,
                        'timestamp': datetime.fromisoformat(interaction['timestamp']),
                    }
                    for interaction in interactions_data
                ]

        except Exception as e:
            print(f"Error loading learning state: {e}")


# Example usage
if __name__ == "__main__":
    engine = SelfLearningEngine()

    # Simulate user learning
    user_id = "user123"

    # Track interactions
    engine.track_interaction(
        user_id,
        "paper1",
        "click",
        {"topics": ["machine learning", "deep learning"], "is_recent": True}
    )

    engine.track_interaction(
        user_id,
        "paper2",
        "save",
        {"topics": ["natural language processing", "transformer"], "is_recent": True}
    )

    engine.track_interaction(
        user_id,
        "paper3",
        "click",
        {"topics": ["machine learning", "neural networks"], "is_recent": False}
    )

    # Get learning insights
    insights = engine.get_learning_insights(user_id)
    print("Learning Insights:")
    print(json.dumps(insights, indent=2, default=str))

    # Get adaptive recommendations
    recommendations = engine.get_adaptive_recommendations(user_id)
    print("\nAdaptive Recommendations:")
    for rec in recommendations:
        print(f"  - {rec['topic']}: {rec['reason']} (confidence: {rec['confidence']:.2f})")
