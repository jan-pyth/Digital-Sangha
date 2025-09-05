# 🌐 Cloudflare DNS Configuration for digital-sangha.org

## Your Heroku DNS Target
```
elliptical-fish-4trxto8jwdjoboth3e6ylepw.herokudns.com
```

## Step-by-Step DNS Setup in Cloudflare

### 1. Login to Cloudflare Dashboard
Go to: https://dash.cloudflare.com

### 2. Select Your Domain
Click on **digital-sangha.org**

### 3. Navigate to DNS Settings
Click on **DNS** in the left sidebar

### 4. Add DNS Records

### Record 1: Root Domain (@)
Click **Add record** and enter:
- **Type:** CNAME
- **Name:** @ (or digital-sangha.org)
- **Target:** `elliptical-fish-4trxto8jwdjoboth3e6ylepw.herokudns.com`
- **Proxy status:** ✅ Proxied (orange cloud ON)
- **TTL:** Auto

### Record 2: WWW Subdomain
Click **Add record** and enter:
- **Type:** CNAME
- **Name:** www
- **Target:** `elliptical-fish-4trxto8jwdjoboth3e6ylepw.herokudns.com`
- **Proxy status:** ✅ Proxied (orange cloud ON)
- **TTL:** Auto

### Record 3: API Subdomain (Optional)
Click **Add record** and enter:
- **Type:** CNAME
- **Name:** api
- **Target:** `elliptical-fish-4trxto8jwdjoboth3e6ylepw.herokudns.com`
- **Proxy status:** ✅ Proxied (orange cloud ON)
- **TTL:** Auto

## 5. SSL/TLS Configuration (CRITICAL!)

### Navigate to SSL/TLS → Overview
Set encryption mode to: **Full**

⚠️ **IMPORTANT:** Must be "Full", NOT "Full (strict)"!
- Full = Works with Heroku's SSL certificate
- Full (strict) = Will cause errors with Heroku

### Navigate to SSL/TLS → Edge Certificates
Enable these settings:
- ✅ **Always Use HTTPS** - ON
- ✅ **Automatic HTTPS Rewrites** - ON
- ✅ **Opportunistic Encryption** - ON
- ✅ **TLS 1.3** - ON

## 6. Speed Optimization

### Navigate to Speed → Optimization
Enable:
- ✅ **Auto Minify** - JavaScript, CSS, HTML
- ✅ **Brotli** - ON
- ✅ **Early Hints** - ON
- ✅ **Rocket Loader** - ON (test first, disable if issues)

## 7. Caching Configuration

### Navigate to Caching → Configuration
- **Caching Level:** Standard
- **Browser Cache TTL:** 4 hours
- **Always Online:** ON

## 8. Page Rules (Optional but Recommended)

### Navigate to Rules → Page Rules

#### Rule 1: Force HTTPS
- **URL:** `http://*digital-sangha.org/*`
- **Setting:** Always Use HTTPS

#### Rule 2: Cache Static Files
- **URL:** `*digital-sangha.org/static/*`
- **Settings:**
  - Cache Level: Cache Everything
  - Edge Cache TTL: 1 month

#### Rule 3: Bypass Cache for API
- **URL:** `*digital-sangha.org/api/*`
- **Setting:** Cache Level: Bypass

## 9. Verify Your Configuration

### Check DNS Records
In Cloudflare DNS section, you should see:
```
Type    Name    Content                                               Proxy
CNAME   @       elliptical-fish-4trxto8jwdjoboth3e6ylepw.herokudns.com   ✅
CNAME   www     elliptical-fish-4trxto8jwdjoboth3e6ylepw.herokudns.com   ✅
```

### Test DNS Propagation
```bash
# Check DNS resolution
nslookup digital-sangha.org
dig digital-sangha.org

# Should return Cloudflare IPs (104.x.x.x or 172.x.x.x)
```

## 10. Wait for Propagation

DNS changes can take:
- **Immediate:** If using Cloudflare DNS
- **5-30 minutes:** For most users
- **Up to 48 hours:** Full global propagation (rare)

## 11. Test Your Site

Once DNS propagates, test:

### Main URLs
- https://digital-sangha.org
- https://www.digital-sangha.org
- https://digital-sangha.org/health
- https://digital-sangha.org/api/examples

### Check SSL Certificate
Click the padlock in your browser - should show Cloudflare SSL certificate

## Troubleshooting

### Site Not Loading?
1. **Check Heroku:** Is your app running?
   ```bash
   heroku ps
   heroku logs --tail
   ```

2. **Check DNS:** Has it propagated?
   ```bash
   nslookup digital-sangha.org
   ```

3. **Check SSL:** Is it set to "Full" (not "Full strict")?

### Getting "Too Many Redirects"?
- SSL/TLS must be set to "Full" (not Flexible or Full strict)
- "Always Use HTTPS" should be ON

### API Not Working?
- Check CORS settings in app.py
- Ensure /api/* Page Rule bypasses cache
- Test directly: `curl https://digital-sangha.org/api/health`

### SSL Certificate Error?
- Wait 5-10 minutes for Cloudflare to provision certificate
- Ensure Proxy is ON (orange cloud) for your DNS records
- SSL/TLS mode must be "Full"

## Success Indicators

✅ Site loads at https://digital-sangha.org
✅ No SSL warnings in browser
✅ API endpoint works: /api/validate
✅ File upload functionality works
✅ All three validation modes work

## Quick Test Commands

```bash
# Test main site
curl -I https://digital-sangha.org

# Test API health
curl https://digital-sangha.org/health

# Test validation API
curl -X POST https://digital-sangha.org/api/validate \
  -H "Content-Type: application/json" \
  -d '{"text":"◆ Test","mode":"relaxed"}'
```

---

## 🎉 Your AOP Validator is Live!

Once configured, your validator will be available at:
- **Main:** https://digital-sangha.org
- **API Documentation:** https://digital-sangha.org/api/examples
- **Health Check:** https://digital-sangha.org/health

Share it with the world! The Digital Sangha validator is ready to bring empirical rigor to AI dialogs. 🚀