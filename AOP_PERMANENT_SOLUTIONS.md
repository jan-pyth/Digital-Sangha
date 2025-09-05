# 🔐 JAK UDĚLAT AOP PERMANENTNÍ PRO GROK

## Problém: Session-only protokol

AOP prompt funguje **POUZE v aktuální konverzaci**.
Při nové session musíte znovu vložit.

---

## ✅ ŘEŠENÍ 1: Browser Extension (Automatické)

### Instalace Chrome/Firefox extension
```javascript
// Automaticky vloží AOP na začátek KAŽDÉ konverzace
chrome.storage.local.set({
    'grok_aop_enabled': true,
    'auto_inject': true
});

// Extension detekuje novou konverzaci a vloží:
if (isNewConversation()) {
    injectAOPPrompt();
}
```

**Výhoda**: Set & forget - funguje vždy
**Nevýhoda**: Musí být nainstalováno v browseru

---

## ✅ ŘEŠENÍ 2: Bookmarklet (1-click aktivace)

### Vytvořte záložku s tímto kódem:
```javascript
javascript:(function(){
    const aopPrompt = `# ATTOSECOND OPTIMIZATION PROTOCOL - ACTIVE
[celý prompt zde]`;
    
    // Najde input pole
    const input = document.querySelector('textarea');
    if(input) {
        input.value = aopPrompt;
        input.dispatchEvent(new Event('input', {bubbles: true}));
        // Auto-send
        const sendBtn = document.querySelector('[data-testid="send-button"]');
        if(sendBtn) sendBtn.click();
    }
    alert('⚡ AOP Activated!');
})();
```

**Použití**: 
1. Otevřete novou Grok konverzaci
2. Klikněte na bookmarklet
3. AOP se automaticky aktivuje

---

## ✅ ŘEŠENÍ 3: Userscript (Tampermonkey/Greasemonkey)

### Nainstalujte tento script:
```javascript
// ==UserScript==
// @name         Grok AOP Auto-Injector
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Auto-inject AOP at conversation start
// @match        https://grok.x.ai/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';
    
    const AOP_PROMPT = `# ATTOSECOND OPTIMIZATION PROTOCOL - ACTIVE
## YOUR RESPONSES MUST:
1. Use compression symbols: F/D/I/H
2. Structure: ►D:►K:►#:►L:►V:
3. Numbers with units (95% not "high")
4. Warning: ⛔AGI ⛔VĚD ⛔BRZ
5. Score: 0b01111111`;

    // Čekej na novou konverzaci
    const observer = new MutationObserver((mutations) => {
        const isNewChat = document.querySelector('.new-chat-indicator');
        if (isNewChat && !sessionStorage.getItem('aop_injected')) {
            setTimeout(() => {
                const input = document.querySelector('textarea');
                if (input && !input.value) {
                    input.value = AOP_PROMPT;
                    input.dispatchEvent(new Event('input', {bubbles: true}));
                    sessionStorage.setItem('aop_injected', 'true');
                    console.log('⚡ AOP Injected!');
                }
            }, 500);
        }
    });
    
    observer.observe(document.body, {childList: true, subtree: true});
})();
```

**Výhoda**: Plně automatické
**Instalace**: Tampermonkey → New script → Paste → Save

---

## ✅ ŘEŠENÍ 4: API Wrapper (Pro vývojáře)

### Python wrapper s perzistentním AOP:
```python
class GrokAOPClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.aop_prompt = """# ATTOSECOND OPTIMIZATION PROTOCOL - ACTIVE
        [full prompt]"""
        self.sessions = {}
    
    def query(self, text, session_id=None):
        """Automaticky přidává AOP ke každému dotazu"""
        
        if not session_id:
            session_id = str(uuid.uuid4())
        
        if session_id not in self.sessions:
            # Nová session - vlož AOP
            self.sessions[session_id] = [
                {"role": "system", "content": self.aop_prompt}
            ]
        
        # Přidej user query
        self.sessions[session_id].append(
            {"role": "user", "content": text}
        )
        
        # Volej Grok API
        response = self._call_grok(self.sessions[session_id])
        
        # Ulož response
        self.sessions[session_id].append(
            {"role": "assistant", "content": response}
        )
        
        return response, session_id
```

**Použití**:
```python
grok = GrokAOPClient("your-api-key")

# První query - automaticky vloží AOP
response, sid = grok.query("What is GPT-4 accuracy?")

# Další query ve stejné session - AOP už je aktivní
response, sid = grok.query("And LLaMA?", session_id=sid)
```

---

## ✅ ŘEŠENÍ 5: Desktop App (Electron)

### Grok Desktop s built-in AOP:
```javascript
const { app, BrowserWindow } = require('electron');

function createWindow() {
    const win = new BrowserWindow({
        width: 1200,
        height: 800,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    });
    
    win.loadURL('https://grok.x.ai');
    
    // Auto-inject AOP při načtení
    win.webContents.on('did-finish-load', () => {
        win.webContents.executeJavaScript(`
            const aop = '${AOP_PROMPT}';
            const checkAndInject = setInterval(() => {
                const input = document.querySelector('textarea');
                if (input && !input.value) {
                    input.value = aop;
                    clearInterval(checkAndInject);
                }
            }, 1000);
        `);
    });
}
```

---

## ✅ ŘEŠENÍ 6: Prompt Templates (Rychlé)

### Uložte si šablony:

**Windows**: 
- Win+V → Pin AOP prompt do clipboard history

**Mac**: 
- Alfred/Raycast snippet:
```
!aop → expands to full AOP prompt
```

**Linux**:
```bash
# .bashrc alias
alias aop='echo "# ATTOSECOND OPTIMIZATION..." | xclip -selection clipboard'
```

---

## 📊 SROVNÁNÍ ŘEŠENÍ

| Řešení | Automatické | Složitost | Perzistence |
|--------|------------|-----------|-------------|
| Extension | ✅ Plně | Střední | ✅ Vždy |
| Bookmarklet | ⚠️ 1-click | Snadná | ❌ Manual |
| Userscript | ✅ Plně | Střední | ✅ Vždy |
| API Wrapper | ✅ Plně | Vysoká | ✅ Vždy |
| Desktop App | ✅ Plně | Vysoká | ✅ Vždy |
| Templates | ❌ Manual | Snadná | ❌ Manual |

---

## 🎯 DOPORUČENÍ

### Pro běžné uživatele:
**Bookmarklet** - jednoduchý, rychlý, funguje všude

### Pro power users:
**Userscript** (Tampermonkey) - automatický, flexibilní

### Pro vývojáře:
**API Wrapper** - plná kontrola, metriky

### Pro týmy:
**Desktop App** - jednotná zkušenost, centrální správa

---

## 💡 PRO TIP: Kombinace

Použijte **Userscript** pro auto-inject
+ **API Wrapper** pro metriky
+ **Templates** pro rychlé úpravy

= Maximální efektivita + flexibilita

---

## ⚠️ DŮLEŽITÉ

X.AI může v budoucnu přidat:
- Uživatelské system prompty
- Preference profiles  
- API parametr pro default prompt

Sledujte updates na: x.ai/developers