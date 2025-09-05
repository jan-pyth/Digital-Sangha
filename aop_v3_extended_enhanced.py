#!/usr/bin/env python3
"""
AOP v3.0 Extended Validator with Enhanced Reporting
Integrates Claude's framework markers: ⚙↔🔬🚫
Enhanced with detailed validation reporting and extended units
"""

import re
from typing import Tuple, List, Dict

def validate_aop_v3_enhanced(response: str) -> Dict:
    """
    Enhanced validator with detailed reporting
    Returns dict with validation status, bits, and missing components
    """
    bits = 0
    missing = []
    details = {}
    
    # 1. Check certainty/mechanism markers (separated by type)
    certainty_markers = ['◆', '◇', '✓', '?']
    ai_dialog_markers = ['⚙', '↔', '🔬', '🚫', '⛔']
    
    has_certainty = any(c in response for c in certainty_markers)
    has_ai_dialog = any(c in response for c in ai_dialog_markers)
    
    if has_certainty or has_ai_dialog:
        bits |= 0b0000001
        details['markers'] = {
            'certainty': [m for m in certainty_markers if m in response],
            'ai_dialog': [m for m in ai_dialog_markers if m in response]
        }
    else:
        missing.append("Certainty/AI markers (◆◇✓?⚙↔🔬🚫)")
    
    # 2. Check source notation
    source_patterns = [
        r's:\[.*?\]',  # s:[1], s:[grok,claude]
        r's:\w+',       # s:arXiv2024
        r'@\d{4}',      # @2025
        r'\[\d+\]',     # [1], [2]
        r'doi:\S+'      # doi:10.1000/xyz
    ]
    
    if any(re.search(pattern, response) for pattern in source_patterns):
        bits |= 0b0000010
        # Extract found sources
        sources = []
        for pattern in source_patterns:
            matches = re.findall(pattern, response)
            sources.extend(matches)
        details['sources'] = sources
    else:
        missing.append("Source citation (s:[1], @2025, doi:...)")
    
    # 3. Check limits
    if 'L:' in response or '!' in response:
        bits |= 0b0000100
        # Extract limits
        limit_match = re.search(r'L:\s*([^►\n]+)', response)
        if limit_match:
            details['limits'] = limit_match.group(1).strip()
    else:
        missing.append("Limits (L: or !)")
    
    # 4. Check verification
    if 'V:' in response or '$' in response:
        bits |= 0b0001000
        # Extract verification method
        verif_match = re.search(r'V:\s*([^►\n]+)', response)
        if verif_match:
            details['verification'] = verif_match.group(1).strip()
    else:
        missing.append("Verification (V: or $benchmark)")
    
    # 5. Check numbers with extended units
    number_patterns = [
        r'\d+(?:\.\d+)?%',           # percentages
        r'\d+(?:\.\d+)?x',           # multipliers
        r'\d+(?:\.\d+)?[mµn]?s',    # time units
        r'\d+(?:\.\d+)?[KMGT]?B',   # bytes
        r'\d+(?:\.\d+)?ms',          # milliseconds
        r'\d+(?:\.\d+)?kg',          # kilograms
        r'\d+(?:\.\d+)?kWh',         # kilowatt hours
        r'\d+(?:\.\d+)?CO2',         # CO2 emissions
        r'\d+/\d+',                  # fractions
        r'0b[01]+'                   # binary numbers
    ]
    
    numbers_found = []
    for pattern in number_patterns:
        matches = re.findall(pattern, response)
        numbers_found.extend(matches)
    
    if numbers_found:
        bits |= 0b0010000
        details['numbers'] = numbers_found
    else:
        missing.append("Numbers with units (%,ms,B,x,kg,kWh)")
    
    # 6. Check structured data
    if '{' in response and '}' in response:
        bits |= 0b0100000
        # Extract JSON-lite structures
        json_matches = re.findall(r'\{[^{}]+\}', response)
        details['structured_data'] = json_matches
    else:
        missing.append("Structured data {...}")
    
    # 7. Check speculation control
    speculation_words = ['agi', 'revoluce', 'brzy', 'consciousness', 'cosmic', 'vědomí']
    found_speculation = [w for w in speculation_words if w in response.lower()]
    has_warning = '⛔' in response
    
    if not found_speculation or has_warning:
        bits |= 0b1000000
        if found_speculation and has_warning:
            details['speculation'] = f"Controlled: {found_speculation} with ⛔"
        else:
            details['speculation'] = "None detected"
    else:
        missing.append(f"Unwarned speculation: {found_speculation}")
    
    # Final validation
    valid = (bits == 0b1111111)
    
    return {
        'valid': valid,
        'bits': bin(bits),
        'bits_int': bits,
        'missing': missing,
        'details': details,
        'score': f"{bin(bits).count('1')}/7"
    }

