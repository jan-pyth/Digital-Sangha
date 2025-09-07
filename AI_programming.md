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

> Jak z tohohle pohledu psát prompty, které navigují mezi 175miliardami parametrů, pokud jsem "laik" kodér" a potřebuji, aby jsi efektivně psal kód?

● Prompt návod pro "laika kodéra":

  ZÁKLADNÍ ŠABLONA:

  Language: [Python/JS/etc]
  Task: [konkrétní úkol]
  Context: [kde to poběží]
  Requirements: [co musí kód splňovat]
  Current code: [váš existující kód]
  Error/Problem: [co nefunguje]

  KONKRÉTNÍ PŘÍKLADY:

  Místo: "Napiš mi web scraper"

  Použij:
  Language: Python
  Task: Scrape product prices from e-shop.cz/products
  Requirements:
  - Handle connection errors
  - Save to CSV
  - Run daily via cron
  Current setup: Ubuntu VPS, Python 3.10
  Need: Working code I can copy-paste

  KLÍČOVÉ FRÁZE, které aktivují správné váhy:

  Pro robustní kód:
  - "production-ready"
  - "with error handling"
  - "handle edge cases"

  Pro čitelný kód:
  - "with comments explaining why, not what"
  - "following [language] conventions"
  - "readable variable names"

  Pro výkon:
  - "optimized for performance"
  - "mention time complexity"
  - "avoid unnecessary loops"

  CO NIKDY NEPOUŽÍVAT:

  ❌ "Make it good"
  ❌ "Write professional code"
  ❌ "Be careful"
  ❌ "Think about it"

  STRUKTURA, která funguje:

  1. KONTEXT PRVNÍ
  I have a Django app with PostgreSQL.
  Users table has 1M records.

  2. PROBLÉM KONKRÉTNĚ
  This query takes 30 seconds:
  [váš kód]

  3. CO CHCETE
  Need: Optimized query under 1 second
  Can: Add indexes, change query structure
  Cannot: Change table schema

  LAIK TRIK #1: Copy-paste chybové hlášky

  Místo: "Kód nefunguje"

  Použij:
  Getting this error:
  [EXACT ERROR MESSAGE]

  When running:
  [YOUR CODE]

  Environment: Windows 11, Python 3.11

  LAIK TRIK #2: Ukažte, co máte

  Místo: "Potřebuju databázi"

  Použij:
  Current structure:
  - Flask app in app.py
  - No database yet
  - Need to store: users (email, password), posts (title, content)
  - Deploy target: Heroku

  Write: SQLAlchemy models + setup

  LAIK TRIK #3: Řekněte, co NEUMÍTE

  Need: React component for image gallery
  My level: Know HTML/CSS, basic JavaScript
  Don't know: React hooks, state management
  Make it: Simple, with comments explaining React concepts

  ULTIMÁTNÍ LAIK ŠABLONA:

  ## What I'm building:
  [2 věty o projektu]

  ## What I have:
  [list souborů/technologií]

  ## What I need:
  [konkrétní funkce]

  ## Problem:
  [co teď nefunguje/chybí]

  ## My skill level:
  [co umíte/neumíte]

  ## Requirements:
  - Must work with: [vaše prostředí]
  - Should be: simple to understand
  - Include: setup instructions

  PROČ TO FUNGUJE:

  - "What I'm building" → aktivuje váhy z podobných projektů
  - "What I have" → omezuje na kompatibilní řešení
  - "My skill level" → aktivuje váhy z tutoriálů, ne z advanced dokumentace
  - "Include setup instructions" → dostanete kód + jak ho spustit

  BONUS: Jak získat vysvětlení

  After writing the code, explain:
  1. Why you chose this approach
  2. What each part does
  3. Common mistakes to avoid

  Pamatujte: Nejste hloupí, když říkáte AI, co neumíte. Pomáháte jí vybrat správnou "knihu" z její knihovny. AI, která dostane "naprogramuj mi web" je jako
  knihovník, kterému řeknete "chci knihu" - může přinést cokoliv.