"""
arXiv Retriever for NeuroQuest
"""
import feedparser
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime
import time


class ArxivRetriever:
    """Retriever for arXiv papers."""

    BASE_URL = "http://export.arxiv.org/api/query"

    def __init__(self, max_results: int = 10):
        """
        Initialize the arXiv retriever.

        Args:
            max_results: Maximum number of results to retrieve
        """
        self.max_results = max_results
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NeuroQuest/1.0 (https://github.com/neuroquest)'
        })

    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search arXiv for papers.

        Args:
            query: Search query
            max_results: Maximum number of results (overrides instance default)

        Returns:
            List of search results
        """
        max_results = max_results or self.max_results

        # Build query parameters
        params = {
            'search_query': f'all:{query}',
            'start': 0,
            'max_results': max_results,
        }

        try:
            # Make request
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()

            # Parse feed
            feed = feedparser.parse(response.content)

            # Extract results
            results = []
            for entry in feed.entries:
                result = self._parse_entry(entry)
                if result:
                    results.append(result)

            return results

        except Exception as e:
            print(f"Error searching arXiv: {e}")
            return []

    def _parse_entry(self, entry: Any) -> Optional[Dict[str, Any]]:
        """
        Parse an arXiv feed entry.

        Args:
            entry: Feed entry

        Returns:
            Parsed result dictionary
        """
        try:
            # Extract authors
            authors = []
            if hasattr(entry, 'authors'):
                authors = [author.name for author in entry.authors]

            # Extract ID
            arxiv_id = entry.id.split('/abs/')[-1]

            # Extract published date
            published_date = None
            if hasattr(entry, 'published'):
                published_date = entry.published

            # Extract categories
            categories = []
            if hasattr(entry, 'tags'):
                categories = [tag.term for tag in entry.tags]

            return {
                'id': f"arxiv_{arxiv_id}",
                'title': entry.title,
                'authors': authors,
                'abstract': entry.summary,
                'source': 'arxiv',
                'url': entry.link,
                'published_date': published_date,
                'relevance_score': 0.8,  # Default score
                'citation_count': None,  # arXiv doesn't provide citation counts
                'metadata': {
                    'arxiv_id': arxiv_id,
                    'categories': categories,
                    'primary_category': categories[0] if categories else None,
                }
            }
        except Exception as e:
            print(f"Error parsing arXiv entry: {e}")
            return None

    def get_paper_by_id(self, arxiv_id: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific paper by arXiv ID.

        Args:
            arxiv_id: arXiv paper ID

        Returns:
            Paper details or None
        """
        params = {
            'id_list': arxiv_id,
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()

            feed = feedparser.parse(response.content)

            if feed.entries:
                return self._parse_entry(feed.entries[0])

            return None

        except Exception as e:
            print(f"Error fetching arXiv paper: {e}")
            return None

    def search_by_category(
        self,
        category: str,
        max_results: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Search papers by category.

        Args:
            category: arXiv category (e.g., 'cs.AI', 'stat.ML')
            max_results: Maximum number of results

        Returns:
            List of papers in the category
        """
        max_results = max_results or self.max_results

        params = {
            'search_query': f'cat:{category}',
            'start': 0,
            'max_results': max_results,
        }

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()

            feed = feedparser.parse(response.content)

            results = []
            for entry in feed.entries:
                result = self._parse_entry(entry)
                if result:
                    results.append(result)

            return results

        except Exception as e:
            print(f"Error searching arXiv by category: {e}")
            return []


# Example usage
if __name__ == "__main__":
    retriever = ArxivRetriever(max_results=5)

    # Search
    results = retriever.search("machine learning")
    print(f"Found {len(results)} results")

    for result in results[:2]:
        print(f"\nTitle: {result['title']}")
        print(f"Authors: {', '.join(result['authors'])}")
        print(f"URL: {result['url']}")
