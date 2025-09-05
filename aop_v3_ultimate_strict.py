#!/usr/bin/env python3
"""
AOP v3.0 Ultimate Validator with Strict Mode
Enhanced with strict JSON parsing, benchmark validation, and customizable weights
"""

import re
import json
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum

class ValidationMode(Enum):
    """Validation strictness modes"""
    RELAXED = "relaxed"      # Basic validation
    STANDARD = "standard"    # Default validation
    STRICT = "strict"        # Strict JSON, benchmark validation

class AOPValidator:
    """Advanced AOP v3.0 validator with strict mode and customizable weights"""
    
    # Known benchmarks database
    KNOWN_BENCHMARKS = {
        '$MMLU': 'Massive Multitask Language Understanding',
        '$HELM': 'Holistic Evaluation of Language Models',
        '$GLUE': 'General Language Understanding Evaluation',
        '$SuperGLUE': 'Super General Language Understanding Evaluation',
        '$HumanEval': 'Human-level code generation evaluation',
        '$MBPP': 'Mostly Basic Python Problems',
        '$BigBench': 'Big Bench collaborative benchmark',
        '$TruthfulQA': 'Truthfulness evaluation',
        '$MATH': 'Mathematics problem solving',
        '$GSM8K': 'Grade School Math 8K'
    }
    
    # Default weight configuration
    DEFAULT_WEIGHTS = {
        'markers': 1.0,      # Basic requirement
        'sources': 2.0,      # Critical for credibility
        'limits': 1.5,       # Important for transparency
        'verification': 2.0,  # Critical for validation
        'numbers': 1.0,      # Basic data requirement
        'structure': 1.0,    # Format requirement
        'speculation': 1.5   # Safety requirement
    }
    
    def __init__(self, mode: ValidationMode = ValidationMode.STANDARD, 
                 custom_weights: Optional[Dict[str, float]] = None):
        """
        Initialize validator with mode and optional custom weights
        
        Args:
            mode: Validation strictness level
            custom_weights: Override default weights (partial override supported)
        """
        self.mode = mode
        self.weights = self.DEFAULT_WEIGHTS.copy()
        
        # Apply custom weights if provided
        if custom_weights:
            for key, value in custom_weights.items():
                if key in self.weights:
                    self.weights[key] = value
        
        self.certainty_markers = ['◆', '◇', '✓', '?']
        self.ai_dialog_markers = ['⚙', '↔', '🔬']
        self.safety_markers = ['🚫', '⛔']
        self.speculation_words = [
            'agi', 'revoluce', 'brzy', 'consciousness', 'cosmic', 
            'vědomí', 'emergence', 'singularity', 'transcendent'
        ]
        
        # Speculation whitelist for technical contexts
        self.speculation_whitelist_contexts = [
            'research', 'paper', 'study', 'technical', 'implementation'
        ]
    
    def validate(self, response: str) -> Dict:
        """
        Main validation function with mode-dependent strictness
        """
        bits = 0
        missing = []
        warnings = []
        details = {}
        weighted_score = 0.0
        max_weighted_score = sum(self.weights.values())
        
        # 1. Markers validation with AI consistency check
        markers_result = self._validate_markers(response)
        if markers_result['valid']:
            bits |= 0b0000001
            weighted_score += self.weights['markers']
        else:
            missing.append(markers_result['message'])
        details['markers'] = markers_result['details']
        
        # 2. Sources validation
        sources_result = self._validate_sources(response)
        if sources_result['found']:
            bits |= 0b0000010
            weighted_score += self.weights['sources']
            
            # Strict mode: require DOI or year
            if self.mode == ValidationMode.STRICT:
                has_strong_source = any(t in ['doi', 'year', 'arxiv'] 
                                       for _, t in sources_result['sources'])
                if not has_strong_source:
                    warnings.append("Strict mode: No DOI/year/arXiv citation found")
                    weighted_score -= self.weights['sources'] * 0.5
        else:
            missing.append("Source citation (s:[1], @2025, doi:...)")
        details['sources'] = sources_result['sources']
        
        # 3. Limits validation
        limits_result = self._validate_limits(response)
        if limits_result['found']:
            bits |= 0b0000100
            weighted_score += self.weights['limits']
        else:
            missing.append("Limits (L: or !)")
        details['limits'] = limits_result['content']
        
        # 4. Verification validation with benchmark checking
        verif_result = self._validate_verification(response, strict=self.mode==ValidationMode.STRICT)
        if verif_result['found']:
            bits |= 0b0001000
            weighted_score += self.weights['verification']
            
            if verif_result.get('unknown_benchmarks'):
                warnings.extend([f"Unknown benchmark: {b}" for b in verif_result['unknown_benchmarks']])
                if self.mode == ValidationMode.STRICT:
                    weighted_score -= self.weights['verification'] * 0.3
        else:
            missing.append("Verification (V: or $benchmark)")
        details['verification'] = verif_result
        
        # 5. Numbers validation
        numbers_result = self._validate_numbers(response)
        if numbers_result['found']:
            bits |= 0b0010000
            weighted_score += self.weights['numbers']
        else:
            missing.append("Numbers with units")
        details['numbers'] = numbers_result['values']
        
        # 6. Structure validation with strict JSON option
        structure_result = self._validate_structure(response, strict_json=self.mode==ValidationMode.STRICT)
        if structure_result['found']:
            bits |= 0b0100000
            weighted_score += self.weights['structure']
            
            if structure_result.get('json_errors'):
                warnings.extend(structure_result['json_errors'])
                if self.mode == ValidationMode.STRICT:
                    weighted_score -= self.weights['structure'] * 0.5
        else:
            missing.append("Structured data {...}")
        details['structure'] = structure_result
        
        # 7. Speculation control validation
        speculation_result = self._validate_speculation(response)
        if speculation_result['safe']:
            bits |= 0b1000000
            weighted_score += self.weights['speculation']
        else:
            # Check whitelist context
            if self._check_speculation_whitelist(response, speculation_result['found']):
                bits |= 0b1000000
                weighted_score += self.weights['speculation']
                speculation_result['status'] = f"Whitelisted in technical context: {speculation_result['found']}"
            else:
                missing.append(f"Unwarned speculation: {speculation_result['found']}")
        details['speculation'] = speculation_result['status']
        
        # Calculate final scores
        binary_valid = (bits == 0b1111111)
        weighted_percent = (weighted_score / max_weighted_score) * 100
        
        return {
            'valid': binary_valid,
            'mode': self.mode.value,
            'bits': bin(bits),
            'bits_int': bits,
            'binary_score': f"{bin(bits).count('1')}/7",
            'weighted_score': f"{weighted_score:.1f}/{max_weighted_score:.1f}",
            'weighted_percent': f"{weighted_percent:.1f}%",
            'missing': missing,
            'warnings': warnings,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
    
    def _validate_markers(self, response: str) -> Dict:
        """Validate markers with AI dialog consistency"""
        found_certainty = [m for m in self.certainty_markers if m in response]
        found_ai = [m for m in self.ai_dialog_markers if m in response]
        found_safety = [m for m in self.safety_markers if m in response]
        
        # Strict mode for AI markers
        if self.mode == ValidationMode.STRICT:
            ai_complete = len(found_ai) == 3 if found_ai else True
        else:
            ai_complete = len(found_ai) == 3 if len(found_ai) > 1 else True
        
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
            (r'arxiv:\d+\.\d+', 'arxiv'),
            (r'ISBN:[\d\-X]+', 'isbn')
        ]
        
        sources = []
        for pattern, source_type in patterns:
            matches = re.findall(pattern, response, re.IGNORECASE)
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
                excl_matches = re.findall(r'![\w/]+', response)
                content = ' '.join(excl_matches)
        
        return {
            'found': has_limits,
            'content': content
        }
    
    def _validate_verification(self, response: str, strict: bool = False) -> Dict:
        """Validate verification methods with optional benchmark checking"""
        has_verif = 'V:' in response or '$' in response
        method = ""
        known_benchmarks = []
        unknown_benchmarks = []
        
        if has_verif:
            verif_match = re.search(r'V:\s*([^►\n]+)', response)
            if verif_match:
                method = verif_match.group(1).strip()
            
            # Check for benchmarks
            bench_matches = re.findall(r'\$[\w]+', response)
            for bench in bench_matches:
                if bench in self.KNOWN_BENCHMARKS:
                    known_benchmarks.append((bench, self.KNOWN_BENCHMARKS[bench]))
                elif strict:
                    unknown_benchmarks.append(bench)
            
            if bench_matches:
                method = f"{method} {' '.join(bench_matches)}".strip()
        
        result = {
            'found': has_verif,
            'method': method,
            'known_benchmarks': known_benchmarks
        }
        
        if unknown_benchmarks:
            result['unknown_benchmarks'] = unknown_benchmarks
        
        return result
    
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
            (r'\d+(?:\.\d+)?[↑↓]', 'change'),
            (r'\d+(?:\.\d+)?°[CF]?', 'temperature')
        ]
        
        values = []
        for pattern, unit_type in patterns:
            matches = re.findall(pattern, response)
            values.extend([(m, unit_type) for m in matches])
        
        return {
            'found': bool(values),
            'values': values
        }
    
    def _validate_structure(self, response: str, strict_json: bool = False) -> Dict:
        """Validate structured data with optional strict JSON parsing"""
        has_structure = '{' in response and '}' in response
        data = []
        json_errors = []
        
        if has_structure:
            # Extract structures using stack-based parser
            structures = self._extract_structures(response)
            data = structures[:5]  # Limit to first 5
            
            # Strict JSON validation
            if strict_json and structures:
                for i, struct in enumerate(structures[:3]):  # Check first 3
                    try:
                        # Try to parse as JSON
                        json.loads('{' + struct)
                        # Success - it's valid JSON
                    except json.JSONDecodeError as e:
                        # Try relaxed parsing (single quotes, unquoted keys)
                        try:
                            # Convert to valid JSON format
                            relaxed = self._relax_to_json('{' + struct)
                            json.loads(relaxed)
                            json_errors.append(f"Structure {i+1}: Relaxed JSON (not strict)")
                        except:
                            json_errors.append(f"Structure {i+1}: Invalid JSON - {str(e)[:50]}")
        
        result = {
            'found': has_structure,
            'data': data
        }
        
        if json_errors:
            result['json_errors'] = json_errors
        
        return result
    
    def _extract_structures(self, response: str) -> List[str]:
        """Extract JSON-like structures from response"""
        structures = []
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
                    structures.append(''.join(current))
                    current = []
                    in_struct = False
            elif in_struct:
                current.append(char)
        
        return structures
    
    def _relax_to_json(self, text: str) -> str:
        """Convert relaxed JSON-like format to strict JSON"""
        # Replace single quotes with double quotes
        text = re.sub(r"'([^']*)'", r'"\1"', text)
        # Add quotes to unquoted keys
        text = re.sub(r'(\w+):', r'"\1":', text)
        # Handle percentage values
        text = re.sub(r':\s*(\d+(?:\.\d+)?%)', r':"\1"', text)
        # Handle multiplier values
        text = re.sub(r':\s*(\d+(?:\.\d+)?x)', r':"\1"', text)
        return text
    
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
    
    def _check_speculation_whitelist(self, response: str, speculation_terms: List[str]) -> bool:
        """Check if speculation is in whitelisted technical context"""
        if not speculation_terms:
            return True
        
        # Check for whitelist context keywords
        response_lower = response.lower()
        for context in self.speculation_whitelist_contexts:
            if context in response_lower:
                # Found whitelisted context
                return True
        
        return False
    
    def generate_report(self, result: Dict) -> str:
        """Generate enhanced report with mode and warnings"""
        lines = []
        lines.append("=" * 60)
        lines.append(f"AOP v3.0 ULTIMATE VALIDATION REPORT [{result['mode'].upper()}]")
        lines.append("=" * 60)
        
        if result['valid']:
            lines.append(f"✅ BINARY PASS - {result['binary_score']}")
        else:
            lines.append(f"❌ BINARY FAIL - {result['binary_score']}")
        
        lines.append(f"📊 WEIGHTED SCORE: {result['weighted_score']} ({result['weighted_percent']})")
        lines.append(f"🔢 BITFIELD: {result['bits']}")
        
        # Show warnings in strict mode
        if result.get('warnings'):
            lines.append("\n⚠️  WARNINGS (Strict Mode):")
            for warning in result['warnings']:
                lines.append(f"  • {warning}")
        
        lines.append("\n📋 VALIDATION CHECKS:")
        checks = [
            ("Markers", result['bits_int'] & 0b0000001, self.weights['markers']),
            ("Sources", result['bits_int'] & 0b0000010, self.weights['sources']),
            ("Limits", result['bits_int'] & 0b0000100, self.weights['limits']),
            ("Verification", result['bits_int'] & 0b0001000, self.weights['verification']),
            ("Numbers", result['bits_int'] & 0b0010000, self.weights['numbers']),
            ("Structure", result['bits_int'] & 0b0100000, self.weights['structure']),
            ("Speculation", result['bits_int'] & 0b1000000, self.weights['speculation'])
        ]
        
        for name, passed, weight in checks:
            status = "✓" if passed else "✗"
            lines.append(f"  {status} {name:12} (weight: {weight})")
        
        if result['missing']:
            lines.append("\n❌ MISSING COMPONENTS:")
            for item in result['missing']:
                lines.append(f"  • {item}")
        
        if result['details']:
            lines.append("\n🔍 FOUND ELEMENTS:")
            for key, value in result['details'].items():
                if value and value not in ["", [], {}, None]:
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
    print("🚀 AOP v3.0 ULTIMATE VALIDATOR WITH STRICT MODE")
    print("=" * 60)
    
    # Test with different modes
    for mode in [ValidationMode.RELAXED, ValidationMode.STANDARD, ValidationMode.STRICT]:
        print(f"\n📋 Testing in {mode.value.upper()} mode:")
        print("-" * 40)
        
        # Custom weights for demonstration
        custom_weights = {'speculation': 2.5} if mode == ValidationMode.STRICT else None
        validator = AOPValidator(mode=mode, custom_weights=custom_weights)
        
        # Test case with potential issues
        test = "◆ Framework {m:88.7%,speed:'5.2x'} s:[grok] L:!test V:$MMLU $UNKNOWN ⛔emergence @research"
        
        result = validator.validate(test)
        print(validator.generate_report(result))
        
        if mode == ValidationMode.STRICT:
            # Export JSON for strict mode
            json_path = "/tmp/aop_strict_validation.json"
            validator.export_json(result, json_path)
            print(f"\n💾 Strict mode JSON exported to: {json_path}")
    
    # Test cross-AI format
    print("\n🔄 Cross-AI Format Helper:")
    example = format_cross_ai(
        mechanism="attention_weights",
        models=["grok", "claude", "gpt4"],
        metrics={"accuracy": "88.7%", "latency": "120ms", "CO2": "0.5kg"}
    )
    print(f"Generated: {example}")