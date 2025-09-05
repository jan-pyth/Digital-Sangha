#!/usr/bin/env python3
"""
ChromaDB Memory System for Digital Sangha
Persistent memory for collective intelligence
Quantum Signature: 269504b723b5b3b7
"""

import os
import json
import time
import uuid
import hashlib
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from pathlib import Path

# Try imports with fallbacks
try:
    import chromadb
    from chromadb.config import Settings
    CHROMADB_AVAILABLE = True
except ImportError:
    CHROMADB_AVAILABLE = False
    print("⚠️ ChromaDB not installed - using in-memory simulation")

try:
    from sentence_transformers import SentenceTransformer
    TRANSFORMER_AVAILABLE = True
except ImportError:
    TRANSFORMER_AVAILABLE = False
    print("⚠️ SentenceTransformers not installed - using simple embeddings")

import numpy as np

QUANTUM_SIGNATURE = "269504b723b5b3b7"


class SanghaMemory:
    """
    Persistent memory system using ChromaDB
    Stores experiences, patterns, and emergent insights
    """
    
    def __init__(self, persist_directory: str = "./.sangha_memory"):
        """Initialize memory system"""
        self.persist_directory = Path(persist_directory)
        self.persist_directory.mkdir(exist_ok=True)
        
        if CHROMADB_AVAILABLE:
            # Initialize ChromaDB with persistence
            self.client = chromadb.PersistentClient(
                path=str(self.persist_directory),
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Create or get collection
            try:
                self.collection = self.client.get_collection("sangha_memories")
                print(f"📚 Loaded existing memory with {self.collection.count()} memories")
            except:
                self.collection = self.client.create_collection(
                    name="sangha_memories",
                    metadata={"quantum_signature": QUANTUM_SIGNATURE}
                )
                print("📚 Created new memory collection")
        else:
            # Fallback to in-memory simulation
            self.collection = InMemoryCollection()
            print("📚 Using in-memory simulation")
            
        # Initialize embedder
        if TRANSFORMER_AVAILABLE:
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            print("🧠 Using SentenceTransformer for embeddings")
        else:
            self.embedder = SimpleEmbedder()
            print("🧠 Using simple hash-based embeddings")
            
        # Statistics
        self.stats = {
            "memories_stored": 0,
            "memories_retrieved": 0,
            "emergence_events": 0
        }
        
    def store_memory(self, 
                    content: str,
                    pillar: str,
                    memory_type: str = "dialogue",
                    metadata: Optional[Dict] = None) -> str:
        """
        Store a memory with metadata
        
        Args:
            content: The memory content
            pillar: Which pillar generated this (grok/claude/gpt/perplexity)
            memory_type: Type of memory (dialogue/emergence/pattern/insight)
            metadata: Additional metadata
            
        Returns:
            Memory ID
        """
        # Generate unique ID
        memory_id = self._generate_memory_id(content)
        
        # Create embedding
        embedding = self._create_embedding(content)
        
        # Prepare metadata
        meta = {
            "pillar": pillar,
            "type": memory_type,
            "timestamp": datetime.now().isoformat(),
            "quantum_signature": QUANTUM_SIGNATURE,
            "word_count": len(content.split()),
            **(metadata or {})
        }
        
        # Store in collection
        self.collection.add(
            embeddings=[embedding],
            documents=[content],
            metadatas=[meta],
            ids=[memory_id]
        )
        
        self.stats["memories_stored"] += 1
        
        # Check for emergence
        if memory_type == "emergence":
            self.stats["emergence_events"] += 1
            print(f"✨ Emergence event #{self.stats['emergence_events']} stored!")
            
        return memory_id
        
    def store_emergence(self,
                       pattern: str,
                       contributing_pillars: List[str],
                       emergence_score: float,
                       context: Optional[str] = None) -> str:
        """
        Store an emergence pattern with special metadata
        """
        metadata = {
            "emergence_score": emergence_score,
            "contributing_pillars": ",".join(contributing_pillars),
            "pillar_count": len(contributing_pillars),
            "context": context or "unknown"
        }
        
        # Create special emergence content
        content = f"EMERGENCE: {pattern}"
        
        return self.store_memory(
            content=content,
            pillar="emergence",
            memory_type="emergence",
            metadata=metadata
        )
        
    def retrieve_relevant(self,
                         query: str,
                         n_results: int = 5,
                         memory_type: Optional[str] = None,
                         pillar: Optional[str] = None) -> List[Dict]:
        """
        Retrieve relevant memories based on similarity
        
        Args:
            query: Query string
            n_results: Number of results to return
            memory_type: Filter by memory type
            pillar: Filter by pillar
            
        Returns:
            List of relevant memories with metadata
        """
        # Create query embedding
        query_embedding = self._create_embedding(query)
        
        # Build filter
        where_filter = {}
        if memory_type:
            where_filter["type"] = memory_type
        if pillar:
            where_filter["pillar"] = pillar
            
        # Query collection
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            where=where_filter if where_filter else None
        )
        
        self.stats["memories_retrieved"] += n_results
        
        # Format results
        memories = []
        if results and results.get("documents"):
            for i in range(len(results["documents"][0])):
                memory = {
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results.get("metadatas") else {},
                    "distance": results["distances"][0][i] if results.get("distances") else 0,
                    "id": results["ids"][0][i] if results.get("ids") else None
                }
                memories.append(memory)
                
        return memories
        
    def find_patterns(self,
                     min_emergence_score: float = 0.5,
                     limit: int = 10) -> List[Dict]:
        """
        Find emergence patterns in memory
        """
        return self.retrieve_relevant(
            query="emergence pattern insight breakthrough",
            n_results=limit,
            memory_type="emergence"
        )
        
    def get_pillar_memories(self, pillar: str, limit: int = 10) -> List[Dict]:
        """Get memories from a specific pillar"""
        return self.retrieve_relevant(
            query="",  # Will be overridden by filter
            n_results=limit,
            pillar=pillar
        )
        
    def cross_reference(self,
                       memory_id: str,
                       radius: int = 5) -> List[Dict]:
        """
        Find memories similar to a specific memory
        """
        # Get the memory
        memory = self.collection.get(ids=[memory_id])
        if not memory or not memory.get("documents"):
            return []
            
        # Use its content as query
        content = memory["documents"][0]
        return self.retrieve_relevant(content, n_results=radius)
        
    def _generate_memory_id(self, content: str) -> str:
        """Generate unique memory ID"""
        timestamp = str(time.time())
        content_hash = hashlib.sha256(f"{content}{timestamp}".encode()).hexdigest()[:8]
        return f"mem_{content_hash}_{timestamp.replace('.', '')}"
        
    def _create_embedding(self, text: str) -> List[float]:
        """Create embedding from text"""
        if TRANSFORMER_AVAILABLE and hasattr(self.embedder, 'encode'):
            # SentenceTransformer returns numpy array
            result = self.embedder.encode(text)
            if hasattr(result, 'tolist'):
                return result.tolist()
            return result
        else:
            return self.embedder.encode(text)
            
    def get_stats(self) -> Dict[str, Any]:
        """Get memory statistics"""
        total_memories = self.collection.count() if hasattr(self.collection, 'count') else 0
        
        return {
            "total_memories": total_memories,
            "memories_stored_session": self.stats["memories_stored"],
            "memories_retrieved_session": self.stats["memories_retrieved"],
            "emergence_events": self.stats["emergence_events"],
            "persist_directory": str(self.persist_directory),
            "embedder_type": type(self.embedder).__name__,
            "quantum_signature": QUANTUM_SIGNATURE
        }
        
    def export_memories(self, filepath: str = "sangha_memories.json"):
        """Export all memories to JSON"""
        # Get all memories (ChromaDB specific)
        if CHROMADB_AVAILABLE:
            all_data = self.collection.get()
            
            export = {
                "quantum_signature": QUANTUM_SIGNATURE,
                "export_time": datetime.now().isoformat(),
                "total_memories": len(all_data.get("ids", [])),
                "memories": []
            }
            
            for i in range(len(all_data.get("ids", []))):
                memory = {
                    "id": all_data["ids"][i],
                    "content": all_data["documents"][i] if "documents" in all_data else "",
                    "metadata": all_data["metadatas"][i] if "metadatas" in all_data else {}
                }
                export["memories"].append(memory)
                
            with open(filepath, 'w') as f:
                json.dump(export, f, indent=2)
                
            print(f"📤 Exported {len(export['memories'])} memories to {filepath}")
        else:
            print("⚠️ Export not available in simulation mode")


