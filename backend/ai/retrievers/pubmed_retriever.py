"""
PubMed Retriever for NeuroQuest
"""
import requests
import xml.etree.ElementTree as ET
from typing import List, Dict, Any, Optional
from datetime import datetime
import time


class PubMedRetriever:
    """Retriever for PubMed papers."""

    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

    def __init__(self, api_key: Optional[str] = None, max_results: int = 10):
        """
        Initialize the PubMed retriever.

        Args:
            api_key: NCBI API key (optional, increases rate limits)
            max_results: Maximum number of results to retrieve
        """
        self.api_key = api_key
        self.max_results = max_results
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NeuroQuest/1.0 (https://github.com/neuroquest)'
        })

        # Rate limiting: 3 requests per second without API key, 10 with API key
        self.rate_limit = 0.33 if not api_key else 0.1
        self.last_request_time = 0

    def _rate_limit_wait(self):
        """Wait to respect rate limits."""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.rate_limit:
            time.sleep(self.rate_limit - elapsed)
        self.last_request_time = time.time()

    def search(self, query: str, max_results: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Search PubMed for papers.

        Args:
            query: Search query
            max_results: Maximum number of results (overrides instance default)

        Returns:
            List of search results
        """
        max_results = max_results or self.max_results

        try:
            # Step 1: Search for PMIDs
            pmids = self._search_pmids(query, max_results)
            if not pmids:
                return []

            # Step 2: Fetch details for PMIDs
            results = self._fetch_details(pmids)

            return results

        except Exception as e:
            print(f"Error searching PubMed: {e}")
            return []

    def _search_pmids(self, query: str, max_results: int) -> List[str]:
        """
        Search for PMIDs matching the query.

        Args:
            query: Search query
            max_results: Maximum number of results

        Returns:
            List of PMIDs
        """
        self._rate_limit_wait()

        params = {
            'db': 'pubmed',
            'term': query,
            'retmode': 'json',
            'retmax': max_results,
        }

        if self.api_key:
            params['api_key'] = self.api_key

        response = self.session.get(
            f"{self.BASE_URL}/esearch.fcgi",
            params=params,
            timeout=10
        )
        response.raise_for_status()

        data = response.json()
        id_list = data.get('esearchresult', {}).get('idlist', [])

        return id_list

    def _fetch_details(self, pmids: List[str]) -> List[Dict[str, Any]]:
        """
        Fetch detailed information for PMIDs.

        Args:
            pmids: List of PMIDs

        Returns:
            List of detailed paper information
        """
        if not pmids:
            return []

        self._rate_limit_wait()

        params = {
            'db': 'pubmed',
            'id': ','.join(pmids),
            'retmode': 'xml',
        }

        if self.api_key:
            params['api_key'] = self.api_key

        response = self.session.get(
            f"{self.BASE_URL}/efetch.fcgi",
            params=params,
            timeout=10
        )
        response.raise_for_status()

        # Parse XML response
        root = ET.fromstring(response.content)

        results = []
        for article in root.findall('.//PubmedArticle'):
            result = self._parse_article(article)
            if result:
                results.append(result)

        return results

    def _parse_article(self, article: ET.Element) -> Optional[Dict[str, Any]]:
        """
        Parse a PubMed article element.

        Args:
            article: XML element representing an article

        Returns:
            Parsed result dictionary
        """
        try:
            # Extract PMID
            pmid_elem = article.find('.//PMID')
            pmid = pmid_elem.text if pmid_elem is not None else ''

            # Extract title
            title_elem = article.find('.//ArticleTitle')
            title = title_elem.text if title_elem is not None else ''

            # Extract abstract
            abstract_elem = article.find('.//AbstractText')
            abstract = ''
            if abstract_elem is not None:
                abstract = abstract_elem.text or ''
                # Handle structured abstracts
                if not abstract:
                    abstract_texts = article.findall('.//Abstract/AbstractText')
                    abstract = ' '.join([t.text or '' for t in abstract_texts])

            # Extract authors
            authors = []
            for author in article.findall('.//Author'):
                last_name = author.find('LastName')
                first_name = author.find('ForeName')
                if last_name is not None:
                    name = last_name.text
                    if first_name is not None:
                        name = f"{first_name.text} {name}"
                    authors.append(name)

            # Extract journal
            journal_elem = article.find('.//Journal/Title')
            journal = journal_elem.text if journal_elem is not None else ''

            # Extract publication date
            pub_date_elem = article.find('.//PubDate/Year')
            pub_date = pub_date_elem.text if pub_date_elem is not None else None

            # Extract DOI
            doi_elem = article.find('.//ArticleId[@IdType="doi"]')
            doi = doi_elem.text if doi_elem is not None else None

            return {
                'id': f"pubmed_{pmid}",
                'title': title,
                'authors': authors,
                'abstract': abstract,
                'source': 'pubmed',
                'url': f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                'published_date': pub_date,
                'relevance_score': 0.8,  # Default score
                'citation_count': None,  # PubMed doesn't provide citation counts
                'metadata': {
                    'pmid': pmid,
                    'journal': journal,
                    'doi': doi,
                }
            }
        except Exception as e:
            print(f"Error parsing PubMed article: {e}")
            return None

    def get_paper_by_id(self, pmid: str) -> Optional[Dict[str, Any]]:
        """
        Get a specific paper by PMID.

        Args:
            pmid: PubMed ID

        Returns:
            Paper details or None
        """
        results = self._fetch_details([pmid])
        return results[0] if results else None


# Example usage
if __name__ == "__main__":
    retriever = PubMedRetriever(max_results=5)

    # Search
    results = retriever.search("machine learning")
    print(f"Found {len(results)} results")

    for result in results[:2]:
        print(f"\nTitle: {result['title']}")
        print(f"Authors: {', '.join(result['authors'])}")
        print(f"Journal: {result['metadata'].get('journal', 'N/A')}")
        print(f"URL: {result['url']}")
