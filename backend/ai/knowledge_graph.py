"""
Knowledge Graph Builder for NeuroQuest
"""
from typing import List, Dict, Any, Optional, Set
import networkx as nx
from datetime import datetime
import json


class KnowledgeGraphBuilder:
    """Builder for creating and managing knowledge graphs."""

    def __init__(self):
        """Initialize the knowledge graph builder."""
        self.graph = nx.DiGraph()
        self.node_types = {
            'paper': 'paper',
            'author': 'author',
            'concept': 'concept',
            'topic': 'topic',
        }

    def add_paper(self, paper: Dict[str, Any]) -> str:
        """
        Add a paper to the knowledge graph.

        Args:
            paper: Paper data

        Returns:
            Node ID of the added paper
        """
        paper_id = paper.get('id', f"paper_{len(self.graph.nodes)}")

        # Add paper node
        self.graph.add_node(
            paper_id,
            label=paper.get('title', ''),
            node_type='paper',
            properties={
                'authors': paper.get('authors', []),
                'abstract': paper.get('abstract', ''),
                'source': paper.get('source', ''),
                'url': paper.get('url', ''),
                'published_date': paper.get('published_date'),
                'citation_count': paper.get('citation_count'),
            },
            weight=1.0,
            created_at=datetime.utcnow().isoformat(),
        )

        # Add author nodes and edges
        for author in paper.get('authors', []):
            author_id = f"author_{author.lower().replace(' ', '_')}"
            self.graph.add_node(
                author_id,
                label=author,
                node_type='author',
                properties={},
                weight=0.5,
                created_at=datetime.utcnow().isoformat(),
            )
            self.graph.add_edge(
                author_id,
                paper_id,
                relationship='authored',
                weight=1.0,
            )

        # Extract and add concept nodes
        concepts = self._extract_concepts(paper)
        for concept in concepts:
            concept_id = f"concept_{concept.lower().replace(' ', '_')}"
            self.graph.add_node(
                concept_id,
                label=concept,
                node_type='concept',
                properties={},
                weight=0.3,
                created_at=datetime.utcnow().isoformat(),
            )
            self.graph.add_edge(
                paper_id,
                concept_id,
                relationship='about',
                weight=0.8,
            )

        return paper_id

    def add_citation(self, citing_paper_id: str, cited_paper_id: str):
        """
        Add a citation relationship between papers.

        Args:
            citing_paper_id: ID of the citing paper
            cited_paper_id: ID of the cited paper
        """
        if self.graph.has_node(citing_paper_id) and self.graph.has_node(cited_paper_id):
            self.graph.add_edge(
                citing_paper_id,
                cited_paper_id,
                relationship='cites',
                weight=1.0,
            )

    def _extract_concepts(self, paper: Dict[str, Any]) -> List[str]:
        """
        Extract concepts from a paper.

        Args:
            paper: Paper data

        Returns:
            List of concepts
        """
        concepts = []

        # Extract from metadata
        metadata = paper.get('metadata', {})
        if 'categories' in metadata:
            concepts.extend(metadata['categories'])

        # Extract from title and abstract
        title = paper.get('title', '').lower()
        abstract = paper.get('abstract', '').lower()

        # Common ML/AI concepts
        common_concepts = [
            'machine learning', 'deep learning', 'neural networks',
            'natural language processing', 'computer vision',
            'reinforcement learning', 'transformer', 'attention',
            'graph neural networks', 'federated learning',
            'convolutional neural networks', 'recurrent neural networks',
            'generative adversarial networks', 'autoencoder',
            'transfer learning', 'few-shot learning',
        ]

        for concept in common_concepts:
            if concept in title or concept in abstract:
                concepts.append(concept)

        return list(set(concepts))

    def get_subgraph(
        self,
        node_id: str,
        max_depth: int = 2,
        max_nodes: int = 50
    ) -> Dict[str, Any]:
        """
        Get a subgraph around a node.

        Args:
            node_id: Starting node ID
            max_depth: Maximum depth of traversal
            max_nodes: Maximum number of nodes

        Returns:
            Subgraph data
        """
        if not self.graph.has_node(node_id):
            return {'nodes': [], 'edges': []}

        # Get nodes within max_depth
        nodes = set()
        edges = set()

        def traverse(current_id: str, depth: int):
            if depth > max_depth or len(nodes) >= max_nodes:
                return

            nodes.add(current_id)

            # Get neighbors
            neighbors = list(self.graph.neighbors(current_id))
            for neighbor_id in neighbors:
                if len(nodes) >= max_nodes:
                    break

                edge_data = self.graph.get_edge_data(current_id, neighbor_id)
                edges.add((current_id, neighbor_id, edge_data))

                if neighbor_id not in nodes:
                    traverse(neighbor_id, depth + 1)

        traverse(node_id, 0)

        # Build result
        result_nodes = []
        for node_id in nodes:
            node_data = self.graph.nodes[node_id]
            result_nodes.append({
                'id': node_id,
                'label': node_data.get('label', ''),
                'type': node_data.get('node_type', ''),
                'properties': node_data.get('properties', {}),
                'weight': node_data.get('weight', 1.0),
            })

        result_edges = []
        for source, target, data in edges:
            result_edges.append({
                'source': source,
                'target': target,
                'relationship': data.get('relationship', ''),
                'weight': data.get('weight', 1.0),
                'properties': data.get('properties', {}),
            })

        return {
            'nodes': result_nodes,
            'edges': result_edges,
        }

    def find_shortest_path(
        self,
        source_id: str,
        target_id: str
    ) -> Optional[List[str]]:
        """
        Find shortest path between two nodes.

        Args:
            source_id: Source node ID
            target_id: Target node ID

        Returns:
            List of node IDs in the path, or None if no path exists
        """
        try:
            path = nx.shortest_path(self.graph, source_id, target_id)
            return path
        except nx.NetworkXNoPath:
            return None

    def get_node_neighbors(
        self,
        node_id: str,
        relationship: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get neighbors of a node.

        Args:
            node_id: Node ID
            relationship: Filter by relationship type

        Returns:
            List of neighbor nodes
        """
        if not self.graph.has_node(node_id):
            return []

        neighbors = []
        for neighbor_id in self.graph.neighbors(node_id):
            edge_data = self.graph.get_edge_data(node_id, neighbor_id)

            if relationship is None or edge_data.get('relationship') == relationship:
                node_data = self.graph.nodes[neighbor_id]
                neighbors.append({
                    'id': neighbor_id,
                    'label': node_data.get('label', ''),
                    'type': node_data.get('node_type', ''),
                    'relationship': edge_data.get('relationship', ''),
                    'weight': edge_data.get('weight', 1.0),
                })

        return neighbors

    def get_statistics(self) -> Dict[str, Any]:
        """
        Get graph statistics.

        Returns:
            Dictionary of graph statistics
        """
        node_types = {}
        for node_id, node_data in self.graph.nodes(data=True):
            node_type = node_data.get('node_type', 'unknown')
            node_types[node_type] = node_types.get(node_type, 0) + 1

        edge_types = {}
        for source, target, edge_data in self.graph.edges(data=True):
            relationship = edge_data.get('relationship', 'unknown')
            edge_types[relationship] = edge_types.get(relationship, 0) + 1

        return {
            'total_nodes': self.graph.number_of_nodes(),
            'total_edges': self.graph.number_of_edges(),
            'node_types': node_types,
            'edge_types': edge_types,
            'is_connected': nx.is_connected(self.graph.to_undirected()),
            'average_clustering': nx.average_clustering(self.graph.to_undirected()),
        }

    def export_graph(self, format: str = 'json') -> str:
        """
        Export the graph.

        Args:
            format: Export format ('json', 'gexf')

        Returns:
            Exported graph data
        """
        if format == 'json':
            nodes = []
            edges = []

            for node_id, node_data in self.graph.nodes(data=True):
                nodes.append({
                    'id': node_id,
                    **node_data,
                })

            for source, target, edge_data in self.graph.edges(data=True):
                edges.append({
                    'source': source,
                    'target': target,
                    **edge_data,
                })

            return json.dumps({
                'nodes': nodes,
                'edges': edges,
            })

        elif format == 'gexf':
            from io import StringIO
            output = StringIO()
            nx.write_gexf(self.graph, output)
            return output.getvalue()

        else:
            raise ValueError(f"Unsupported format: {format}")

    def save_graph(self, filepath: str):
        """
        Save the graph to a file.

        Args:
            filepath: Path to save the graph
        """
        if filepath.endswith('.gexf'):
            nx.write_gexf(self.graph, filepath)
        elif filepath.endswith('.graphml'):
            nx.write_graphml(self.graph, filepath)
        else:
            raise ValueError("Unsupported file format. Use .gexf or .graphml")

    def load_graph(self, filepath: str):
        """
        Load a graph from a file.

        Args:
            filepath: Path to load the graph from
        """
        if filepath.endswith('.gexf'):
            self.graph = nx.read_gexf(filepath)
        elif filepath.endswith('.graphml'):
            self.graph = nx.read_graphml(filepath)
        else:
            raise ValueError("Unsupported file format. Use .gexf or .graphml")


# Example usage
if __name__ == "__main__":
    builder = KnowledgeGraphBuilder()

    # Add sample papers
    paper1 = {
        'id': 'paper1',
        'title': 'Attention Is All You Need',
        'authors': ['Ashish Vaswani', 'Noam Shazeer'],
        'abstract': 'The dominant sequence transduction models...',
        'source': 'arxiv',
        'url': 'https://arxiv.org/abs/1706.03762',
        'metadata': {'categories': ['cs.AI', 'cs.LG']},
    }

    paper2 = {
        'id': 'paper2',
        'title': 'BERT: Pre-training of Deep Bidirectional Transformers',
        'authors': ['Jacob Devlin', 'Ming-Wei Chang'],
        'abstract': 'We introduce a new language representation model...',
        'source': 'arxiv',
        'url': 'https://arxiv.org/abs/1810.04805',
        'metadata': {'categories': ['cs.CL', 'cs.LG']},
    }

    builder.add_paper(paper1)
    builder.add_paper(paper2)

    # Add citation
    builder.add_citation('paper2', 'paper1')

    # Get statistics
    stats = builder.get_statistics()
    print("Graph Statistics:")
    print(f"  Nodes: {stats['total_nodes']}")
    print(f"  Edges: {stats['total_edges']}")
    print(f"  Node types: {stats['node_types']}")
    print(f"  Edge types: {stats['edge_types']}")

    # Get subgraph
    subgraph = builder.get_subgraph('paper1', max_depth=2)
    print(f"\nSubgraph around paper1:")
    print(f"  Nodes: {len(subgraph['nodes'])}")
    print(f"  Edges: {len(subgraph['edges'])}")
