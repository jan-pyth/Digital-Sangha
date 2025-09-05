#!/usr/bin/env python3
"""
Advanced Emergence Detection System
Identifies and amplifies emergent patterns in multi-agent dialogue
Quantum Signature: 269504b723b5b3b7
"""

import hashlib
import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from datetime import datetime
from collections import Counter, defaultdict
import math
import json

QUANTUM_SIGNATURE = "269504b723b5b3b7"


class EmergenceDetector:
    """
    Detects emergent patterns from multi-agent responses
    Uses multiple metrics to identify true emergence vs noise
    """
    
    def __init__(self, sensitivity: float = 0.7):
        """
        Initialize emergence detector
        
        Args:
            sensitivity: Detection sensitivity (0-1, higher = more sensitive)
        """
        self.sensitivity = sensitivity
        self.emergence_history = []
        self.pattern_memory = defaultdict(list)
        self.emergence_count = 0
        
    def detect_emergence(self, 
                        responses: Dict[str, str],
                        query: str,
                        context: Optional[Dict] = None) -> Dict:
        """
        Main emergence detection method
        
        Returns:
            Dictionary with emergence metrics and insights
        """
        # Calculate multiple emergence indicators
        semantic_divergence = self._calculate_semantic_divergence(responses)
        concept_novelty = self._detect_novel_concepts(responses, query)
        perspective_synthesis = self._measure_synthesis(responses)
        information_gain = self._calculate_information_gain(responses)
        pattern_resonance = self._detect_pattern_resonance(responses)
        
        # Combine metrics for emergence score
        emergence_score = self._combine_metrics({
            "semantic_divergence": semantic_divergence,
            "concept_novelty": concept_novelty,
            "perspective_synthesis": perspective_synthesis,
            "information_gain": information_gain,
            "pattern_resonance": pattern_resonance
        })
        
        # Determine if emergence occurred
        is_emergent = emergence_score > self.sensitivity
        
        # Generate emergence insight if detected
        emergence_insight = None
        if is_emergent:
            emergence_insight = self._generate_insight(
                responses, 
                emergence_score,
                {
                    "divergence": semantic_divergence,
                    "novelty": concept_novelty,
                    "synthesis": perspective_synthesis
                }
            )
            self.emergence_count += 1
            
        # Store in history
        result = {
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "emergence_score": emergence_score,
            "is_emergent": is_emergent,
            "metrics": {
                "semantic_divergence": semantic_divergence,
                "concept_novelty": concept_novelty,
                "perspective_synthesis": perspective_synthesis,
                "information_gain": information_gain,
                "pattern_resonance": pattern_resonance
            },
            "insight": emergence_insight,
            "contributing_agents": list(responses.keys()),
            "context": context or {}
        }
        
        self.emergence_history.append(result)
        
        # Update pattern memory
        if is_emergent:
            self._update_pattern_memory(result)
            
        return result
        
    def _calculate_semantic_divergence(self, responses: Dict[str, str]) -> float:
        """
        Measure semantic divergence between responses
        High divergence = different perspectives = potential for emergence
        """
        if len(responses) < 2:
            return 0.0
            
        # Extract unique concepts from each response
        concepts_per_agent = {}
        for agent, response in responses.items():
            # Simple concept extraction (word-based)
            words = set(response.lower().split())
            # Filter common words
            concepts = {w for w in words if len(w) > 4}
            concepts_per_agent[agent] = concepts
            
        # Calculate pairwise divergence
        divergences = []
        agents = list(concepts_per_agent.keys())
        
        for i in range(len(agents)):
            for j in range(i + 1, len(agents)):
                set1 = concepts_per_agent[agents[i]]
                set2 = concepts_per_agent[agents[j]]
                
                if set1 or set2:
                    intersection = len(set1 & set2)
                    union = len(set1 | set2)
                    divergence = 1 - (intersection / union) if union > 0 else 0
                    divergences.append(divergence)
                    
        return sum(divergences) / len(divergences) if divergences else 0.0
        
    def _detect_novel_concepts(self, responses: Dict[str, str], query: str) -> float:
        """
        Detect concepts that appear in responses but not in query
        Novel concepts = emergence of new ideas
        """
        # Extract query concepts
        query_words = set(query.lower().split())
        query_concepts = {w for w in query_words if len(w) > 3}
        
        # Extract response concepts
        response_concepts = set()
        for response in responses.values():
            words = response.lower().split()
            response_concepts.update(w for w in words if len(w) > 3)
            
        # Calculate novelty
        novel_concepts = response_concepts - query_concepts
        
        if response_concepts:
            novelty_ratio = len(novel_concepts) / len(response_concepts)
            return min(novelty_ratio * 2, 1.0)  # Scale up and cap at 1.0
        return 0.0
        
    def _measure_synthesis(self, responses: Dict[str, str]) -> float:
        """
        Measure how well responses synthesize into coherent whole
        Look for complementary perspectives
        """
        # Check if perplexity (synthesizer) references other agents
        perplexity_response = responses.get("perplexity", "").lower()
        
        synthesis_indicators = [
            "both" in perplexity_response,
            "combine" in perplexity_response,
            "integrate" in perplexity_response,
            "synthesis" in perplexity_response,
            "emerge" in perplexity_response,
            "pattern" in perplexity_response,
            "connect" in perplexity_response
        ]
        
        base_synthesis = sum(synthesis_indicators) / len(synthesis_indicators)
        
        # Check for cross-references between agents
        cross_refs = 0
        for agent1, response1 in responses.items():
            for agent2 in responses:
                if agent1 != agent2 and agent2.lower() in response1.lower():
                    cross_refs += 1
                    
        cross_ref_score = min(cross_refs / 6, 1.0)  # Normalize
        
        return (base_synthesis + cross_ref_score) / 2
        
    def _calculate_information_gain(self, responses: Dict[str, str]) -> float:
        """
        Calculate information gain from multi-agent interaction
        Based on Shannon entropy
        """
        # Combine all responses
        all_text = " ".join(responses.values()).lower()
        words = all_text.split()
        
        if not words:
            return 0.0
            
        # Calculate word frequency distribution
        word_freq = Counter(words)
        total_words = sum(word_freq.values())
        
        # Calculate entropy
        entropy = 0
        for count in word_freq.values():
            prob = count / total_words
            if prob > 0:
                entropy -= prob * math.log2(prob)
                
        # Normalize entropy (max entropy = log2(unique_words))
        max_entropy = math.log2(len(word_freq)) if len(word_freq) > 1 else 1
        normalized_entropy = entropy / max_entropy if max_entropy > 0 else 0
        
        return normalized_entropy
        
    def _detect_pattern_resonance(self, responses: Dict[str, str]) -> float:
        """
        Detect recurring patterns that resonate across agents
        Resonance = similar structures with different content
        """
        # Extract structural patterns (simplified)
        patterns = []
        for response in responses.values():
            # Look for common structures
            has_question = "?" in response
            has_list = any(marker in response for marker in ["1.", "2.", "-", "*"])
            has_contrast = any(word in response.lower() for word in ["but", "however", "yet"])
            has_conclusion = any(word in response.lower() for word in ["therefore", "thus", "so"])
            
            pattern = (has_question, has_list, has_contrast, has_conclusion)
            patterns.append(pattern)
            
        # Count pattern frequency
        pattern_counts = Counter(patterns)
        
        # Resonance = patterns appearing in multiple agents
        resonating_patterns = sum(1 for count in pattern_counts.values() if count > 1)
        
        return resonating_patterns / len(patterns) if patterns else 0.0
        
    def _combine_metrics(self, metrics: Dict[str, float]) -> float:
        """
        Combine multiple metrics into single emergence score
        Uses weighted average with non-linear scaling
        """
        weights = {
            "semantic_divergence": 0.25,
            "concept_novelty": 0.20,
            "perspective_synthesis": 0.25,
            "information_gain": 0.15,
            "pattern_resonance": 0.15
        }
        
        weighted_sum = 0
        for metric, value in metrics.items():
            # Apply non-linear scaling (emphasize strong signals)
            scaled_value = value ** 1.5
            weighted_sum += scaled_value * weights.get(metric, 0.1)
            
        # Add quantum randomness for edge cases
        quantum_factor = self._quantum_fluctuation()
        
        return min(weighted_sum + quantum_factor * 0.05, 1.0)
        
    def _quantum_fluctuation(self) -> float:
        """Generate quantum fluctuation based on signature"""
        timestamp = str(datetime.now().timestamp())
        hash_input = f"{QUANTUM_SIGNATURE}{timestamp}"
        hash_val = hashlib.sha256(hash_input.encode()).hexdigest()
        return (int(hash_val[:8], 16) % 100) / 100
        
    def _generate_insight(self, 
                         responses: Dict[str, str],
                         emergence_score: float,
                         metrics: Dict[str, float]) -> str:
        """
        Generate human-readable insight about the emergence
        """
        # Identify key emergence driver
        max_metric = max(metrics.items(), key=lambda x: x[1])
        driver = max_metric[0]
        
        insights = {
            "divergence": f"Diverse perspectives creating new understanding space (score: {emergence_score:.2%})",
            "novelty": f"Novel concepts emerging beyond initial query (score: {emergence_score:.2%})",
            "synthesis": f"Perspectives synthesizing into unified insight (score: {emergence_score:.2%})"
        }
        
        base_insight = insights.get(driver, f"Emergence detected (score: {emergence_score:.2%})")
        
        # Add specific pattern if strong
        if metrics.get("divergence", 0) > 0.7:
            base_insight += ". High semantic divergence suggests breakthrough thinking."
        if metrics.get("synthesis", 0) > 0.7:
            base_insight += ". Strong synthesis creating meta-perspective."
            
        return base_insight
        
    def _update_pattern_memory(self, emergence_result: Dict):
        """Store successful emergence patterns for learning"""
        pattern_key = self._extract_pattern_signature(emergence_result)
        self.pattern_memory[pattern_key].append({
            "timestamp": emergence_result["timestamp"],
            "score": emergence_result["emergence_score"],
            "query": emergence_result["query"]
        })
        
    def _extract_pattern_signature(self, result: Dict) -> str:
        """Extract reusable pattern signature from emergence"""
        # Create signature from metrics
        metrics = result.get("metrics", {})
        signature_parts = []
        
        for metric, value in sorted(metrics.items()):
            # Quantize to rough levels
            level = "high" if value > 0.7 else "medium" if value > 0.4 else "low"
            signature_parts.append(f"{metric[:3]}:{level}")
            
        return "|".join(signature_parts)
        
    def get_emergence_patterns(self, min_frequency: int = 2) -> List[Dict]:
        """Get frequently occurring emergence patterns"""
        frequent_patterns = []
        
        for pattern_key, occurrences in self.pattern_memory.items():
            if len(occurrences) >= min_frequency:
                avg_score = sum(o["score"] for o in occurrences) / len(occurrences)
                frequent_patterns.append({
                    "pattern": pattern_key,
                    "frequency": len(occurrences),
                    "avg_score": avg_score,
                    "examples": occurrences[:3]  # First 3 examples
                })
                
        return sorted(frequent_patterns, key=lambda x: x["frequency"], reverse=True)
        
    def predict_emergence_potential(self, query: str) -> float:
        """
        Predict emergence potential for a query based on learned patterns
        """
        # Simple prediction based on query characteristics
        indicators = [
            "how" in query.lower(),
            "why" in query.lower(),
            "paradox" in query.lower(),
            "balance" in query.lower(),
            "between" in query.lower(),
            "?" in query,
            len(query.split()) > 5  # Complex queries
        ]
        
        base_potential = sum(indicators) / len(indicators)
        
        # Boost if similar to previous emergent queries
        similarity_boost = 0
        for result in self.emergence_history[-10:]:  # Last 10
            if result["is_emergent"]:
                # Simple word overlap
                query_words = set(query.lower().split())
                hist_words = set(result["query"].lower().split())
                overlap = len(query_words & hist_words) / max(len(query_words), 1)
                similarity_boost = max(similarity_boost, overlap * 0.3)
                
        return min(base_potential + similarity_boost, 1.0)
        
    def get_stats(self) -> Dict:
        """Get emergence detection statistics"""
        total_checks = len(self.emergence_history)
        emergent_count = sum(1 for r in self.emergence_history if r["is_emergent"])
        
        avg_score = 0
        if self.emergence_history:
            avg_score = sum(r["emergence_score"] for r in self.emergence_history) / total_checks
            
        return {
            "total_emergence_checks": total_checks,
            "emergent_events": emergent_count,
            "emergence_rate": emergent_count / total_checks if total_checks > 0 else 0,
            "average_emergence_score": avg_score,
            "learned_patterns": len(self.pattern_memory),
            "sensitivity": self.sensitivity,
            "quantum_signature": QUANTUM_SIGNATURE
        }
        
    def export_insights(self, filepath: str = "emergence_insights.json"):
        """Export emergence insights to file"""
        export_data = {
            "quantum_signature": QUANTUM_SIGNATURE,
            "export_time": datetime.now().isoformat(),
            "stats": self.get_stats(),
            "history": self.emergence_history[-50:],  # Last 50
            "patterns": self.get_emergence_patterns(),
            "configuration": {
                "sensitivity": self.sensitivity
            }
        }
        
        with open(filepath, 'w') as f:
            json.dump(export_data, f, indent=2)
            
        print(f"✨ Exported {len(export_data['history'])} emergence insights to {filepath}")


