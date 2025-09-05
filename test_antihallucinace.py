#!/usr/bin/env python3
"""
Unit testy pro anti-halucinační validátor
Testuje všechny komponenty protokolu

Spuštění:
    pytest test_antihallucinace.py -v
    nebo
    python3 test_antihallucinace.py
"""

try:
    import pytest
    PYTEST_AVAILABLE = True
except ImportError:
    PYTEST_AVAILABLE = False
    
from antihallucinace_validator import (
    validate_100_percent,
    generate_report,
    format_claim,
    check_blocked,
    AntiHallucinationPipeline
)

class TestBlockedWords:
    """Testy pro detekci blokovaných slov"""
    
    def test_clean_text(self):
        """Text bez blokovaných slov by měl projít"""
        text = "Model dosahuje 85% přesnosti na datasetu."
        is_clean, violations = check_blocked(text)
        assert is_clean == True
        assert violations == []
    
    def test_blocked_agi(self):
        """AGI by mělo být detekováno"""
        text = "Tento model umožní AGI."
        is_clean, violations = check_blocked(text)
        assert is_clean == False
        assert "AGI" in violations
    
    def test_multiple_blocked(self):
        """Více blokovaných slov by mělo být detekováno"""
        text = "Brzy překonává všechny modely dramaticky."
        is_clean, violations = check_blocked(text)
        assert is_clean == False
        assert len(violations) >= 3
        assert "brzy" in [v.lower() for v in violations]

class TestCitationDetection:
    """Testy pro detekci citací"""
    
    def test_standard_citation(self):
        """Standardní citace 'Autor et al. 2020' """
        text = "[D] Model podle Devlin et al. 2019 dosahuje dobrých výsledků."
        result = validate_100_percent(text)
        assert result['checks']['has_citation'] == True
        assert 'Devlin et al. 2019' in result.get('found_citations', [])
    
    def test_simple_citation(self):
        """Jednoduchá citace 'Autor 2020' """
        text = "[F] Podle Smith 2023 je to efektivní."
        result = validate_100_percent(text)
        assert result['checks']['has_citation'] == True
    
    def test_no_citation(self):
        """Text bez citace"""
        text = "[D] Model je velmi dobrý."
        result = validate_100_percent(text)
        assert result['checks']['has_citation'] == False

class TestNumberContext:
    """Testy pro čísla s kontextem"""
    
    def test_number_with_percent(self):
        """Číslo s procentem"""
        text = "[D] Model dosahuje 95% přesnosti."
        result = validate_100_percent(text)
        assert result['checks']['numbers_with_context'] == True
    
    def test_number_without_unit(self):
        """Číslo bez jednotky"""
        text = "[D] Model má 175 parametrů."
        result = validate_100_percent(text)
        assert result['checks']['numbers_with_context'] == False
        assert '175' in str(result['violations'])
    
    def test_multiple_numbers_mixed(self):
        """Mix čísel s a bez jednotek"""
        text = "[D] Model má 95% přesnost ale 1000 vrstev."
        result = validate_100_percent(text)
        assert result['checks']['numbers_with_context'] == False

class TestDatasetDetection:
    """Testy pro detekci konkrétních datasetů"""
    
    def test_known_dataset(self):
        """Známý dataset by měl být uznán jako verifikace"""
        text = "[D] Model testován na SQuAD datasetu."
        result = validate_100_percent(text)
        assert result['checks']['has_verification'] == True
        assert 'SQuAD' in result.get('found_datasets', [])
    
    def test_multiple_datasets(self):
        """Více datasetů"""
        text = "[D] Testováno na MNIST, CIFAR-10 a ImageNet."
        result = validate_100_percent(text)
        assert result['checks']['has_verification'] == True
        datasets = result.get('found_datasets', [])
        assert 'MNIST' in datasets
        assert 'CIFAR' in datasets
        assert 'ImageNet' in datasets

