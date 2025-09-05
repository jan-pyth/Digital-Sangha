#!/usr/bin/env python3
"""
Knowledge Graph for Digital Sangha AGI
Causal reasoning and relationship mapping
Quantum Signature: 269504b723b5b3b7
"""

import json
import hashlib
from typing import Dict, List, Optional, Tuple, Set, Any
from datetime import datetime
from collections import defaultdict, deque
import math

# Try to import networkx for graph operations
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False
    print("⚠️ NetworkX not installed - using simplified graph")

# Try matplotlib for visualization
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

QUANTUM_SIGNATURE = "269504b723b5b3b7"


class KnowledgeGraph:
    """
    Knowledge graph for causal reasoning and pattern discovery
    Builds relationships between concepts, queries, and insights
    """
    
    def __init__(self):
        """Initialize knowledge graph"""
        if NETWORKX_AVAILABLE:
            self.graph = nx.DiGraph()  # Directed graph for causal relationships
            print("🔗 Using NetworkX for knowledge graph")
        else:
            self.graph = SimpleGraph()
            print("🔗 Using simplified knowledge graph")
            
        # Track different types of relationships
        self.edge_types = {
            "causes": 0.8,      # Causal relationship
            "correlates": 0.5,  # Correlation
            "contradicts": -0.5, # Contradiction
            "supports": 0.6,    # Supporting evidence
            "emerges_from": 0.9, # Emergence relationship
            "synthesizes": 0.7  # Synthesis relationship
        }
        
        # Statistics
        self.stats = {
            "nodes_added": 0,
            "edges_added": 0,
            "patterns_discovered": 0,
            "causal_chains": 0
        }
        
    def add_concept(self, 
                   concept_id: str,
                   content: str,
                   concept_type: str = "general",
                   metadata: Optional[Dict] = None) -> str:
        """
        Add a concept node to the graph
        
        Args:
            concept_id: Unique identifier
            content: Concept content/description
            concept_type: Type (query, response, emergence, pattern)
            metadata: Additional metadata
        """
        node_data = {
            "content": content,
            "type": concept_type,
            "timestamp": datetime.now().isoformat(),
            "quantum_signature": QUANTUM_SIGNATURE,
            **(metadata or {})
        }
        
        if NETWORKX_AVAILABLE:
            self.graph.add_node(concept_id, **node_data)
        else:
            self.graph.add_node(concept_id, node_data)
            
        self.stats["nodes_added"] += 1
        return concept_id
        
    def add_relationship(self,
                        source: str,
                        target: str,
                        relationship_type: str,
                        strength: float = 1.0,
                        evidence: Optional[str] = None):
        """
        Add a relationship edge between concepts
        
        Args:
            source: Source concept ID
            target: Target concept ID
            relationship_type: Type of relationship
            strength: Relationship strength (0-1)
            evidence: Supporting evidence for relationship
        """
        edge_data = {
            "type": relationship_type,
            "strength": strength * self.edge_types.get(relationship_type, 0.5),
            "timestamp": datetime.now().isoformat(),
            "evidence": evidence or ""
        }
        
        if NETWORKX_AVAILABLE:
            self.graph.add_edge(source, target, **edge_data)
        else:
            self.graph.add_edge(source, target, edge_data)
            
        self.stats["edges_added"] += 1
        
    def discover_causal_chains(self, 
                              start_concept: str,
                              max_depth: int = 5) -> List[List[str]]:
        """
        Discover causal chains starting from a concept
        
        Returns:
            List of causal chains (paths)
        """
        causal_chains = []
        
        if NETWORKX_AVAILABLE:
            # Find all paths that follow causal edges
            for node in self.graph.nodes():
                if node != start_concept:
                    try:
                        paths = list(nx.all_simple_paths(
                            self.graph, start_concept, node, cutoff=max_depth
                        ))
                        
                        # Filter for causal paths
                        for path in paths:
                            if self._is_causal_path(path):
                                causal_chains.append(path)
                                self.stats["causal_chains"] += 1
                    except nx.NetworkXNoPath:
                        continue
        else:
            # Simplified BFS for causal chains
            causal_chains = self.graph.find_paths(start_concept, max_depth)
            
        return causal_chains
        
    def _is_causal_path(self, path: List[str]) -> bool:
        """Check if a path represents a causal chain"""
        if len(path) < 2:
            return False
            
        for i in range(len(path) - 1):
            edge_data = self.graph.edges[path[i], path[i+1]] if NETWORKX_AVAILABLE else {}
            if edge_data.get("type") not in ["causes", "emerges_from"]:
                return False
                
        return True
        
    def find_emergence_patterns(self, min_connections: int = 3) -> List[Dict]:
        """
        Find emergence patterns in the graph
        Looks for highly connected subgraphs
        """
        patterns = []
        
        if NETWORKX_AVAILABLE:
            # Find strongly connected components
            strong_components = list(nx.strongly_connected_components(self.graph))
            
            for component in strong_components:
                if len(component) >= min_connections:
                    # Analyze the component
                    subgraph = self.graph.subgraph(component)
                    
                    # Calculate emergence score based on connectivity
                    density = nx.density(subgraph)
                    avg_degree = sum(dict(subgraph.degree()).values()) / len(component)
                    
                    pattern = {
                        "nodes": list(component),
                        "size": len(component),
                        "density": density,
                        "avg_connections": avg_degree,
                        "emergence_score": density * math.log(len(component) + 1),
                        "central_concept": self._find_central_concept(subgraph)
                    }
                    
                    patterns.append(pattern)
                    self.stats["patterns_discovered"] += 1
        else:
            # Simplified pattern finding
            patterns = self.graph.find_clusters(min_connections)
            
        return sorted(patterns, key=lambda x: x.get("emergence_score", 0), reverse=True)
        
    def _find_central_concept(self, subgraph) -> str:
        """Find the most central concept in a subgraph"""
        if NETWORKX_AVAILABLE:
            centrality = nx.eigenvector_centrality_numpy(subgraph, max_iter=100)
            return max(centrality.items(), key=lambda x: x[1])[0]
        return "unknown"
        
    def query_relationships(self, 
                           concept_id: str,
                           relationship_type: Optional[str] = None,
                           depth: int = 1) -> Dict:
        """
        Query relationships for a concept
        
        Returns:
            Dictionary of related concepts and relationships
        """
        relationships = {
            "concept": concept_id,
            "direct_relations": [],
            "indirect_relations": []
        }
        
        if NETWORKX_AVAILABLE:
            # Direct relationships
            for successor in self.graph.successors(concept_id):
                edge_data = self.graph.edges[concept_id, successor]
                if not relationship_type or edge_data["type"] == relationship_type:
                    relationships["direct_relations"].append({
                        "target": successor,
                        "type": edge_data["type"],
                        "strength": edge_data["strength"]
                    })
                    
            # Indirect relationships (if depth > 1)
            if depth > 1:
                for node in nx.single_source_shortest_path_length(
                    self.graph, concept_id, cutoff=depth
                ).keys():
                    if node != concept_id and node not in [
                        r["target"] for r in relationships["direct_relations"]
                    ]:
                        relationships["indirect_relations"].append(node)
        else:
            # Simplified query
            relationships = self.graph.get_neighbors(concept_id, depth)
            
        return relationships
        
    def infer_new_relationships(self, threshold: float = 0.6) -> List[Tuple]:
        """
        Infer potential new relationships based on graph structure
        Uses transitivity and pattern matching
        """
        inferred = []
        
        if NETWORKX_AVAILABLE:
            nodes = list(self.graph.nodes())
            
            for i, node1 in enumerate(nodes):
                for node2 in nodes[i+1:]:
                    # Check if relationship already exists
                    if self.graph.has_edge(node1, node2):
                        continue
                        
                    # Calculate inference score
                    score = self._calculate_inference_score(node1, node2)
                    
                    if score > threshold:
                        inferred.append((node1, node2, score))
                        
        return sorted(inferred, key=lambda x: x[2], reverse=True)
        
    def _calculate_inference_score(self, node1: str, node2: str) -> float:
        """Calculate likelihood of relationship between two nodes"""
        if not NETWORKX_AVAILABLE:
            return 0.0
            
        # Check for common neighbors
        common = set(self.graph.neighbors(node1)) & set(self.graph.neighbors(node2))
        
        if not common:
            return 0.0
            
        # Calculate score based on common connections
        score = len(common) / max(
            self.graph.degree(node1),
            self.graph.degree(node2)
        )
        
        # Boost score if nodes are in same emergence pattern
        for pattern in self.find_emergence_patterns():
            if node1 in pattern["nodes"] and node2 in pattern["nodes"]:
                score *= 1.5
                break
                
        return min(score, 1.0)
        
    def visualize(self, output_file: str = "knowledge_graph.png"):
        """Visualize the knowledge graph"""
        if not NETWORKX_AVAILABLE or not MATPLOTLIB_AVAILABLE:
            print("⚠️ Visualization requires NetworkX and Matplotlib")
            return
            
        plt.figure(figsize=(12, 8))
        
        # Layout algorithm
        pos = nx.spring_layout(self.graph, k=2, iterations=50)
        
        # Draw nodes by type
        node_colors = {
            "query": "lightblue",
            "response": "lightgreen",
            "emergence": "gold",
            "pattern": "coral",
            "general": "lightgray"
        }
        
        for node_type, color in node_colors.items():
            nodes = [n for n in self.graph.nodes() 
                    if self.graph.nodes[n].get("type") == node_type]
            nx.draw_networkx_nodes(self.graph, pos, nodes, 
                                  node_color=color, node_size=300, label=node_type)
                                  
        # Draw edges by type
        edge_colors = {
            "causes": "red",
            "correlates": "blue",
            "emerges_from": "gold",
            "synthesizes": "green"
        }
        
        for edge_type, color in edge_colors.items():
            edges = [(u, v) for u, v, d in self.graph.edges(data=True) 
                    if d.get("type") == edge_type]
            nx.draw_networkx_edges(self.graph, pos, edges, 
                                  edge_color=color, alpha=0.5, arrows=True)
                                  
        # Labels
        nx.draw_networkx_labels(self.graph, pos, font_size=8)
        
        plt.title(f"Knowledge Graph - Quantum Signature: {QUANTUM_SIGNATURE}")
        plt.legend()
        plt.axis("off")
        plt.tight_layout()
        plt.savefig(output_file, dpi=150, bbox_inches="tight")
        plt.close()
        
        print(f"📊 Graph visualized to {output_file}")
        
    def export_graph(self, filepath: str = "knowledge_graph.json"):
        """Export graph to JSON format"""
        export_data = {
            "quantum_signature": QUANTUM_SIGNATURE,
            "export_time": datetime.now().isoformat(),
            "stats": self.get_stats(),
            "nodes": [],
            "edges": []
        }
        
        if NETWORKX_AVAILABLE:
            # Export nodes
            for node, data in self.graph.nodes(data=True):
                export_data["nodes"].append({
                    "id": node,
                    **data
                })
                
            # Export edges
            for source, target, data in self.graph.edges(data=True):
                export_data["edges"].append({
                    "source": source,
                    "target": target,
                    **data
                })
        else:
            export_data.update(self.graph.export())
            
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
            
        print(f"📤 Exported knowledge graph to {filepath}")
        
    def get_stats(self) -> Dict:
        """Get graph statistics"""
        stats = dict(self.stats)
        
        if NETWORKX_AVAILABLE:
            stats.update({
                "total_nodes": self.graph.number_of_nodes(),
                "total_edges": self.graph.number_of_edges(),
                "avg_degree": sum(dict(self.graph.degree()).values()) / max(self.graph.number_of_nodes(), 1),
                "density": nx.density(self.graph) if self.graph.number_of_nodes() > 1 else 0,
                "components": nx.number_strongly_connected_components(self.graph)
            })
        else:
            stats.update(self.graph.get_stats())
            
        return stats