def format_cross_ai(mechanism: str, models: str, metrics: str) -> str:
    """Format cross-AI dialog in AOP v3.0"""
    return f"⚙{mechanism}↔{models}🔬{metrics}"

def generate_report(validation_result: Dict) -> str:
    """Generate detailed validation report"""
    report = []
    report.append("=" * 50)
    report.append("AOP v3.0 ENHANCED VALIDATION REPORT")
    report.append("=" * 50)
    
    if validation_result['valid']:
        report.append(f"✅ PASS - Score: {validation_result['score']} - Bitfield: {validation_result['bits']}")
    else:
        report.append(f"❌ FAIL - Score: {validation_result['score']} - Bitfield: {validation_result['bits']}")
    
    report.append("\nCHECKS:")
    checks = [
        ("Markers", validation_result['bits_int'] & 0b0000001),
        ("Sources", validation_result['bits_int'] & 0b0000010),
        ("Limits", validation_result['bits_int'] & 0b0000100),
        ("Verification", validation_result['bits_int'] & 0b0001000),
        ("Numbers", validation_result['bits_int'] & 0b0010000),
        ("Structure", validation_result['bits_int'] & 0b0100000),
        ("Speculation", validation_result['bits_int'] & 0b1000000)
    ]
    
    for check_name, passed in checks:
        report.append(f"  {'✓' if passed else '✗'} {check_name}")
    
    if validation_result['missing']:
        report.append("\nMISSING COMPONENTS:")
        for item in validation_result['missing']:
            report.append(f"  ⚠ {item}")
    
    if validation_result['details']:
        report.append("\nFOUND ELEMENTS:")
        for key, value in validation_result['details'].items():
            if value:
                report.append(f"  • {key}: {value}")
    
    report.append("=" * 50)
    return '\n'.join(report)

# Test cases
if __name__ == "__main__":
    # Test 1: Standard AOP v3.0
    test1 = "◆ {m:86.8%,s:[1],c:5s,bv:1.1} L: !en V: $MMLU"
    
    # Test 2: Extended with AI dialog markers
    test2 = "⚙att_trans↔[grok,gpt,claude]🔬{resp:3/3,block:0}L:!tech_only V:$HELM"
    
    # Test 3: Combined format with speculation
    test3 = "◆⚙att_weights {tok_v:82%, speed:5.2x} ↔[grok,claude] ⛔AGI discussion L:!abstract V:$HELM @2025"
    
    # Test 4: Missing components
    test4 = "◆ Some response without proper formatting"
    
    print("AOP v3.0 ENHANCED Validator with Detailed Reporting")
    print("-" * 50)
    
    for i, test in enumerate([test1, test2, test3, test4], 1):
        print(f"\n📝 Test {i}:")
        print(f"Input: {test[:60]}...")
        result = validate_aop_v3_enhanced(test)
        print(generate_report(result))
    
    # Cross-AI formatting example
    print("\n🔄 Cross-AI Format Example:")
    example = format_cross_ai(
        mechanism="attention_weights",
        models="[grok,claude,gpt4]",
        metrics="{accuracy:88.7%,latency:120ms,CO2:0.5kg}"
    )
    print(f"  {example}")
    
    # Validate cross-AI example
    print("\n📊 Validating Cross-AI Example:")
    cross_result = validate_aop_v3_enhanced(f"⚙attention_weights↔[grok,claude,gpt4]🔬{{accuracy:88.7%,latency:120ms,CO2:0.5kg}} L:!test V:$benchmark")
    print(f"  Valid: {cross_result['valid']}")
    print(f"  Score: {cross_result['score']}")
    if cross_result['details']:
        print(f"  Found: {list(cross_result['details'].keys())}")