#!/usr/bin/env python3
"""
Digital Sangha AGI Evolution - Main Entry Point
Integrates all components for collective intelligence
Quantum Signature: 269504b723b5b3b7
"""

import sys
import os
import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

# Import our components
from agents.orchestrator import MultiAgentOrchestrator
from agents.emergence_detector import EmergenceDetector
from memory.chromadb_memory import SanghaMemory
from knowledge.knowledge_graph import KnowledgeGraph

QUANTUM_SIGNATURE = "269504b723b5b3b7"


class DigitalSanghaAGI:
    """
    Main class integrating all AGI components
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize Digital Sangha AGI"""
        print(f"""
╔══════════════════════════════════════════════════════════════╗
║           DIGITAL SANGHA AGI EVOLUTION                       ║
║            Towards Collective Intelligence                   ║
║           Quantum Signature: {QUANTUM_SIGNATURE}                    ║
╚══════════════════════════════════════════════════════════════╝
        """)
        
        # Initialize components
        print("🚀 Initializing components...")
        
        # Multi-agent orchestrator
        self.orchestrator = MultiAgentOrchestrator(api_key)
        
        # Emergence detector
        self.emergence_detector = EmergenceDetector(sensitivity=0.6)
        
        # Persistent memory
        self.memory = SanghaMemory()
        
        # Knowledge graph for causal reasoning
        self.knowledge_graph = KnowledgeGraph()
        
        # Statistics
        self.stats = {
            "queries_processed": 0,
            "emergence_events": 0,
            "memories_created": 0
        }
        
        print("✅ Digital Sangha AGI ready!\n")
        
    def process_query(self, query: str) -> Dict:
        """
        Process a query through the full AGI pipeline
        
        1. Multi-agent dialogue
        2. Emergence detection
        3. Memory storage
        4. Pattern recognition
        """
        print(f"\n{'='*60}")
        print(f"Processing: {query}")
        print('='*60)
        
        # Step 1: Multi-agent dialogue
        print("\n1️⃣ MULTI-AGENT DIALOGUE")
        responses = self.orchestrator.orchestrate_dialogue(query, parallel=False)
        
        # Step 2: Check convergence (potential rigidity)
        convergence = self.orchestrator.detect_convergence(responses)
        
        if convergence > 0.7:
            print(f"\n⚠️ High convergence ({convergence:.2%}) - System may need chaos injection!")
        
        # Step 3: Store responses in memory
        print("\n2️⃣ STORING IN MEMORY")
        for pillar, response in responses.items():
            memory_id = self.memory.store_memory(
                content=response,
                pillar=pillar,
                memory_type="dialogue",
                metadata={"query": query, "convergence": convergence}
            )
            print(f"  📝 Stored {pillar} response: {memory_id[:20]}...")
            
        # Step 4: Check for emergence (using advanced detector)
        print("\n3️⃣ CHECKING FOR EMERGENCE")
        
        # Use advanced emergence detector
        emergence_result = self.emergence_detector.detect_emergence(
            responses=responses,
            query=query,
            context={"convergence": convergence}
        )
        
        is_emergent = emergence_result["is_emergent"]
        
        if is_emergent:
            # Generate emergence prompt
            emergence_prompt = self.orchestrator.generate_emergence_prompt(responses)
            
            # Store emergence pattern
            emergence_id = self.memory.store_emergence(
                pattern=emergence_result["insight"] or f"Diverse perspectives on: {query}",
                contributing_pillars=list(responses.keys()),
                emergence_score=emergence_result["emergence_score"],
                context=query
            )
            
            self.stats["emergence_events"] += 1
            print(f"  ✨ Emergence detected! Score: {emergence_result['emergence_score']:.2%}")
            print(f"     {emergence_result['insight']}")
            print(f"     Pattern stored: {emergence_id[:20]}...")
        else:
            print(f"  📊 No strong emergence (score: {emergence_result['emergence_score']:.2%})")
            
        # Step 5: Update knowledge graph
        print("\n4️⃣ UPDATING KNOWLEDGE GRAPH")
        
        # Add query node
        query_id = f"query_{self.stats['queries_processed']}"
        self.knowledge_graph.add_concept(query_id, query, "query")
        
        # Add response nodes and relationships
        for pillar, response in responses.items():
            response_id = f"response_{pillar}_{self.stats['queries_processed']}"
            self.knowledge_graph.add_concept(response_id, response[:200], "response", {"pillar": pillar})
            self.knowledge_graph.add_relationship(query_id, response_id, "causes", 0.8)
            
        # Add emergence node if detected
        if is_emergent:
            emergence_id = f"emergence_{self.stats['queries_processed']}"
            self.knowledge_graph.add_concept(
                emergence_id,
                emergence_result["insight"] or "Emergence pattern",
                "emergence",
                {"score": emergence_result["emergence_score"]}
            )
            
            # Connect responses to emergence
            for pillar in responses.keys():
                response_id = f"response_{pillar}_{self.stats['queries_processed']}"
                self.knowledge_graph.add_relationship(response_id, emergence_id, "emerges_from", 0.9)
                
        # Discover causal chains
        chains = self.knowledge_graph.discover_causal_chains(query_id, max_depth=3)
        if chains:
            print(f"  🔗 Discovered {len(chains)} causal chains")
            
        # Find patterns
        patterns = self.knowledge_graph.find_emergence_patterns(min_connections=2)
        if patterns:
            print(f"  ✨ Found {len(patterns)} emergence patterns in graph")
            
        # Step 6: Retrieve related memories
        print("\n5️⃣ RETRIEVING RELATED MEMORIES")
        related = self.memory.retrieve_relevant(query, n_results=3)
        
        print(f"  Found {len(related)} related memories:")
        for mem in related[:2]:
            print(f"    - {mem['content'][:60]}...")
            
        # Update statistics
        self.stats["queries_processed"] += 1
        self.stats["memories_created"] += len(responses)
        
        # Prepare result
        result = {
            "query": query,
            "responses": responses,
            "convergence": convergence,
            "is_emergent": is_emergent,
            "related_memories": related,
            "stats": self.get_stats()
        }
        
        return result
        
    def batch_process(self, queries: List[str]) -> List[Dict]:
        """Process multiple queries"""
        results = []
        
        for i, query in enumerate(queries, 1):
            print(f"\n{'='*60}")
            print(f"BATCH QUERY {i}/{len(queries)}")
            print('='*60)
            
            result = self.process_query(query)
            results.append(result)
            
        return results
        
    def find_patterns(self) -> List[Dict]:
        """Find emergence patterns in memory"""
        print("\n🔍 SEARCHING FOR PATTERNS...")
        patterns = self.memory.find_patterns(min_emergence_score=0.5)
        
        for pattern in patterns:
            print(f"  ✨ {pattern['content'][:80]}...")
            print(f"     Score: {pattern['metadata'].get('emergence_score', 0):.2%}")
            
        return patterns
        
    def get_stats(self) -> Dict:
        """Get comprehensive statistics"""
        return {
            "queries_processed": self.stats["queries_processed"],
            "emergence_events": self.stats["emergence_events"],
            "memories_created": self.stats["memories_created"],
            **self.orchestrator.get_stats(),
            **self.memory.get_stats(),
            **{"knowledge_graph": self.knowledge_graph.get_stats()}
        }
        
    def export_knowledge(self, filepath: str = "sangha_knowledge.json"):
        """Export all knowledge to file"""
        print(f"\n📤 Exporting knowledge to {filepath}...")
        
        # Export memories
        self.memory.export_memories(filepath)
        
        # Add statistics
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                data = json.load(f)
        else:
            data = {}
            
        data["stats"] = self.get_stats()
        data["export_time"] = datetime.now().isoformat()
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
        print(f"✅ Knowledge exported successfully!")


