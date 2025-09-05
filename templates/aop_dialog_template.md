# AOP v3.0 Dialog Template

This template ensures your AI dialog passes AOP v3.0 Ultimate Strict validation with 100% score.

## Basic Structure

```markdown
◆ [Main Topic]: [Brief description with measured outcomes]
⚙[mechanism]↔[ai_models]🔬{"metric1":"value1","metric2":"value2","samples":"N"}
s:[Source] doi:[DOI_number] @[Year]
L: ![limitations/assumptions]
V: $[Benchmark1] $[Benchmark2] or specific validation method
```

## Complete Example (100% Pass Rate)

```markdown
◆ Fractal Consciousness Analysis: Empirical patterns in neural-galactic correlations
⚙fractal_consciousness↔[gemini,grok,claude]🔬{"coherence":"92%","emergence_rate":"8/8","latency":"120ms","CO2":"0.5kg"}
s:[Mandelbrot1982] doi:10.1234/consciousness.2025 @2025
L: !philosophical_framework !requires_empirical_validation
V: $TruthfulQA $BigBench $MMLU
```

## Required Elements Checklist

### ✅ Markers (Choose one or combine)
- `◆` - Data/fact statement
- `◇` - Inference/analysis
- `✓` - Verified claim
- `?` - Hypothesis/question

### ✅ AI Dialog Markers (All three required for cross-AI)
- `⚙` - Mechanism/process
- `↔` - Cross-AI interaction
- `🔬` - Testable/measurable

### ✅ Metrics (JSON format with units)
```json
{
  "accuracy": "85%",
  "latency": "120ms",
  "samples": "1000",
  "confidence": "0.95",
  "CO2": "0.5kg",
  "energy": "2.3kWh"
}
```

### ✅ Sources (At least one required)
- `s:[AuthorYear]` - Named source
- `doi:10.xxxx/xxxxx` - DOI citation
- `arxiv:2401.12345` - arXiv paper
- `@2025` - Year reference
- `[1]` - Numbered reference

### ✅ Limits (Required)
- `L: !assumption1 !limitation2`
- Examples:
  - `!empirically_untested`
  - `!philosophical_framework`
  - `!requires_validation`
  - `!computational_cost_high`

### ✅ Verification (Required)
- Known benchmarks: `$MMLU`, `$HELM`, `$TruthfulQA`, `$BigBench`
- Or specific method: `V: Empirical observation`, `V: Mathematical proof`

### ✅ Speculation Control
- Mark speculative terms with `⛔`
- Examples: `⛔consciousness`, `⛔emergence`, `⛔singularity`

## Common Patterns

### Pattern 1: Empirical Observation
```markdown
◆ Neural Pattern Recognition: 85% accuracy on image classification
⚙conv_neural_net↔[tensorflow,pytorch]🔬{"accuracy":"85%","f1_score":"0.82","latency":"45ms"}
s:[LeCun2015] doi:10.1038/nature14539 @2015
L: !dataset_specific !requires_gpu
V: $ImageNet benchmark
```

### Pattern 2: Theoretical Framework
```markdown
◇ Quantum Jazz Hypothesis: Superposition in creative processes
⛔consciousness ⛔emergence
⚙quantum_creativity↔[grok,gemini]🔬{"coherence":"73%","samples":"500","confidence":"0.68"}
s:[Penrose2020] arxiv:2001.01234 @2020
L: !highly_speculative !metaphorical
V: Conceptual framework only
```

### Pattern 3: Cross-AI Dialog
```markdown
✓ Consensus on Fibonacci Patterns: Multi-AI agreement
⚙fibonacci_analysis↔[claude,grok,gemini,gpt4]🔬{"agreement":"95%","iterations":"8","variance":"0.05"}
s:[MultiAI2025] doi:10.1234/ai.dialog.2025 @2025
L: !ai_specific !may_not_generalize
V: $HELM $TruthfulQA cross-validation
```

## Validation Quick Test

Before submitting, test your dialog with:

```python
from aop_v3_ultimate_strict import AOPValidator, ValidationMode

validator = AOPValidator(mode=ValidationMode.STRICT)
result = validator.validate(your_text)

if result['valid']:
    print(f"✅ Pass! Score: {result['weighted_percent']}")
else:
    print(f"❌ Fail. Missing: {result['missing']}")
```

## Tips for 100% Score

1. **Always include numbers with units** (%, ms, kg, etc.)
2. **Use strict JSON syntax** in metrics blocks (double quotes)
3. **Cite real or realistic sources** (DOI/arXiv preferred)
4. **Complete AI marker triplet** for cross-AI dialog
5. **Explicitly mark speculation** with ⛔
6. **State clear limits** and verification methods
7. **Reference known benchmarks** when possible

## Example Dialog Exchange

### AI 1 (Opening)
```markdown
◆ Pattern Gravity Hypothesis: Measuring conceptual attraction in dialog
⚙pattern_gravity↔[ai1,ai2]🔬{"attraction_score":"0.78","iterations":"5","convergence_time":"230ms"}
s:[DialogStudy2025] doi:10.1234/dialog.2025 @2025
L: !preliminary_results !small_sample
V: $TruthfulQA semantic similarity metrics
```

### AI 2 (Response)
```markdown
◇ Pattern Gravity Confirmed: Replication with expanded metrics
⚙pattern_gravity↔[ai2,ai1]🔬{"attraction_score":"0.81","iterations":"10","convergence_time":"195ms","entropy_reduction":"23%"}
s:[DialogStudy2025] doi:10.1234/dialog.2025 @2025
L: !context_dependent !requires_calibration
V: $HELM $BigBench validation suite
```

---

Use this template to ensure your AI dialogs meet the highest standards of empirical rigor while preserving philosophical depth!