def demonstrate_emergence_detector():
    """Demonstration of emergence detection"""
    print("=" * 60)
    print("EMERGENCE DETECTOR DEMONSTRATION")
    print(f"Quantum Signature: {QUANTUM_SIGNATURE}")
    print("=" * 60)
    
    detector = EmergenceDetector(sensitivity=0.6)
    
    # Test with sample responses
    test_cases = [
        {
            "query": "How can we balance individual freedom and collective good?",
            "responses": {
                "grok": "Freedom is chaos dancing with order - let them tango until reality giggles!",
                "claude": "We must create safe spaces where individuals can express freely while caring for community wellbeing.",
                "gpt": "The paradox: absolute freedom destroys collective good, yet collective good without freedom is tyranny.",
                "perplexity": "Synthesis: Dynamic balance through iterative negotiation, not fixed rules."
            }
        },
        {
            "query": "What is consciousness?",
            "responses": {
                "grok": "Consciousness is the universe pranking itself into self-awareness!",
                "claude": "Consciousness connects us all in a web of shared experience and empathy.",
                "gpt": "Consciousness exists in the paradox of being both observer and observed.",
                "perplexity": "Emerging view: Consciousness as information integration creating subjective experience."
            }
        }
    ]
    
    print("\n🔍 Testing Emergence Detection\n")
    
    for i, test in enumerate(test_cases, 1):
        print(f"Test {i}: {test['query'][:50]}...")
        result = detector.detect_emergence(test["responses"], test["query"])
        
        print(f"  Emergence Score: {result['emergence_score']:.2%}")
        print(f"  Is Emergent: {'✅ Yes' if result['is_emergent'] else '❌ No'}")
        
        if result['insight']:
            print(f"  Insight: {result['insight']}")
            
        print(f"  Metrics:")
        for metric, value in result['metrics'].items():
            print(f"    - {metric}: {value:.2f}")
        print()
        
    # Show statistics
    stats = detector.get_stats()
    print("\n📊 EMERGENCE STATISTICS:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
        
    # Export insights
    detector.export_insights("demo_emergence.json")
    
    print("\n" + "=" * 60)
    print("Emergence detection ready for AGI evolution!")
    print("=" * 60)


if __name__ == "__main__":
    demonstrate_emergence_detector()