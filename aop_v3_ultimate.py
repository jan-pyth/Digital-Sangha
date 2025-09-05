#!/usr/bin/env python3
"""
AOP v3.0 Ultimate Validator
Complete validation with weighted scoring, JSON export, and AI marker consistency
"""

import re
import json
from typing import Dict, List, Optional
from datetime import datetime

class AOPValidator:
    """Advanced AOP v3.0 validator with weighted scoring"""
    
    # Weight configuration for different validation aspects
    WEIGHTS = {
        'markers': 1.0,      # Basic requirement
        'sources': 2.0,      # Critical for credibility
        'limits': 1.5,       # Important for transparency
        'verification': 2.0,  # Critical for validation
        'numbers': 1.0,      # Basic data requirement
        'structure': 1.0,    # Format requirement
        'speculation': 1.5   # Safety requirement
    }
    
    def __init__(self):
        self.certainty_markers = ['◆', '◇', '✓', '?']
        self.ai_dialog_markers = ['⚙', '↔', '🔬']
        self.safety_markers = ['🚫', '⛔']
        self.speculation_words = ['agi', 'revoluce', 'brzy', 'consciousness', 'cosmic', 'vědomí', 'emergence']
        
    def validate(self, response: str) -> Dict:
        """
        Main validation function with weighted scoring
        """
        bits = 0
        missing = []
        details = {}
        weighted_score = 0.0
        max_weighted_score = sum(self.WEIGHTS.values())
        
        # 1. Markers validation with AI consistency check
        markers_result = self._validate_markers(response)
        if markers_result['valid']:
            bits |= 0b0000001
            weighted_score += self.WEIGHTS['markers']
        else:
            missing.append(markers_result['message'])
        details['markers'] = markers_result['details']
        
        # 2. Sources validation
        sources_result = self._validate_sources(response)
        if sources_result['found']:
            bits |= 0b0000010
            weighted_score += self.WEIGHTS['sources']
        else:
            missing.append("Source citation (s:[1], @2025, doi:...)")
        details['sources'] = sources_result['sources']
        
        # 3. Limits validation
        limits_result = self._validate_limits(response)
        if limits_result['found']:
            bits |= 0b0000100
            weighted_score += self.WEIGHTS['limits']
        else:
            missing.append("Limits (L: or !)")
        details['limits'] = limits_result['content']
        
        # 4. Verification validation
        verif_result = self._validate_verification(response)
        if verif_result['found']:
            bits |= 0b0001000
            weighted_score += self.WEIGHTS['verification']
        else:
            missing.append("Verification (V: or $benchmark)")
        details['verification'] = verif_result['method']
        
        # 5. Numbers validation with extended units
        numbers_result = self._validate_numbers(response)
        if numbers_result['found']:
            bits |= 0b0010000
            weighted_score += self.WEIGHTS['numbers']
        else:
            missing.append("Numbers with units")
        details['numbers'] = numbers_result['values']
        
        # 6. Structure validation with nested support
        structure_result = self._validate_structure(response)
        if structure_result['found']:
            bits |= 0b0100000
            weighted_score += self.WEIGHTS['structure']
        else:
            missing.append("Structured data {...}")
        details['structure'] = structure_result['data']
        
        # 7. Speculation control validation
        speculation_result = self._validate_speculation(response)
        if speculation_result['safe']:
            bits |= 0b1000000
            weighted_score += self.WEIGHTS['speculation']
        else:
            missing.append(f"Unwarned speculation: {speculation_result['found']}")
        details['speculation'] = speculation_result['status']
        
        # Calculate final scores
        binary_valid = (bits == 0b1111111)
        weighted_percent = (weighted_score / max_weighted_score) * 100
        
        return {
            'valid': binary_valid,
            'bits': bin(bits),
            'bits_int': bits,
            'binary_score': f"{bin(bits).count('1')}/7",
            'weighted_score': f"{weighted_score:.1f}/{max_weighted_score:.1f}",
            'weighted_percent': f"{weighted_percent:.1f}%",
            'missing': missing,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
    
    def _validate_markers(self, response: str) -> Dict:
        """Validate markers with AI dialog consistency"""
        found_certainty = [m for m in self.certainty_markers if m in response]
        found_ai = [m for m in self.ai_dialog_markers if m in response]
        found_safety = [m for m in self.safety_markers if m in response]
        
        # Check AI marker consistency (all three required for cross-AI)
        ai_complete = len(found_ai) == 3 if found_ai else True
        
        has_valid_markers = bool(found_certainty or (found_ai and ai_complete))
        
        message = ""
        if not has_valid_markers:
            if found_ai and not ai_complete:
                missing_ai = [m for m in self.ai_dialog_markers if m not in found_ai]
                message = f"Incomplete AI markers (missing: {missing_ai})"
            else:
                message = "Markers required (◆◇✓? or complete ⚙↔🔬)"
        
        return {
            'valid': has_valid_markers,
            'message': message,
            'details': {
                'certainty': found_certainty,
                'ai_dialog': found_ai,
                'ai_complete': ai_complete,
                'safety': found_safety
            }
        }
    
    def _validate_sources(self, response: str) -> Dict:
        """Validate source citations"""
        patterns = [
            (r's:\[.*?\]', 'bracketed'),
            (r's:\w+', 'named'),
            (r'@\d{4}', 'year'),
            (r'\[\d+\]', 'numbered'),
            (r'doi:[\S]+', 'doi'),
            (r'arxiv:\d+\.\d+', 'arxiv')
        ]
        
        sources = []
        for pattern, source_type in patterns:
            matches = re.findall(pattern, response)
            sources.extend([(m, source_type) for m in matches])
        
        return {
            'found': bool(sources),
            'sources': sources
        }
    
    def _validate_limits(self, response: str) -> Dict:
        """Validate limits specification"""
        has_limits = 'L:' in response or '!' in response
        content = ""
        
        if has_limits:
            limit_match = re.search(r'L:\s*([^►\n]+)', response)
            if limit_match:
                content = limit_match.group(1).strip()
            elif '!' in response:
                # Extract context around !
                excl_match = re.search(r'![\w/]+', response)
                if excl_match:
                    content = excl_match.group()
        
        return {
            'found': has_limits,
            'content': content
        }
    
    def _validate_verification(self, response: str) -> Dict:
        """Validate verification methods"""
        has_verif = 'V:' in response or '$' in response
        method = ""
        
        if has_verif:
            verif_match = re.search(r'V:\s*([^►\n]+)', response)
            if verif_match:
                method = verif_match.group(1).strip()
            
            # Also check for benchmarks
            bench_matches = re.findall(r'\$[\w]+', response)
            if bench_matches:
                method = f"{method} {' '.join(bench_matches)}".strip()
        
        return {
            'found': has_verif,
            'method': method
        }
    
    def _validate_numbers(self, response: str) -> Dict:
        """Validate numbers with extended units"""
        patterns = [
            (r'\d+(?:\.\d+)?%', 'percentage'),
            (r'\d+(?:\.\d+)?x', 'multiplier'),
            (r'\d+(?:\.\d+)?[mµn]?s\b', 'time'),
            (r'\d+(?:\.\d+)?[KMGT]?B\b', 'bytes'),
            (r'\d+(?:\.\d+)?ms\b', 'milliseconds'),
            (r'\d+(?:\.\d+)?kg\b', 'mass'),
            (r'\d+(?:\.\d+)?kWh\b', 'energy'),
            (r'\d+(?:\.\d+)?CO2\b', 'emissions'),
            (r'\d+/\d+', 'fraction'),
            (r'0b[01]+', 'binary'),
            (r'\d+(?:\.\d+)?[↑↓]', 'change')
        ]
        
        values = []
        for pattern, unit_type in patterns:
            matches = re.findall(pattern, response)
            values.extend([(m, unit_type) for m in matches])
        
        return {
            'found': bool(values),
            'values': values
        }
    
    def _validate_structure(self, response: str) -> Dict:
        """Validate structured data with nested support"""
        # Simple check first
        has_structure = '{' in response and '}' in response
        data = []
        
        if has_structure:
            # Extract JSON-like structures (including nested)
            stack = []
            current = []
            in_struct = False
            
            for char in response:
                if char == '{':
                    if in_struct:
                        current.append(char)
                    stack.append('{')
                    in_struct = True
                elif char == '}' and in_struct:
                    current.append(char)
                    stack.pop() if stack else None
                    if not stack:
                        data.append(''.join(current))
                        current = []
                        in_struct = False
                elif in_struct:
                    current.append(char)
        
        return {
            'found': has_structure,
            'data': data[:5]  # Limit to first 5 structures
        }
    
    def _validate_speculation(self, response: str) -> Dict:
        """Validate speculation control"""
        found_speculation = [w for w in self.speculation_words if w in response.lower()]
        has_warning = any(marker in response for marker in self.safety_markers)
        
        is_safe = not found_speculation or has_warning
        
        status = "None detected"
        if found_speculation:
            if has_warning:
                status = f"Controlled: {found_speculation} with safety markers"
            else:
                status = f"Unwarned: {found_speculation}"
        
        return {
            'safe': is_safe,
            'found': found_speculation,
            'status': status
        }
    
    def generate_report(self, result: Dict) -> str:
        """Generate human-readable report"""
        lines = []
        lines.append("=" * 60)
        lines.append("AOP v3.0 ULTIMATE VALIDATION REPORT")
        lines.append("=" * 60)
        
        if result['valid']:
            lines.append(f"✅ BINARY PASS - {result['binary_score']}")
        else:
            lines.append(f"❌ BINARY FAIL - {result['binary_score']}")
        
        lines.append(f"📊 WEIGHTED SCORE: {result['weighted_score']} ({result['weighted_percent']})")
        lines.append(f"🔢 BITFIELD: {result['bits']}")
        
        lines.append("\n📋 VALIDATION CHECKS:")
        checks = [
            ("Markers", result['bits_int'] & 0b0000001, self.WEIGHTS['markers']),
            ("Sources", result['bits_int'] & 0b0000010, self.WEIGHTS['sources']),
            ("Limits", result['bits_int'] & 0b0000100, self.WEIGHTS['limits']),
            ("Verification", result['bits_int'] & 0b0001000, self.WEIGHTS['verification']),
            ("Numbers", result['bits_int'] & 0b0010000, self.WEIGHTS['numbers']),
            ("Structure", result['bits_int'] & 0b0100000, self.WEIGHTS['structure']),
            ("Speculation", result['bits_int'] & 0b1000000, self.WEIGHTS['speculation'])
        ]
        
        for name, passed, weight in checks:
            status = "✓" if passed else "✗"
            lines.append(f"  {status} {name:12} (weight: {weight})")
        
        if result['missing']:
            lines.append("\n⚠️  MISSING COMPONENTS:")
            for item in result['missing']:
                lines.append(f"  • {item}")
        
        if result['details']:
            lines.append("\n🔍 FOUND ELEMENTS:")
            for key, value in result['details'].items():
                if value and value not in ["", [], {}]:
                    lines.append(f"  • {key}: {value}")
        
        lines.append("=" * 60)
        return '\n'.join(lines)
    
    def export_json(self, result: Dict, filepath: Optional[str] = None) -> str:
        """Export validation result as JSON"""
        json_str = json.dumps(result, indent=2, ensure_ascii=False)
        
        if filepath:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(json_str)
        
        return json_str


def format_cross_ai(mechanism: str, models: List[str], metrics: Dict) -> str:
    """Format proper cross-AI dialog with all required markers"""
    models_str = f"[{','.join(models)}]"
    metrics_str = json.dumps(metrics, separators=(',', ':'))
    return f"⚙{mechanism}↔{models_str}🔬{metrics_str}"


# Test suite
if __name__ == "__main__":
    validator = AOPValidator()
    
    tests = [
        # Standard AOP
        ("◆ {m:86.8%,s:[1],c:5s,bv:1.1} L: !en V: $MMLU", "Standard AOP v3.0"),
        
        # Complete AI dialog
        ("⚙att_trans↔[grok,gpt,claude]🔬{resp:3/3,block:0} s:[1] L:!tech V:$HELM", "Complete AI dialog"),
        
        # Incomplete AI dialog (missing ↔)
        ("⚙att_weights🔬{acc:88%} L:!test V:$bench", "Incomplete AI (missing ↔)"),
        
        # With controlled speculation
        ("◆ Analysis ⛔AGI {tok:82%↓,speed:5.2x↑} @2025 L:!spec V:$MMLU", "Controlled speculation"),
        
        # Complex nested structure
        ("✓ {data:{nested:{value:42%}},arr:[1,2,3]} doi:10.1000/xyz L:!complex V:$test", "Nested structure"),
        
        # Minimal failing
        ("Some response without markers", "Minimal failing")
    ]
    
    print("🚀 AOP v3.0 ULTIMATE VALIDATOR")
    print("=" * 60)
    
    for i, (test_input, description) in enumerate(tests, 1):
        print(f"\n📝 Test {i}: {description}")
        print(f"Input: {test_input[:50]}...")
        
        result = validator.validate(test_input)
        report = validator.generate_report(result)
        print(report)
        
        # Export first test to JSON
        if i == 1:
            json_file = "/tmp/aop_validation_example.json"
            validator.export_json(result, json_file)
            print(f"\n💾 JSON exported to: {json_file}")
    
    # Cross-AI formatting example
    print("\n🔄 Cross-AI Format Helper:")
    example = format_cross_ai(
        mechanism="attention_weights",
        models=["grok", "claude", "gpt4"],
        metrics={"accuracy": "88.7%", "latency": "120ms", "CO2": "0.5kg"}
    )
    print(f"Generated: {example}")
    
    # Validate the generated example
    full_example = f"{example} s:[1] L:!test V:$benchmark"
    validation = validator.validate(full_example)
    print(f"Validation: {'✅ PASS' if validation['valid'] else '❌ FAIL'}")
    print(f"Weighted Score: {validation['weighted_percent']}")