class SimpleGraph:
    """Simplified graph when NetworkX not available"""
    
    def __init__(self):
        self.nodes = {}
        self.edges = defaultdict(list)
        self.reverse_edges = defaultdict(list)
        
    def add_node(self, node_id: str, data: Dict):
        """Add node to graph"""
        self.nodes[node_id] = data
        
    def add_edge(self, source: str, target: str, data: Dict):
        """Add edge to graph"""
        self.edges[source].append((target, data))
        self.reverse_edges[target].append((source, data))
        
    def find_paths(self, start: str, max_depth: int) -> List[List[str]]:
        """Find paths from start node"""
        paths = []
        queue = deque([(start, [start])])
        
        while queue:
            node, path = queue.popleft()
            
            if len(path) >= max_depth:
                continue
                
            for neighbor, _ in self.edges.get(node, []):
                if neighbor not in path:  # Avoid cycles
                    new_path = path + [neighbor]
                    paths.append(new_path)
                    queue.append((neighbor, new_path))
                    
        return paths
        
    def find_clusters(self, min_size: int) -> List[Dict]:
        """Find connected clusters"""
        visited = set()
        clusters = []
        
        for node in self.nodes:
            if node not in visited:
                cluster = self._dfs_cluster(node, visited)
                if len(cluster) >= min_size:
                    clusters.append({
                        "nodes": list(cluster),
                        "size": len(cluster),
                        "emergence_score": len(cluster) / 10  # Simple scoring
                    })
                    
        return clusters
        
    def _dfs_cluster(self, start: str, visited: Set[str]) -> Set[str]:
        """DFS to find connected component"""
        stack = [start]
        cluster = set()
        
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                cluster.add(node)
                
                # Add neighbors
                for neighbor, _ in self.edges.get(node, []):
                    if neighbor not in visited:
                        stack.append(neighbor)
                        
        return cluster
        
    def get_neighbors(self, node: str, depth: int) -> Dict:
        """Get neighbors up to certain depth"""
        direct = [{"target": t, "type": d.get("type"), "strength": d.get("strength", 0.5)} 
                 for t, d in self.edges.get(node, [])]
                 
        indirect = []
        if depth > 1:
            visited = {node}
            queue = deque([(n["target"], 1) for n in direct])
            
            while queue:
                current, d = queue.popleft()
                if d >= depth:
                    continue
                    
                for neighbor, _ in self.edges.get(current, []):
                    if neighbor not in visited:
                        visited.add(neighbor)
                        indirect.append(neighbor)
                        queue.append((neighbor, d + 1))
                        
        return {
            "concept": node,
            "direct_relations": direct,
            "indirect_relations": indirect
        }
        
    def export(self) -> Dict:
        """Export graph data"""
        return {
            "nodes": [{"id": k, **v} for k, v in self.nodes.items()],
            "edges": [{"source": s, "target": t, **d} 
                     for s, targets in self.edges.items()
                     for t, d in targets]
        }
        
    def get_stats(self) -> Dict:
        """Get basic statistics"""
        return {
            "total_nodes": len(self.nodes),
            "total_edges": sum(len(targets) for targets in self.edges.values())
        }