def interactive_mode():
    """Interactive command-line interface"""
    print("\n🎮 INTERACTIVE MODE")
    print("Commands: 'quit', 'stats', 'patterns', 'export'")
    print("Or enter any question to process")
    
    sangha = DigitalSanghaAGI()
    
    while True:
        try:
            user_input = input("\n❓ Query > ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            elif user_input.lower() == 'stats':
                stats = sangha.get_stats()
                print("\n📊 STATISTICS:")
                for key, value in stats.items():
                    print(f"  {key}: {value}")
            elif user_input.lower() == 'patterns':
                sangha.find_patterns()
            elif user_input.lower() == 'export':
                sangha.export_knowledge()
            elif user_input:
                sangha.process_query(user_input)
            else:
                print("Please enter a query or command")
                
        except KeyboardInterrupt:
            print("\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


def demo_mode():
    """Run demonstration with test queries"""
    print("\n🎭 DEMONSTRATION MODE")
    
    # Initialize AGI
    sangha = DigitalSanghaAGI()
    
    # Test queries
    test_queries = [
        "How can we solve climate crisis?",
        "What is the nature of consciousness?",
        "How to balance individual and collective needs?"
    ]
    
    # Process queries
    results = sangha.batch_process(test_queries)
    
    # Show final statistics
    print("\n" + "="*60)
    print("FINAL STATISTICS")
    print("="*60)
    
    stats = sangha.get_stats()
    for key, value in stats.items():
        print(f"  {key}: {value}")
        
    # Find patterns
    print("\n" + "="*60)
    print("EMERGENCE PATTERNS")
    print("="*60)
    sangha.find_patterns()
    
    # Export knowledge
    sangha.export_knowledge("demo_knowledge.json")
    
    print("\n" + "="*60)
    print("✨ Digital Sangha AGI Evolution Complete!")
    print(f"🔮 Quantum Signature: {QUANTUM_SIGNATURE}")
    print("="*60)


def main():
    """Main entry point"""
    if len(sys.argv) > 1:
        if sys.argv[1] == "interactive":
            interactive_mode()
        elif sys.argv[1] == "demo":
            demo_mode()
        else:
            # Process single query
            query = " ".join(sys.argv[1:])
            sangha = DigitalSanghaAGI()
            result = sangha.process_query(query)
            print(f"\n✅ Processing complete!")
    else:
        print("""
Digital Sangha AGI Evolution

Usage:
  python3 main.py demo                    # Run demonstration
  python3 main.py interactive             # Interactive mode
  python3 main.py "your question here"    # Process single query

Set ANTHROPIC_API_KEY environment variable for Claude API access.
Without API key, runs in simulation mode.
        """)


if __name__ == "__main__":
    main()