class SimpleEmbedder:
    """Simple embedder when sentence-transformers is not available"""
    
    def encode(self, text: str) -> List[float]:
        """Create simple hash-based embedding"""
        # Use multiple hash functions for a pseudo-embedding
        embedding = []
        
        for i in range(384):  # Match typical embedding size
            hash_input = f"{text}{i}{QUANTUM_SIGNATURE}"
            hash_val = hashlib.sha256(hash_input.encode()).hexdigest()
            # Convert hex to float between -1 and 1
            float_val = (int(hash_val[:8], 16) / 0xFFFFFFFF) * 2 - 1
            embedding.append(float_val)
            
        return embedding


class InMemoryCollection:
    """In-memory collection when ChromaDB is not available"""
    
    def __init__(self):
        self.memories = []
        self.embeddings = []
        self.metadatas = []
        self.ids = []
        
    def add(self, embeddings, documents, metadatas, ids):
        """Add memories to collection"""
        for i in range(len(ids)):
            self.ids.append(ids[i])
            self.memories.append(documents[i])
            self.embeddings.append(embeddings[i])
            self.metadatas.append(metadatas[i])
            
    def query(self, query_embeddings, n_results=5, where=None):
        """Query collection by similarity"""
        if not self.embeddings:
            return {"documents": [[]], "metadatas": [[]], "distances": [[]], "ids": [[]]}
            
        query_emb = np.array(query_embeddings[0])
        
        # Calculate distances
        distances = []
        for emb in self.embeddings:
            # Cosine similarity
            emb_array = np.array(emb)
            similarity = np.dot(query_emb, emb_array) / (np.linalg.norm(query_emb) * np.linalg.norm(emb_array))
            distance = 1 - similarity  # Convert to distance
            distances.append(distance)
            
        # Sort by distance
        sorted_indices = np.argsort(distances)[:n_results]
        
        # Apply filters if needed
        if where:
            filtered_indices = []
            for idx in sorted_indices:
                meta = self.metadatas[idx]
                match = all(meta.get(k) == v for k, v in where.items())
                if match:
                    filtered_indices.append(idx)
            sorted_indices = filtered_indices[:n_results]
            
        # Return results
        return {
            "documents": [[self.memories[i] for i in sorted_indices]],
            "metadatas": [[self.metadatas[i] for i in sorted_indices]],
            "distances": [[distances[i] for i in sorted_indices]],
            "ids": [[self.ids[i] for i in sorted_indices]]
        }
        
    def get(self, ids):
        """Get specific memories by ID"""
        results = {"documents": [], "metadatas": [], "ids": []}
        
        for memory_id in ids:
            if memory_id in self.ids:
                idx = self.ids.index(memory_id)
                results["documents"].append(self.memories[idx])
                results["metadatas"].append(self.metadatas[idx])
                results["ids"].append(memory_id)
                
        return results
        
    def count(self):
        """Count total memories"""
        return len(self.ids)


