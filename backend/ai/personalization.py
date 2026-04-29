"""
Behavior-Driven Personalization Engine
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import numpy as np


class PersonalizationEngine:
    """Engine for personalizing search results based on user behavior."""

    def __init__(self):
        """Initialize the personalization engine."""
        self.user_profiles: Dict[str, Dict[str, Any]] = {}
        self.behavior_weights = {
            'click': 0.3,
            'save': 0.5,
            'share': 0.2,
            'time_spent': 0.4,
        }

    def update_user_profile(
        self,
        user_id: str,
        behavior: str,
        paper_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Update user profile based on behavior.

        Args:
            user_id: User identifier
            behavior: Type of behavior (click, save, share, etc.)
            paper_id: Paper identifier
            metadata: Additional metadata
        """
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = {
                'interactions': [],
                'interests': {},
                'last_updated': datetime.utcnow(),
            }

        profile = self.user_profiles[user_id]

        # Record interaction
        interaction = {
            'behavior': behavior,
            'paper_id': paper_id,
            'timestamp': datetime.utcnow(),
            'metadata': metadata or {},
        }
        profile['interactions'].append(interaction)

        # Update interests based on paper metadata
        if metadata and 'topics' in metadata:
            for topic in metadata['topics']:
                if topic not in profile['interests']:
                    profile['interests'][topic] = 0
                profile['interests'][topic] += self.behavior_weights.get(behavior, 0.1)

        profile['last_updated'] = datetime.utcnow()

    def get_user_profile(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user profile.

        Args:
            user_id: User identifier

        Returns:
            User profile or None
        """
        return self.user_profiles.get(user_id)

    def get_user_interests(
        self,
        user_id: str,
        top_n: int = 10
    ) -> List[tuple]:
        """
        Get top user interests.

        Args:
            user_id: User identifier
            top_n: Number of top interests to return

        Returns:
            List of (interest, score) tuples
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            return []

        interests = profile.get('interests', {})
        sorted_interests = sorted(
            interests.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_interests[:top_n]

    def personalize_results(
        self,
        user_id: str,
        results: List[Dict[str, Any]],
        query: str
    ) -> List[Dict[str, Any]]:
        """
        Personalize search results for a user.

        Args:
            user_id: User identifier
            results: List of search results
            query: Original search query

        Returns:
            Personalized search results
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            # No profile yet, return results as-is
            for result in results:
                result['personalization_score'] = 0.5
            return results

        # Get user interests
        interests = self.get_user_interests(user_id, top_n=20)
        interest_topics = {topic for topic, _ in interests}

        # Calculate personalization scores
        for result in results:
            personalization_score = self._calculate_personalization_score(
                result,
                interests,
                query
            )
            result['personalization_score'] = personalization_score

        # Sort by personalization score
        results.sort(
            key=lambda x: x['personalization_score'],
            reverse=True
        )

        return results

    def _calculate_personalization_score(
        self,
        result: Dict[str, Any],
        interests: List[tuple],
        query: str
    ) -> float:
        """
        Calculate personalization score for a result.

        Args:
            result: Search result
            interests: List of (interest, score) tuples
            query: Original search query

        Returns:
            Personalization score (0-1)
        """
        score = 0.5  # Base score

        # Check if result matches user interests
        result_topics = self._extract_topics(result)
        interest_dict = dict(interests)

        for topic in result_topics:
            if topic in interest_dict:
                score += interest_dict[topic] * 0.3

        # Check if result matches query terms
        query_terms = set(query.lower().split())
        result_text = (
            result.get('title', '').lower() + ' ' +
            result.get('abstract', '').lower()
        )

        for term in query_terms:
            if term in result_text:
                score += 0.1

        # Normalize score
        return min(score, 1.0)

    def _extract_topics(self, result: Dict[str, Any]) -> List[str]:
        """
        Extract topics from a result.

        Args:
            result: Search result

        Returns:
            List of topics
        """
        topics = []

        # Extract from metadata
        metadata = result.get('metadata', {})
        if 'topics' in metadata:
            topics.extend(metadata['topics'])

        # Extract from categories
        if 'categories' in metadata:
            topics.extend(metadata['categories'])

        # Extract from title and abstract (simplified)
        title = result.get('title', '').lower()
        abstract = result.get('abstract', '').lower()

        # Common ML/AI topics
        common_topics = [
            'machine learning', 'deep learning', 'neural networks',
            'natural language processing', 'computer vision',
            'reinforcement learning', 'transformer', 'attention',
            'graph neural networks', 'federated learning',
        ]

        for topic in common_topics:
            if topic in title or topic in abstract:
                topics.append(topic)

        return topics

    def get_recommendations(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get personalized recommendations for a user.

        Args:
            user_id: User identifier
            limit: Number of recommendations

        Returns:
            List of recommended papers
        """
        profile = self.get_user_profile(user_id)
        if not profile:
            return []

        # Get top interests
        interests = self.get_user_interests(user_id, top_n=5)

        # In production, this would query a recommendation system
        # For now, return mock recommendations based on interests
        recommendations = []

        for i, (interest, score) in enumerate(interests[:limit]):
            recommendations.append({
                'id': f"rec_{i}",
                'title': f"Recommended Paper: {interest}",
                'reason': f"Based on your interest in {interest}",
                'relevance_score': score,
                'source': 'recommendation',
            })

        return recommendations

    def cleanup_old_profiles(self, days: int = 30):
        """
        Clean up old user profiles.

        Args:
            days: Number of days after which to remove profiles
        """
        cutoff = datetime.utcnow() - timedelta(days=days)

        users_to_remove = []
        for user_id, profile in self.user_profiles.items():
            last_updated = profile.get('last_updated')
            if last_updated and last_updated < cutoff:
                users_to_remove.append(user_id)

        for user_id in users_to_remove:
            del self.user_profiles[user_id]

        print(f"Cleaned up {len(users_to_remove)} old profiles")


# Example usage
if __name__ == "__main__":
    engine = PersonalizationEngine()

    # Simulate user behavior
    user_id = "user123"

    engine.update_user_profile(
        user_id,
        "click",
        "paper1",
        {"topics": ["machine learning", "deep learning"]}
    )

    engine.update_user_profile(
        user_id,
        "save",
        "paper2",
        {"topics": ["natural language processing", "transformer"]}
    )

    # Get user interests
    interests = engine.get_user_interests(user_id)
    print("User interests:")
    for interest, score in interests:
        print(f"  {interest}: {score:.2f}")

    # Personalize results
    results = [
        {
            'id': 'res1',
            'title': 'Deep Learning for NLP',
            'abstract': 'This paper explores deep learning...',
            'metadata': {'topics': ['deep learning', 'natural language processing']},
        },
        {
            'id': 'res2',
            'title': 'Quantum Computing Basics',
            'abstract': 'Introduction to quantum computing...',
            'metadata': {'topics': ['quantum computing']},
        },
    ]

    personalized = engine.personalize_results(user_id, results, "machine learning")
    print("\nPersonalized results:")
    for result in personalized:
        print(f"  {result['title']}: {result['personalization_score']:.2f}")
