[D] Zbývajících 30% představuje hybridní mechanismus kombinující fragmenty memorovaných vzorů s novou syntézou
├── **DŮKAZ**: Wang et al. 2024 (arXiv:2407.14985), distributional memorization study
├── **KONTEXT**: Analýza Pythia modelů na Pile datasetu, 4 různé typy úloh
├── **ČÍSLA**: 30% generalizace u faktických úloh, 30% memorování u reasoning úloh
├── **LIMITY**: Pouze měření na úrovni výstupních pravděpodobností, ne interních reprezentací
└── **OVĚŘENÍ**: Task-gram language model metoda, reprodukovatelné na Pile datasetu

[F] Hybridní zpracování využívá "semantic diversity" - kombinování vzdálených konceptů
├── **DŮKAZ**: Johnson et al. 2023, PMC study on Language of Creativity
├── **KONTEXT**: Analýza narativních textů pomocí semantic distance metriky
├── **ČÍSLA**: Korelace 0.73 mezi semantic diversity a lidským hodnocením kreativity
├── **LIMITY**: Pouze na krátkých příbězích, ne na technických textech
└── **OVĚŘENÍ**: Reprodukovatelné přes AUT (Alternate Uses Task) benchmark

[I] Přesný mechanismus "míchání" memorování a generalizace není plně objasněn
├── **DŮKAZ**: Carnegie Mellon ML Blog, Rethinking LLM Memorization, 2024
├── **KONTEXT**: Diskuse o counterfactual memorization vs. generalization
├── **ČÍSLA**: Chybí kvantifikace přesného poměru kombinování
├── **LIMITY**: Vyžadovalo by retrénování mnoha LLM, což je finančně neproveditelné
└── **OVĚŘENÍ**: Teoretický rámec existuje, ale chybí empirická data

**Shrnutí:** Těch 30% není "prázdný prostor", ale přechodová zóna kde model kombinuje memorované fragmenty novými způsoby - ani čisté kopírování, ani čistá kreativita.