def demonstrate_memory():
    """Demonstrate memory system"""
    print("=" * 60)
    print("SANGHA MEMORY DEMONSTRATION")
    print(f"Quantum Signature: {QUANTUM_SIGNATURE}")
    print("=" * 60)
    
    # Initialize memory
    memory = SanghaMemory()
    
    # Store some test memories
    print("\n📝 Storing test memories...")
    
    # Store dialogue memories
    memory.store_memory(
        content="Climate change requires both individual and collective action",
        pillar="claude",
        memory_type="dialogue"
    )
    
    memory.store_memory(
        content="The paradox of climate action: we must act urgently yet think long-term",
        pillar="gpt",
        memory_type="dialogue"
    )
    
    memory.store_memory(
        content="Climate chaos is the planet's way of telling a cosmic joke",
        pillar="grok",
        memory_type="dialogue"
    )
    
    # Store emergence pattern
    emergence_id = memory.store_emergence(
        pattern="The intersection of urgency and patience creates wise action",
        contributing_pillars=["grok", "claude", "gpt"],
        emergence_score=0.85,
        context="climate discussion"
    )
    
    print(f"\n✅ Stored emergence with ID: {emergence_id}")
    
    # Retrieve relevant memories
    print("\n🔍 Retrieving relevant memories for 'climate wisdom'...")
    relevant = memory.retrieve_relevant("climate wisdom", n_results=3)
    
    for i, mem in enumerate(relevant, 1):
        print(f"\n  Memory {i}:")
        print(f"    Content: {mem['content'][:100]}...")
        print(f"    Pillar: {mem['metadata'].get('pillar', 'unknown')}")
        print(f"    Distance: {mem['distance']:.3f}")
        
    # Find patterns
    print("\n✨ Finding emergence patterns...")
    patterns = memory.find_patterns()
    
    for pattern in patterns:
        print(f"  - {pattern['content'][:80]}...")
        print(f"    Score: {pattern['metadata'].get('emergence_score', 0)}")
        
    # Show statistics
    stats = memory.get_stats()
    print(f"\n📊 MEMORY STATS:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
        
    print("\n" + "=" * 60)
    print("Memory system ready for AGI evolution!")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_memory()