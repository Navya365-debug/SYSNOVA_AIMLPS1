"""
Session Memory System for Persistent Learning
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
import json
import os
from pathlib import Path


class SessionMemory:
    """
    Manages persistent session memory for continuous learning across sessions.
    """

    def __init__(self, storage_dir: str = "./sessions"):
        """
        Initialize session memory.

        Args:
            storage_dir: Directory to store session data
        """
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.current_sessions: Dict[str, Dict[str, Any]] = {}

    def create_session(self, user_id: str) -> str:
        """
        Create a new session for user.

        Args:
            user_id: User identifier

        Returns:
            Session ID
        """
        session_id = f"session_{datetime.utcnow().timestamp()}"

        session = {
            'session_id': session_id,
            'user_id': user_id,
            'created_at': datetime.utcnow().isoformat(),
            'last_activity': datetime.utcnow().isoformat(),
            'interactions': [],
            'queries': [],
            'papers_viewed': [],
            'learning_state': {
                'topics_discovered': [],
                'preferences_identified': [],
                'improvement_made': [],
            },
            'session_goals': {
                'papers_explored': 0,
                'topics_learned': 0,
                'connections_made': 0,
            },
        }

        self.current_sessions[session_id] = session
        return session_id

    def update_session(self, session_id: str, update_data: Dict[str, Any]):
        """
        Update session with new data.

        Args:
            session_id: Session identifier
            update_data: Data to update
        """
        if session_id not in self.current_sessions:
            return

        session = self.current_sessions[session_id]
        session['last_activity'] = datetime.utcnow().isoformat()

        # Update session data
        for key, value in update_data.items():
            if key in session and isinstance(session[key], list):
                session[key].append(value)
            else:
                session[key] = value

    def add_interaction(
        self,
        session_id: str,
        interaction_type: str,
        paper_id: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Add interaction to session.

        Args:
            session_id: Session identifier
            interaction_type: Type of interaction
            paper_id: Paper identifier
            metadata: Additional metadata
        """
        if session_id not in self.current_sessions:
            return

        interaction = {
            'type': interaction_type,
            'paper_id': paper_id,
            'timestamp': datetime.utcnow().isoformat(),
            'metadata': metadata or {},
        }

        self.current_sessions[session_id]['interactions'].append(interaction)

        # Update session goals
        if interaction_type in ['click', 'save', 'share']:
            self.current_sessions[session_id]['session_goals']['papers_explored'] += 1

    def add_query(self, session_id: str, query: str, results_count: int):
        """
        Add query to session.

        Args:
            session_id: Session identifier
            query: Search query
            results_count: Number of results
        """
        if session_id not in self.current_sessions:
            return

        query_data = {
            'query': query,
            'timestamp': datetime.utcnow().isoformat(),
            'results_count': results_count,
        }

        self.current_sessions[session_id]['queries'].append(query_data)

    def add_paper_viewed(self, session_id: str, paper_id: str, duration: int):
        """
        Add paper view to session.

        Args:
            session_id: Session identifier
            paper_id: Paper identifier
            duration: View duration in seconds
        """
        if session_id not in self.current_sessions:
            return

        paper_view = {
            'paper_id': paper_id,
            'timestamp': datetime.utcnow().isoformat(),
            'duration': duration,
        }

        self.current_sessions[session_id]['papers_viewed'].append(paper_view)

    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """
        Get summary of session.

        Args:
            session_id: Session identifier

        Returns:
            Session summary
        """
        if session_id not in self.current_sessions:
            return {'error': 'Session not found'}

        session = self.current_sessions[session_id]

        # Calculate session duration
        created_at = datetime.fromisoformat(session['created_at'])
        last_activity = datetime.fromisoformat(session['last_activity'])
        duration = (last_activity - created_at).total_seconds()

        # Get unique topics
        topics = set()
        for interaction in session['interactions']:
            if 'metadata' in interaction and 'topics' in interaction['metadata']:
                topics.update(interaction['metadata']['topics'])

        return {
            'session_id': session_id,
            'duration_minutes': duration / 60,
            'total_interactions': len(session['interactions']),
            'total_queries': len(session['queries']),
            'papers_viewed': len(session['papers_viewed']),
            'unique_topics': list(topics),
            'goals_achieved': session['session_goals'],
            'learning_progress': self._calculate_learning_progress(session),
        }

    def _calculate_learning_progress(self, session: Dict[str, Any]) -> float:
        """
        Calculate learning progress for session.

        Args:
            session: Session data

        Returns:
            Learning progress (0-1)
        """
        goals = session['session_goals']
        total_goals = sum(goals.values())

        if total_goals == 0:
            return 0.0

        # Normalize progress (assume 20 interactions is good progress)
        progress = min(total_goals / 20.0, 1.0)

        return progress

    def save_session(self, session_id: str):
        """
        Save session to disk.

        Args:
            session_id: Session identifier
        """
        if session_id not in self.current_sessions:
            return

        session = self.current_sessions[session_id]
        user_id = session['user_id']

        # Create user directory
        user_dir = self.storage_dir / user_id
        user_dir.mkdir(exist_ok=True)

        # Save session
        session_file = user_dir / f"{session_id}.json"
        with open(session_file, 'w') as f:
            json.dump(session, f, indent=2)

    def load_user_sessions(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Load all sessions for a user.

        Args:
            user_id: User identifier

        Returns:
            List of sessions
        """
        user_dir = self.storage_dir / user_id

        if not user_dir.exists():
            return []

        sessions = []
        for session_file in user_dir.glob("session_*.json"):
            with open(session_file, 'r') as f:
                session = json.load(f)
                sessions.append(session)

        # Sort by creation date (most recent first)
        sessions.sort(key=lambda x: x['created_at'], reverse=True)

        return sessions

    def get_user_learning_history(self, user_id: str) -> Dict[str, Any]:
        """
        Get comprehensive learning history for user.

        Args:
            user_id: User identifier

        Returns:
            Learning history summary
        """
        sessions = self.load_user_sessions(user_id)

        if not sessions:
            return {
                'total_sessions': 0,
                'total_interactions': 0,
                'total_papers_viewed': 0,
                'topics_explored': [],
                'learning_trend': [],
            }

        # Aggregate data across sessions
        total_interactions = sum(len(session['interactions']) for session in sessions)
        total_papers_viewed = sum(len(session['papers_viewed']) for session in sessions)

        # Get all unique topics
        all_topics = set()
        for session in sessions:
            for interaction in session['interactions']:
                if 'metadata' in interaction and 'topics' in interaction['metadata']:
                    all_topics.update(interaction['metadata']['topics'])

        # Calculate learning trend
        learning_trend = []
        for session in sessions:
            progress = self._calculate_learning_progress(session)
            learning_trend.append({
                'session_id': session['session_id'],
                'date': session['created_at'][:10],  # Just the date
                'progress': progress,
            })

        return {
            'total_sessions': len(sessions),
            'total_interactions': total_interactions,
            'total_papers_viewed': total_papers_viewed,
            'topics_explored': list(all_topics),
            'learning_trend': learning_trend,
            'most_recent_session': sessions[0] if sessions else None,
        }

    def cleanup_old_sessions(self, days: int = 30):
        """
        Clean up sessions older than specified days.

        Args:
            days: Number of days to keep sessions
        """
        cutoff = datetime.utcnow() - timedelta(days=days)

        for user_dir in self.storage_dir.iterdir():
            if user_dir.is_dir():
                for session_file in user_dir.glob("session_*.json"):
                    try:
                        with open(session_file, 'r') as f:
                            session = json.load(f)

                        created_at = datetime.fromisoformat(session['created_at'])
                        if created_at < cutoff:
                            session_file.unlink()
                            print(f"Cleaned up old session: {session_file.name}")

                    except Exception as e:
                        print(f"Error cleaning up session {session_file.name}: {e}")


# Example usage
if __name__ == "__main__":
    memory = SessionMemory()

    # Create a session
    session_id = memory.create_session("user123")

    # Add interactions
    memory.add_interaction(
        session_id,
        "click",
        "paper1",
        {"topics": ["machine learning", "deep learning"]}
    )

    memory.add_query(session_id, "transformer architecture", 10)

    # Get session summary
    summary = memory.get_session_summary(session_id)
    print("Session Summary:")
    print(json.dumps(summary, indent=2, default=str))

    # Save session
    memory.save_session(session_id)

    # Load user sessions
    user_sessions = memory.load_user_sessions("user123")
    print(f"\nTotal sessions for user: {len(user_sessions)}")
