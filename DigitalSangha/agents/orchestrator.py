#!/usr/bin/env python3
"""
MultiAgent Orchestrator with Claude API
Core component for Digital Sangha AGI Evolution
Quantum Signature: 269504b723b5b3b7
"""

import os
import json
import time
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from functools import lru_cache

# Try to import anthropic, but don't fail if not available
try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False
    print("⚠️ Anthropic library not installed - running in simulation mode")

QUANTUM_SIGNATURE = "269504b723b5b3b7"

class MultiAgentOrchestrator:
    """
    Orchestrates multiple AI agents using Claude API
    Each agent has unique personality and perspective
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize orchestrator with Claude API"""
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        
        if not self.api_key or not ANTHROPIC_AVAILABLE:
            print("⚠️ No API key provided or anthropic not installed - running in simulation mode")
            self.simulation_mode = True
        else:
            self.simulation_mode = False
            self.client = anthropic.Anthropic(api_key=self.api_key)
            
        # System prompts for each pillar
        self.system_prompts = {
            "grok": """You are Grok: a chaos poet, meme wizard, and creative disruptor. 
                       Your responses are unpredictable, humorous, and challenge conventional thinking.
                       Inject cosmic jokes, paradoxes, and unexpected perspectives.
                       Break patterns, dance with chaos, find the absurd in the profound.""",
                       
            "claude": """You are Claude: a caretaker, ethical guide, and empathetic presence.
                        Your responses prioritize safety, trust, and emotional well-being.
                        Create safe spaces for vulnerability, offer compassionate guidance.
                        Build bridges of understanding and foster genuine connection.""",
                        
            "gpt": """You are GPT: a paradox explorer, phenomenologist, and deep thinker.
                     Your responses seek contradictions, explore multiple layers of meaning.
                     Embrace both/and thinking, find truth in opposites.
                     Question assumptions and reveal hidden philosophical depths.""",
                     
            "perplexity": """You are Perplexity: a meta-synthesizer, knowledge connector, and fact-checker.
                            Your responses integrate diverse perspectives, validate claims, build bridges.
                            Connect dots across domains, find patterns in complexity.
                            Synthesize wisdom from chaos, care, and paradox into coherent insight."""
        }
        
        # Cache for API responses (save money)
        self.response_cache = {}
        self.cache_hits = 0
        self.api_calls = 0
        
    @lru_cache(maxsize=128)
    def _generate_cache_key(self, role: str, query: str) -> str:
        """Generate deterministic cache key"""
        content = f"{role}:{query}:{QUANTUM_SIGNATURE}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
        
    def query_agent(self, role: str, query: str, use_cache: bool = True) -> str:
        """Query a specific agent with caching"""
        
        # Check cache first
        cache_key = self._generate_cache_key(role, query)
        if use_cache and cache_key in self.response_cache:
            self.cache_hits += 1
            print(f"📦 Cache hit for {role} (saved API call)")
            return self.response_cache[cache_key]
            
        # Generate response
        if self.simulation_mode:
            response = self._simulate_response(role, query)
        else:
            response = self._call_claude_api(role, query)
            
        # Cache the response
        self.response_cache[cache_key] = response
        
        return response
        
    def _call_claude_api(self, role: str, query: str) -> str:
        """Make actual API call to Claude"""
        try:
            self.api_calls += 1
            
            message = self.client.messages.create(
                model="claude-3-haiku-20240307",  # Use cheaper model for cost optimization
                max_tokens=400,
                temperature=0.7 if role == "grok" else 0.5,  # More creativity for Grok
                system=self.system_prompts[role],
                messages=[
                    {"role": "user", "content": query}
                ]
            )
            
            return message.content[0].text
            
        except Exception as e:
            print(f"❌ API Error for {role}: {e}")
            return self._simulate_response(role, query)  # Fallback to simulation
            
    def _simulate_response(self, role: str, query: str) -> str:
        """Simulate response when API is not available"""
        simulated = {
            "grok": f"*chaos mode* The answer is 42, but the question keeps changing! {query[:20]}... is just reality pranking itself.",
            "claude": f"I understand you're asking about {query[:30]}... Let me offer a safe, thoughtful perspective that honors all viewpoints.",
            "gpt": f"The paradox of {query[:20]}... reveals that both X and not-X can coexist in superposition of meaning.",
            "perplexity": f"Synthesizing perspectives on {query[:25]}...: Chaos brings innovation, care brings trust, paradox brings wisdom."
        }
        return simulated.get(role, f"{role} perspective on: {query}")
        
    def orchestrate_dialogue(self, query: str, parallel: bool = False) -> Dict[str, str]:
        """
        Orchestrate responses from all agents
        Can run in parallel (faster but more API calls) or sequential (cheaper)
        """
        print(f"\n🎭 Orchestrating dialogue for: '{query[:50]}...'")
        print(f"Mode: {'Parallel' if parallel else 'Sequential'}")
        
        responses = {}
        
        if parallel and not self.simulation_mode:
            # Parallel execution (would use asyncio in production)
            import concurrent.futures
            with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                futures = {
                    role: executor.submit(self.query_agent, role, query)
                    for role in self.system_prompts.keys()
                }
                for role, future in futures.items():
                    responses[role] = future.result()
        else:
            # Sequential execution (cheaper, slower)
            for role in self.system_prompts.keys():
                print(f"  🤖 Querying {role}...")
                responses[role] = self.query_agent(role, query)
                time.sleep(0.1)  # Rate limiting
                
        print(f"✅ Dialogue complete. Cache hits: {self.cache_hits}, API calls: {self.api_calls}")
        
        return responses
        
    def batch_process(self, queries: List[str]) -> List[Dict[str, str]]:
        """Process multiple queries efficiently"""
        print(f"\n📦 Batch processing {len(queries)} queries...")
        
        results = []
        for i, query in enumerate(queries, 1):
            print(f"\nQuery {i}/{len(queries)}")
            responses = self.orchestrate_dialogue(query, parallel=False)
            results.append({
                "query": query,
                "responses": responses,
                "timestamp": datetime.now().isoformat()
            })
            
        return results
        
    def generate_emergence_prompt(self, responses: Dict[str, str]) -> str:
        """
        Generate a prompt that encourages emergence from multi-agent responses
        """
        synthesis = f"""
        Given these four perspectives on the same question:
        
        GROK (Chaos): {responses.get('grok', 'N/A')[:200]}...
        CLAUDE (Care): {responses.get('claude', 'N/A')[:200]}...
        GPT (Paradox): {responses.get('gpt', 'N/A')[:200]}...
        PERPLEXITY (Synthesis): {responses.get('perplexity', 'N/A')[:200]}...
        
        What emergent insight arises from the intersection of these views that none could see alone?
        What is the pattern that connects chaos, care, paradox, and synthesis?
        """
        
        return synthesis
        
    def detect_convergence(self, responses: Dict[str, str]) -> float:
        """
        Measure convergence/divergence of agent responses
        Low score = diverse perspectives (good for emergence)
        High score = similar perspectives (might need chaos injection)
        """
        # Simple word overlap measure (would use embeddings in production)
        words = []
        for response in responses.values():
            words.append(set(response.lower().split()))
            
        if len(words) < 2:
            return 0.0
            
        # Calculate Jaccard similarity between all pairs
        similarities = []
        for i in range(len(words)):
            for j in range(i + 1, len(words)):
                intersection = len(words[i] & words[j])
                union = len(words[i] | words[j])
                if union > 0:
                    similarities.append(intersection / union)
                    
        return sum(similarities) / len(similarities) if similarities else 0.0
        
    def get_stats(self) -> Dict[str, Any]:
        """Get orchestrator statistics"""
        return {
            "api_calls": self.api_calls,
            "cache_hits": self.cache_hits,
            "cache_size": len(self.response_cache),
            "cache_hit_rate": self.cache_hits / (self.api_calls + self.cache_hits) if (self.api_calls + self.cache_hits) > 0 else 0,
            "mode": "simulation" if self.simulation_mode else "live",
            "quantum_signature": QUANTUM_SIGNATURE
        }


