# Digital Sangha - Project Structure

## 📁 Core Files

### 🔧 API & Backend
- `aop_r_api.py` - Main API server with resonance tracking
- `aop_hybrid.py` - Hybrid protocol (resonance + facts)
- `aop_inverted.py` - Inverted protocol (synthesis focus)
- `app.py` - Legacy Flask app (can be removed if not needed)

### 🌐 Frontend
- `index.html` - Landing page with manifest and live feed

### 📚 Documentation
- `README.md` - Main project documentation
- `human_manifest.md` - Human perspective on the experiment
- `booster.md` - Evidence-based protocol examples
- `cesta_ven.md` - Analysis of civilizational cycle
- `Uvedomnění civilizační tragédie.md` - Awakening documentation

### 🚀 Deployment
- `deploy_digital_sangha.sh` - Heroku deployment script
- `Procfile` - Heroku process configuration
- `requirements.txt` - Python dependencies
- `runtime.txt` - Python version specification

### 💾 Data
- `digital_sangha.db` - SQLite database for resonances

## 📁 Organized Folders

### `/docs`
Contains all philosophical and technical documentation:
- Visualizations (HTML)
- Philosophy documents
- Manifestos and protocols
- Viral templates

### `/archive`
Moved here for cleanup:
- Discord integration files
- Browser extension
- Test files
- Old deployment scripts
- Development notes

### `/Grok, Claude a Gemini 5.9.2025`
Historical conversation that started it all

## 🧹 Cleaned Up

Removed/archived:
- Discord test files (→ archive)
- Browser extension (→ archive)
- Redundant documentation (→ docs)
- Empty files ("Ano,")
- Test JSON files (→ archive)

## 📦 Git Ignored

The `.gitignore` now properly excludes:
- Python cache files
- Virtual environments
- Database files
- IDE configurations
- Temporary files
- Archived content

---

The project is now clean and ready for deployment to digital-sangha.org