class TestCompleteValidation:
    """Testy kompletní validace"""
    
    def test_perfect_response(self):
        """Perfektní odpověď by měla dostat 100%"""
        text = """[D] BERT-base dosahuje 88.5% F1 skóre na SQuAD v2.0
├── DŮKAZ: Devlin et al. 2019, NAACL
├── KONTEXT: 110M parametrů, fine-tuning na TPU v4
├── ČÍSLA: 88.5% F1, 81.2% EM (exact match)
├── LIMITY: Pouze anglický text, ne pro low-resource jazyky
└── OVĚŘENÍ: Reprodukovatelné přes HuggingFace transformers"""
        
        result = validate_100_percent(text)
        assert result['pass'] == True
        assert result['score'] == 100
        assert len(result['violations']) == 0
    
    def test_bad_response(self):
        """Špatná odpověď by měla selhat"""
        text = "Model brzy překonává všechny a umožní AGI."
        result = validate_100_percent(text)
        assert result['pass'] == False
        assert result['score'] < 50
        assert len(result['violations']) > 3
    
    def test_medium_response(self):
        """Středně dobrá odpověď"""
        text = "[D] Model dosahuje 90% přesnosti. Limit: jen pro anglický text."
        result = validate_100_percent(text)
        assert result['pass'] == False  # Chybí citace a verifikace
        assert 40 < result['score'] < 80

class TestFormatClaim:
    """Test formátování tvrzení"""
    
    def test_format_structure(self):
        """Správná struktura výstupu"""
        output = format_claim(
            level="D",
            claim="Test tvrzení",
            evidence="Test důkaz",
            context="Test kontext",
            numbers="99%",
            limits="Test limit",
            verification="Test ověření"
        )
        
        assert "[D]" in output
        assert "├── DŮKAZ:" in output
        assert "├── KONTEXT:" in output
        assert "├── ČÍSLA:" in output
        assert "├── LIMITY:" in output
        assert "└── OVĚŘENÍ:" in output

class TestPipeline:
    """Testy pipeline"""
    
    def test_pipeline_clean_text(self):
        """Pipeline by měl vyčistit blokovaná slova"""
        pipeline = AntiHallucinationPipeline()
        text = "Model brzy dosáhne dramatického zlepšení."
        cleaned = pipeline.clean_during_generation(text)
        assert "brzy" not in cleaned
        assert "dramatického" not in cleaned
    
    def test_pipeline_regeneration(self):
        """Pipeline by měl umět regenerovat text"""
        pipeline = AntiHallucinationPipeline()
        text = "Model je dobrý."
        violations = ["CHYBÍ označení úrovně jistoty", "CHYBÍ citace"]
        regenerated = pipeline.regenerate_with_constraints(text, violations)
        assert "[D]" in regenerated
        assert "2023" in regenerated

# Hlavní spuštění testů
if __name__ == "__main__":
    # Pokud není nainstalován pytest, spustí testy manuálně
    if PYTEST_AVAILABLE:
        pytest.main([__file__, "-v"])
    else:
        print("Spouštím testy manuálně (pytest není nainstalován)...")
        
        # Manuální spuštění
        test_classes = [
            TestBlockedWords(),
            TestCitationDetection(),
            TestNumberContext(),
            TestDatasetDetection(),
            TestCompleteValidation(),
            TestFormatClaim(),
            TestPipeline()
        ]
        
        total_tests = 0
        passed_tests = 0
        
        for test_class in test_classes:
            class_name = test_class.__class__.__name__
            print(f"\n{class_name}:")
            
            methods = [m for m in dir(test_class) if m.startswith("test_")]
            for method_name in methods:
                total_tests += 1
                try:
                    method = getattr(test_class, method_name)
                    method()
                    print(f"  ✓ {method_name}")
                    passed_tests += 1
                except AssertionError as e:
                    print(f"  ✗ {method_name}: {e}")
                except Exception as e:
                    print(f"  ✗ {method_name}: Unexpected error: {e}")
        
        print(f"\n{'='*50}")
        print(f"Výsledky: {passed_tests}/{total_tests} testů prošlo")
        print(f"Úspěšnost: {passed_tests/total_tests*100:.1f}%")