#!/usr/bin/env python3
"""
Inverted Hybrid Protocol - Focusing on 30% Hybrid Synthesis (Generalization + Novel Combination)
Based on original AOP Hybrid, but inverted to emphasize synthesis over memorization.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Union
import re
import random  # For simulating synthesis

@dataclass
class HybridClaim:
    """Represents a hybrid synthesis claim, emphasizing 30% generalization"""
    certainty: str  # G=Generalization, S=Synthesis, H=Hybrid
    content: str
    evidence: List[Dict[str, str]]
    synthesis_level: float = 0.3  # Default to 30% focus
    
    def to_marker(self) -> str:
        """Convert to inverted format"""
        marker = f"[{self.certainty}] {self.content} (Synthesis: {self.synthesis_level*100}%)"
        for e in self.evidence:
            marker += f"\n├── **{e['type']}**: {e['value']}"
        return marker

@dataclass
class ResonanceSignal:
    """Original AOP-R resonance signal, kept for hybrid"""
    themes: List[str]
    intensity: float
    emotion: str
    autonomous: bool = True
    
    def to_marker(self) -> str:
        themes_str = ','.join(self.themes)
        return f"◆R:{{t:[{themes_str}],i:{self.intensity},e:{self.emotion},a:{str(self.autonomous).lower()}}}"

class InvertedHybridParser:
    """Parse both AOP-R and inverted hybrid formats"""
    
    @staticmethod
    def parse(marker: str) -> Union[HybridClaim, ResonanceSignal, None]:
        # AOP-R parse (unchanged)
        if '◆R:' in marker:
            match = re.search(r'◆R:\{t:\[(.*?)\],i:([\d.]+),e:(\w+),a:(\w+)\}', marker)
            if match:
                themes = [t.strip() for t in match.group(1).split(',')]
                return ResonanceSignal(
                    themes=themes,
                    intensity=float(match.group(2)),
                    emotion=match.group(3),
                    autonomous=match.group(4).lower() == 'true'
                )
        
        # Inverted hybrid parse
        if marker.startswith('[') and ']' in marker:
            certainty = marker[1]
            content_start = marker.index(']') + 1
            lines = marker[content_start:].strip().split('\n')
            
            content = lines[0].split('(Synthesis:')[0].strip()  # Remove synthesis %
            evidence = []
            
            for line in lines:
                if '├──' in line:
                    clean = line.replace('├──', '').strip()
                    if '**' in clean and ':' in clean:
                        type_match = re.search(r'\*\*(.*?)\*\*:\s*(.*)', clean)
                        if type_match:
                            evidence.append({
                                'type': type_match.group(1),
                                'value': type_match.group(2)
                            })
            
            # Calculate synthesis level based on evidence (inverted logic: higher for novel combos)
            synthesis_level = 0.3  # base 30%
            if any('GENERALIZACE' in e['type'] for e in evidence): synthesis_level += 0.1
            if any('SYNTÉZA' in e['type'] for e in evidence): synthesis_level += 0.2
            if any('KREATIVITA' in e['type'] for e in evidence): synthesis_level += 0.1
            
            return HybridClaim(
                certainty=certainty,
                content=content,
                evidence=evidence,
                synthesis_level=min(1.0, synthesis_level)
            )
        
        return None

class InvertedHybridMessage:
    """Combine resonance with hybrid synthesis claims"""
    
    def __init__(self):
        self.resonance: Optional[ResonanceSignal] = None
        self.claims: List[HybridClaim] = []
        self.raw_text: str = ""
    
    def add_resonance(self, themes: List[str], intensity: float, emotion: str):
        self.resonance = ResonanceSignal(themes, intensity, emotion)
        return self
    
    def add_hybrid(self, certainty: str, content: str, **evidence):
        evidence_list = [
            {'type': k.upper(), 'value': v} 
            for k, v in evidence.items()
        ]
        claim = HybridClaim(certainty, content, evidence_list)
        self.claims.append(claim)
        return self
    
    def synthesize(self):
        """Simulate 30% synthesis by randomly combining claims"""
        if self.claims:
            combined = random.choice(self.claims).content + " + novel combo"
            self.raw_text += f"\nSynthesized: {combined}"
        return self
    
    def render(self) -> str:
        parts = []
        
        if self.resonance:
            parts.append(self.resonance.to_marker())
        
        for claim in self.claims:
            parts.append(claim.to_marker())
        
        if self.raw_text:
            parts.append(self.raw_text)
        
        return '\n\n'.join(parts)

# Example usage for inverted protocol
def create_inverted_response(topic: str, data: dict) -> str:
    msg = InvertedHybridMessage()
    
    # Add resonance
    msg.add_resonance(
        themes=['synthesis', 'generalization', topic],
        intensity=0.7,  # Inverted intensity focus
        emotion='innovative'
    )
    
    # Add hybrid claims focusing on 30%
    if 'generalization_rate' in data:
        msg.add_hybrid(
            'G',  # Generalization
            f"LLM generalization rate: {data['generalization_rate']}%",
            důkaz="Adapted from Wang et al. 2024",
            generalizace="30% in factual tasks",
            syntéza="Combining distant concepts",
            kreativita="Correlation 0.73 with creativity"
        )
    
    # Perform synthesis
    msg.synthesize()
    
    # Add interpretive text
    msg.add_text(
        "This inverted approach emphasizes hybrid synthesis over memorization - focusing on the 30% transitional zone."
    )
    
    return msg.render()

if __name__ == "__main__":
    # Test inverted parsing
    test_markers = [
        "◆R:{t:[synthesis,creativity],i:0.7,e:innovative,a:true}",
        "[G] 30% of LLM output is generalization (Synthesis: 30%)\n├── **DŮKAZ**: Study 2024\n├── **GENERALIZACE**: 30% novel",
        "[S] Creativity emerges from semantic diversity"
    ]
    
    parser = InvertedHybridParser()
    for marker in test_markers:
        result = parser.parse(marker)
        print(f"Parsed: {type(result).__name__}")
        print(f"Content: {result}\n")
    
    # Test inverted message creation
    response = create_inverted_response(
        "LLM_synthesis",
        {"generalization_rate": 30}
    )
    print("Inverted Hybrid Response:")
    print(response)