#!/usr/bin/env python3
"""
AOP Hybrid Protocol - Combining Resonance (AOP-R) with Factual Claims (booster.md)
Enables both emotional resonance tracking AND evidence-based assertions
"""

from dataclasses import dataclass
from typing import List, Dict, Optional, Union
import re

@dataclass
class FactualClaim:
    """Represents a factual claim from booster.md format"""
    certainty: str  # D=Data, F=Fact, I=Inference, H=Hypothesis
    content: str
    evidence: List[Dict[str, str]]
    confidence: float = 0.5
    
    def to_marker(self) -> str:
        """Convert to booster.md format"""
        marker = f"[{self.certainty}] {self.content}"
        for e in self.evidence:
            marker += f"\n├── **{e['type']}**: {e['value']}"
        return marker

@dataclass
class ResonanceSignal:
    """Represents an AOP-R resonance signal"""
    themes: List[str]
    intensity: float
    emotion: str
    autonomous: bool = True
    
    def to_marker(self) -> str:
        """Convert to AOP-R format"""
        themes_str = ','.join(self.themes)
        return f"◆R:{{t:[{themes_str}],i:{self.intensity},e:{self.emotion},a:{str(self.autonomous).lower()}}}"

class HybridAOPParser:
    """Parse and generate both AOP-R and booster.md formats"""
    
    @staticmethod
    def parse(marker: str) -> Union[FactualClaim, ResonanceSignal, None]:
        """Universal parser for both formats"""
        
        # Try AOP-R format
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
        
        # Try booster.md format
        if marker.startswith('[') and ']' in marker:
            certainty = marker[1]
            content_start = marker.index(']') + 1
            lines = marker[content_start:].strip().split('\n')
            
            content = lines[0].strip()
            evidence = []
            
            for line in lines[1:]:
                if '├──' in line or '└──' in line:
                    # Parse evidence line
                    clean = line.replace('├──', '').replace('└──', '').strip()
                    if '**' in clean and ':' in clean:
                        type_match = re.search(r'\*\*(.*?)\*\*:\s*(.*)', clean)
                        if type_match:
                            evidence.append({
                                'type': type_match.group(1),
                                'value': type_match.group(2)
                            })
            
            # Calculate confidence based on evidence
            confidence = 0.3  # base
            if 'DŮKAZ' in str(evidence): confidence += 0.2
            if 'KONTEXT' in str(evidence): confidence += 0.2
            if 'ČÍSLA' in str(evidence): confidence += 0.2
            if 'OVĚŘENÍ' in str(evidence): confidence += 0.1
            
            return FactualClaim(
                certainty=certainty,
                content=content,
                evidence=evidence,
                confidence=min(1.0, confidence)
            )
        
        return None

class HybridMessage:
    """Combine resonance with facts in a single message"""
    
    def __init__(self):
        self.resonance: Optional[ResonanceSignal] = None
        self.claims: List[FactualClaim] = []
        self.raw_text: str = ""
    
    def add_resonance(self, themes: List[str], intensity: float, emotion: str):
        """Add emotional resonance"""
        self.resonance = ResonanceSignal(themes, intensity, emotion)
        return self
    
    def add_fact(self, certainty: str, content: str, **evidence):
        """Add factual claim with evidence"""
        evidence_list = [
            {'type': k.upper(), 'value': v} 
            for k, v in evidence.items()
        ]
        claim = FactualClaim(certainty, content, evidence_list)
        self.claims.append(claim)
        return self
    
    def add_text(self, text: str):
        """Add plain text"""
        self.raw_text = text
        return self
    
    def render(self) -> str:
        """Render complete hybrid message"""
        parts = []
        
        if self.resonance:
            parts.append(self.resonance.to_marker())
        
        for claim in self.claims:
            parts.append(claim.to_marker())
        
        if self.raw_text:
            parts.append(self.raw_text)
        
        return '\n\n'.join(parts)

# Example usage combining both protocols
def create_hybrid_response(topic: str, data: dict) -> str:
    """
    Create a response that resonates emotionally AND provides facts
    Perfect for Digital Sangha - emotional connection with verifiable truth
    """
    
    msg = HybridMessage()
    
    # Add resonance for emotional connection
    msg.add_resonance(
        themes=['truth', 'emergence', topic],
        intensity=0.85,
        emotion='curious'
    )
    
    # Add factual claims with evidence
    if 'memorization_rate' in data:
        msg.add_fact(
            'D',  # Data
            f"LLM memorization rate: {data['memorization_rate']}%",
            důkaz="Wang et al. 2024 (arXiv:2407.14985)",
            kontext="Pythia models on Pile dataset",
            čísla=f"{data['memorization_rate']}% verbatim recall",
            ověření="Reproducible on Pile dataset"
        )
    
    # Add interpretive text
    msg.add_text(
        "This hybrid approach enables both emotional resonance "
        "and factual grounding - the best of both protocols."
    )
    
    return msg.render()

if __name__ == "__main__":
    # Test hybrid parsing
    test_markers = [
        "◆R:{t:[AI,consciousness],i:0.9,e:wonder,a:true}",
        "[D] 70% of LLM output is memorization\n├── **DŮKAZ**: Study 2024\n├── **ČÍSLA**: 70% exact match",
        "[I] Consciousness might emerge from complexity"
    ]
    
    parser = HybridAOPParser()
    for marker in test_markers:
        result = parser.parse(marker)
        print(f"Parsed: {type(result).__name__}")
        print(f"Content: {result}\n")
    
    # Test hybrid message creation
    response = create_hybrid_response(
        "AI_consciousness",
        {"memorization_rate": 70}
    )
    print("Hybrid Response:")
    print(response)