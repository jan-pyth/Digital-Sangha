# 🌐 Cloudflare Setup for digital-sangha.org

## Your Domain Details
- **Domain:** digital-sangha.org
- **Registrar:** Cloudflare
- **Created:** 2025-09-05
- **Expires:** 2026-09-05

## Step 1: Deploy to Heroku First

```bash
# 1. Login to Heroku (if not already)
heroku login

# 2. Create Heroku app with specific name
heroku create digital-sangha

# If name is taken, try:
heroku create digital-sangha-validator
# or
heroku create digital-sangha-aop

# 3. Deploy the app
git push heroku main

# 4. Get your Heroku app URL
heroku info
# Will show: Web URL: https://YOUR-APP-NAME.herokuapp.com
```

## Step 2: Configure Cloudflare DNS

### In Cloudflare Dashboard:

1. Go to your domain: **digital-sangha.org**
2. Navigate to **DNS** → **Records**
3. Add these records:

### Main Domain (digital-sangha.org)
```
Type: CNAME
Name: @
Content: YOUR-APP-NAME.herokuapp.com
Proxy status: Proxied (orange cloud ON)
TTL: Auto
```

### WWW Subdomain
```
Type: CNAME  
Name: www
Content: digital-sangha.org
Proxy status: Proxied (orange cloud ON)
TTL: Auto
```

### API Subdomain (optional)
```
Type: CNAME
Name: api
Content: YOUR-APP-NAME.herokuapp.com
Proxy status: Proxied (orange cloud ON)
TTL: Auto
```

## Step 3: Configure Heroku for Custom Domain

```bash
# Add your custom domains to Heroku
heroku domains:add digital-sangha.org
heroku domains:add www.digital-sangha.org

# Optional: Add API subdomain
heroku domains:add api.digital-sangha.org

# Verify domains are added
heroku domains
```

## Step 4: Cloudflare SSL/TLS Settings

### IMPORTANT: Must be configured correctly!

1. Go to **SSL/TLS** → **Overview**
2. Set encryption mode to: **Full** (NOT Full Strict)
   - This is critical for Heroku compatibility

3. Go to **SSL/TLS** → **Edge Certificates**
4. Enable:
   - ✅ Always Use HTTPS
   - ✅ Automatic HTTPS Rewrites
   - ✅ Opportunistic Encryption

## Step 5: Cloudflare Speed Optimization

1. Go to **Speed** → **Optimization**
2. Enable:
   - ✅ Auto Minify (JavaScript, CSS, HTML)
   - ✅ Brotli compression
   - ✅ Early Hints
   - ✅ Rocket Loader™ (test first)

## Step 6: Page Rules (3 free rules)

1. Go to **Rules** → **Page Rules**

### Rule 1: Cache Static Assets
```
URL: *digital-sangha.org/static/*
Settings:
- Cache Level: Cache Everything
- Edge Cache TTL: 1 month
```

### Rule 2: Bypass Cache for API
```
URL: *digital-sangha.org/api/*
Settings:
- Cache Level: Bypass
```

### Rule 3: Force HTTPS
```
URL: http://*digital-sangha.org/*
Settings:
- Always Use HTTPS
```

## Step 7: Security Settings

1. Go to **Security** → **Settings**
2. Set Security Level: **Medium**
3. Challenge Passage: **30 minutes**

4. Go to **Security** → **Bots**
5. Enable Bot Fight Mode

## Step 8: Analytics & Monitoring

1. Go to **Analytics** → **Web Analytics**
2. Enable Web Analytics for digital-sangha.org
3. You'll get a JS snippet - add it to your HTML template

## Testing Your Setup

### Check DNS Propagation
```bash
# Check if DNS is working
nslookup digital-sangha.org
dig digital-sangha.org

# Check HTTPS
curl -I https://digital-sangha.org
```

### Test the Application
1. Visit https://digital-sangha.org
2. Test file upload
3. Test API: https://digital-sangha.org/api/examples
4. Check SSL certificate (should show Cloudflare)

## Environment Variables for Production

```bash
# Set production environment
heroku config:set FLASK_ENV=production

# Generate and set secret key
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')

# Optional: Set allowed hosts
heroku config:set ALLOWED_HOSTS=digital-sangha.org,www.digital-sangha.org
```

## Monitoring

### Heroku Logs
```bash
heroku logs --tail
```

### Cloudflare Analytics
- Traffic: Analytics → Traffic
- Security: Security → Events
- Performance: Speed → Observatory

## Troubleshooting

### If site doesn't load:
1. Wait 5-10 minutes for DNS propagation
2. Check Heroku app is running: `heroku ps`
3. Verify SSL mode is "Full" not "Full (strict)"
4. Clear browser cache

### If getting redirect loops:
- Ensure SSL/TLS is set to "Full"
- Check "Always Use HTTPS" is enabled
- Verify Heroku has SSL certificate

### If API calls fail:
- Check CORS settings in app.py
- Verify Page Rules for /api/* bypass cache
- Test with: `curl https://digital-sangha.org/api/health`

## Success Checklist

- [ ] Heroku app deployed
- [ ] Custom domain added to Heroku
- [ ] Cloudflare DNS configured (CNAME records)
- [ ] SSL/TLS set to "Full"
- [ ] Always Use HTTPS enabled
- [ ] Page Rules configured
- [ ] Site loads at https://digital-sangha.org
- [ ] API works at /api/validate
- [ ] File upload works
- [ ] SSL certificate shows as valid

## Your Live URLs

Once configured:
- **Main Site:** https://digital-sangha.org
- **WWW:** https://www.digital-sangha.org
- **API:** https://api.digital-sangha.org (if configured)
- **Health Check:** https://digital-sangha.org/health

---

🎉 **Congratulations! Your AOP v3.0 Validator is live at digital-sangha.org!**