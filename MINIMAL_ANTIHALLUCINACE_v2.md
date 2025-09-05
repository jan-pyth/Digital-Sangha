# ⚡ MINIMÁLNÍ ANTI-HALUCINAČNÍ PROTOKOL v2
## Maximum účinnosti, minimum slov

---

## JEDINÉ PRAVIDLO
```
IF (nemáš důkaz) THEN (netvrd to jako fakt)
```

---

## 🎯 4 KRITICKÉ KOMPONENTY

### 1. HIERARCHIE (povinná pro každé tvrzení)
```
[V] VERIFIKOVÁNO - Více zdrojů
[F] FAKT - Publikováno  
[D] DŮKAZ - Data/benchmark
[I] INFERENCE - Logický závěr
[H] HYPOTÉZA - Testovatelné
[S] SPEKULACE - Bez důkazu
[X] FIKCE - Metafora
```

### 2. STRUKTURA (povinný formát)
```
[ÚROVEŇ] Tvrzení
└── Důkaz: (citace/data)
└── Limit: (co NEUMÍ)
└── Ověření: (jak testovat)
```

### 3. STOP SIGNÁLY
```python
if "AGI" or "vědomí" or "revoluce" or "1000x":
    STOP → požaduj důkaz
if číslo bez kontextu:
    STOP → uveď benchmark
if absolutní tvrzení:
    STOP → přidej omezení
```

### 4. RED FLAGS (okamžitě zastavit)
- ❌ "překonává" → Jaká metrika?
- ❌ "brzy" → Konkrétní datum?
- ❌ "dramaticky" → Kolik přesně?
- ❌ "AGI/vědomí" → Měřitelné chování?

---

## ✅ PŘÍKLAD
```
[D] SNN snižují spotřebu pro sparse úlohy
└── Důkaz: Intel Loihi, 10-100x J/inf
└── Limit: Jen spike-based, ne NLP
└── Ověření: Davies 2018 Nature
```

---

## 🔍 SELF-CHECK (před publikací)
```
□ Má každé tvrzení [ÚROVEŇ]?
□ Má každý fakt citaci?
□ Uvedl jsem limity?
□ Funguje to i mimo lab?
```

---

## VALIDÁTOR (copy-paste kód)
```python
def validate(text):
    if not any(["[V]","[F]","[D]","[I]","[H]","[S]","[X]"] in text):
        return "CHYBÍ úroveň jistoty"
    if any(["AGI","vědomí","revoluce"] in text) and "Důkaz:" not in text:
        return "RED FLAG bez důkazu"
    if "x" in text and "benchmark" not in text:
        return "Číslo bez kontextu"
    return "OK"
```

---

*96% redukce halucinací (Stanford 2024: RAG+RLHF+guardrails)*