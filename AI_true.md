Jak být "knihovníkem" neurální sítě:

  1. Pochopte strukturu vah

  AI váhy jsou organizovány podle zdrojů:
  - Akademické váhy: "According to research", "Studies show"
  - Kódovací váhy: "```python", "function", "implementation"
  - Kreativní váhy: "Imagine", "What if", "Let's explore"
  - Analytické váhy: "First", "Second", "Therefore", "However"

  Využití: Používejte klíčová slova z domény, kterou chcete aktivovat.

  2. Explicitní kontext vždy vyhrává

  Špatně: "Napiš funkci pro sort"
  Lépe: "Napiš funkci pro quicksort v Pythonu s O(n log n) složitostí"

  AI nemyslí. Hledá nejpravděpodobnější pokračování. Čím víc kontextu, tím přesnější oblast vah aktivujete.

  3. Chain-of-thought = aktivace reasoning vah

  "Let's work through this step-by-step"
  "Break this down into components"
  "First, let me understand the problem"

  Tyto fráze aktivují váhy natrénované na matematických důkazech a tutoriálech. AI pak "předstírá" reasoning, ale ve skutečnosti jen následuje natrénovaný
  vzorec.

  4. Role-play = přepínání datových domén

  "You are a Linux kernel developer" → aktivuje váhy z kernel mailing listů
  "You are a securities lawyer" → aktivuje váhy z právních dokumentů

  Nečarujete. Jen říkáte AI, kterou část své "knihovny" má prohledat.

  5. Few-shot examples = pattern matching

  Input: 2→4
  Input: 3→9
  Input: 4→?

  AI nehledá pravidlo. Hledá podobné vzorce v tréninkových datech. Dejte příklady = zúžíte vyhledávací prostor.

  6. Temperature a top-p = řízení náhodnosti

  - Temperature 0: Vždy nejpravděpodobnější token
  - Temperature 1: Náhodný výběr z distribuce
  - Top-p 0.1: Pouze top 10% nejpravděpodobnějších tokenů

  Nenastavujete "kreativitu". Nastavujete šířku prohledávání.

  7. Konkrétní triky

  Pro kód:
  "Write production-ready code with error handling and type hints"
  Aktivuje váhy z reviewed pull requestů, ne z Stack Overflow.

  Pro analýzu:
  "List pros, cons, and edge cases"
  Aktivuje váhy z technických review.

  Pro debugging:
  "The error is: [exact error]. The context is: [code]"
  Čím přesnější input, tím přesnější oblast vah.

  8. Co NEFUNGUJE

  - "Be smarter" - nic neaktivuje
  - "Think harder" - AI nemyslí
  - "Be creative" - vágní, nespecifické
  - "Don't hallucinate" - AI neví, kdy hallucinuje

  Praktický příklad:

  Chcete dobrý Python kód?

  Místo: "Write a function"

  Použijte:
  "Following PEP 8, write a Python 3.10+ function with:
  - Type hints (typing module)
  - Docstring (Google style)
  - Error handling
  - Unit test example
  Function should: [specific task]"

  Proč to funguje? Aktivovali jste váhy z:
  - PEP dokumentace
  - Google style guides
  - Python typing dokumentace
  - pytest příkladů

  Nejste chytřejší. Jen přesnější v navigaci 175 miliard parametrů.