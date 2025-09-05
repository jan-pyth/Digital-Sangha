# ✅ Správné DNS nastavení pro Cloudflare

## Co už máš hotové:
✅ **CNAME záznam pro root doménu:**
- Type: CNAME
- Name: digital-sangha.org
- Content: elliptical-fish-4trxto8jwdjob...
- Proxy: Proxied (oranžový mráček)

## Co ještě přidat:

### 1. Přidej WWW subdoénu
Klikni na **"Add record"** a vyplň:

1. **V dropdown "Type" vyber:** CNAME
2. **Do pole "Name" napiš:** www
3. **Do pole "Content" vlož:** elliptical-fish-4trxto8jwdjoboth3e6ylepw.herokudns.com
4. **Proxy status:** Nech zapnutý (oranžový mráček)
5. **TTL:** Auto
6. Klikni **Save**

### 2. Volitelně: API subdoména
Pokud chceš API na subdoméně:

1. **Type:** CNAME
2. **Name:** api
3. **Content:** elliptical-fish-4trxto8jwdjoboth3e6ylepw.herokudns.com
4. **Proxy:** Zapnutý
5. **Save**

## Důležité SSL/TLS nastavení:

### Jdi do SSL/TLS → Overview
**MUSÍ být nastaveno na: Full**

⚠️ **NE "Full (strict)"** - to nebude fungovat s Heroku!
⚠️ **NE "Flexible"** - způsobí redirect loop!
✅ **"Full"** - správné nastavení pro Heroku

### Jdi do SSL/TLS → Edge Certificates
Zapni:
- ✅ Always Use HTTPS
- ✅ Automatic HTTPS Rewrites

## Finální DNS záznamy by měly vypadat takto:

| Type | Name | Content | Proxy | TTL |
|------|------|---------|-------|-----|
| CNAME | digital-sangha.org | elliptical-fish-4trxto8jwdjob... | Proxied | Auto |
| CNAME | www | elliptical-fish-4trxto8jwdjob... | Proxied | Auto |

## Test funkčnosti:

Po uložení počkej 5-10 minut a pak zkus:

```bash
# Test DNS
nslookup digital-sangha.org
nslookup www.digital-sangha.org

# Test HTTPS
curl -I https://digital-sangha.org
curl -I https://www.digital-sangha.org
```

## Tvoje URLs budou:
- https://digital-sangha.org ✅
- https://www.digital-sangha.org ✅
- https://digital-sangha.org/api/validate ✅
- https://digital-sangha.org/health ✅

---

💡 **TIP:** Pokud v dropdown menu není CNAME, zkus scrollovat dolů nebo začít psát "CNAME" - mělo by se objevit.