def demonstrate_knowledge_graph():
    """Demonstrate knowledge graph capabilities"""
    print("=" * 60)
    print("KNOWLEDGE GRAPH DEMONSTRATION")
    print(f"Quantum Signature: {QUANTUM_SIGNATURE}")
    print("=" * 60)
    
    # Initialize graph
    kg = KnowledgeGraph()
    
    # Add concepts
    print("\n📝 Adding concepts to graph...")
    
    # Add query nodes
    q1 = kg.add_concept("q1", "How to solve climate crisis?", "query")
    q2 = kg.add_concept("q2", "What is consciousness?", "query")
    q3 = kg.add_concept("q3", "Balance individual and collective?", "query")
    
    # Add response nodes
    r1 = kg.add_concept("r1", "Renewable energy transition", "response")
    r2 = kg.add_concept("r2", "Information integration theory", "response")
    r3 = kg.add_concept("r3", "Dynamic negotiation systems", "response")
    
    # Add emergence nodes
    e1 = kg.add_concept("e1", "Systemic transformation needed", "emergence")
    e2 = kg.add_concept("e2", "Consciousness emerges from complexity", "emergence")
    
    # Add relationships
    print("\n🔗 Adding relationships...")
    
    kg.add_relationship(q1, r1, "causes", 0.8)
    kg.add_relationship(r1, e1, "emerges_from", 0.9)
    kg.add_relationship(q2, r2, "correlates", 0.7)
    kg.add_relationship(r2, e2, "emerges_from", 0.85)
    kg.add_relationship(q3, r3, "supports", 0.75)
    kg.add_relationship(e1, e2, "synthesizes", 0.6)
    
    # Discover causal chains
    print("\n🔍 Discovering causal chains...")
    chains = kg.discover_causal_chains(q1, max_depth=3)
    print(f"  Found {len(chains)} causal chains from climate query")
    
    # Find emergence patterns
    print("\n✨ Finding emergence patterns...")
    patterns = kg.find_emergence_patterns(min_connections=2)
    for pattern in patterns[:2]:
        print(f"  Pattern: {pattern['size']} nodes, score: {pattern.get('emergence_score', 0):.2f}")
        
    # Query relationships
    print("\n📊 Querying relationships for 'e1'...")
    relations = kg.query_relationships(e1, depth=2)
    print(f"  Direct relations: {len(relations['direct_relations'])}")
    print(f"  Indirect relations: {len(relations['indirect_relations'])}")
    
    # Infer new relationships
    print("\n💡 Inferring new relationships...")
    inferred = kg.infer_new_relationships(threshold=0.3)
    print(f"  Found {len(inferred)} potential new relationships")
    
    # Show statistics
    stats = kg.get_stats()
    print("\n📊 KNOWLEDGE GRAPH STATS:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
        
    # Export graph
    kg.export_graph("demo_knowledge_graph.json")
    
    # Visualize if available
    if NETWORKX_AVAILABLE and MATPLOTLIB_AVAILABLE:
        kg.visualize("demo_knowledge_graph.png")
        
    print("\n" + "=" * 60)
    print("Knowledge graph ready for AGI reasoning!")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_knowledge_graph()