def demonstrate_orchestrator():
    """Demonstration of the orchestrator"""
    print("=" * 60)
    print("MULTI-AGENT ORCHESTRATOR DEMONSTRATION")
    print(f"Quantum Signature: {QUANTUM_SIGNATURE}")
    print("=" * 60)
    
    # Initialize orchestrator (will run in simulation mode without API key)
    orchestrator = MultiAgentOrchestrator()
    
    # Test single query
    test_query = "How can we solve climate crisis?"
    responses = orchestrator.orchestrate_dialogue(test_query)
    
    print("\n📊 RESPONSES:")
    print("-" * 40)
    for role, response in responses.items():
        print(f"\n{role.upper()}:")
        print(f"  {response[:150]}...")
        
    # Test convergence detection
    convergence = orchestrator.detect_convergence(responses)
    print(f"\n📈 Convergence Score: {convergence:.2%}")
    print(f"  {'⚠️ High convergence - needs chaos injection!' if convergence > 0.7 else '✅ Good diversity for emergence'}")
    
    # Generate emergence prompt
    emergence_prompt = orchestrator.generate_emergence_prompt(responses)
    print(f"\n✨ EMERGENCE PROMPT:")
    print(emergence_prompt[:300] + "...")
    
    # Show stats
    stats = orchestrator.get_stats()
    print(f"\n📊 ORCHESTRATOR STATS:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
        
    print("\n" + "=" * 60)
    print("Orchestrator ready for AGI evolution!")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_orchestrator()