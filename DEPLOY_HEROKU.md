# 🚀 Deploy to Heroku & Cloudflare

## Prerequisites
- Heroku account (already have ✅)
- Heroku CLI installed
- Domain registered with Cloudflare (need to do)

## Step 1: Heroku Deployment

### 1.1 Login to Heroku
```bash
heroku login
```

### 1.2 Create Heroku App
```bash
# Create app with unique name
heroku create digital-sangha-validator

# Or use your preferred name
heroku create YOUR-APP-NAME
```

### 1.3 Deploy to Heroku
```bash
# Initialize git if not already done
git init

# Add Heroku remote
heroku git:remote -a YOUR-APP-NAME

# Add all files
git add .
git commit -m "Initial deployment of AOP validator web interface"

# Push to Heroku
git push heroku main
```

### 1.4 Open Your App
```bash
heroku open
```

Your app will be available at: `https://YOUR-APP-NAME.herokuapp.com`

## Step 2: Cloudflare Configuration

### 2.1 Add Your Domain to Cloudflare

1. Sign up at [Cloudflare](https://dash.cloudflare.com/sign-up)
2. Add your domain (e.g., `digital-sangha.com`)
3. Update nameservers at your domain registrar to Cloudflare's nameservers

### 2.2 Configure DNS

In Cloudflare dashboard:

1. Go to **DNS** → **Records**
2. Add CNAME record:
   - **Type:** CNAME
   - **Name:** @ (or subdomain like `validator`)
   - **Target:** YOUR-APP-NAME.herokuapp.com
   - **Proxy status:** Proxied (orange cloud ON)

3. Add www redirect (optional):
   - **Type:** CNAME
   - **Name:** www
   - **Target:** YOUR-DOMAIN.com
   - **Proxy status:** Proxied

### 2.3 SSL/TLS Configuration

1. Go to **SSL/TLS** → **Overview**
2. Set encryption mode to **Full** (not Full Strict)
3. Enable **Always Use HTTPS** in SSL/TLS → Edge Certificates

### 2.4 Speed Optimization

1. Go to **Speed** → **Optimization**
2. Enable:
   - Auto Minify (JavaScript, CSS, HTML)
   - Brotli compression
   - Rocket Loader™ (optional)

### 2.5 Configure Heroku for Custom Domain

```bash
# Add custom domain to Heroku
heroku domains:add YOUR-DOMAIN.com
heroku domains:add www.YOUR-DOMAIN.com

# Verify domains
heroku domains
```

## Step 3: Environment Variables (Optional)

Set secret key for production:

```bash
heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(32))')
heroku config:set FLASK_ENV=production
```

## Step 4: Monitor Your App

### Check logs
```bash
heroku logs --tail
```

### Check app status
```bash
heroku ps
```

### Scale if needed (free tier = 1 dyno)
```bash
heroku ps:scale web=1
```

## Step 5: Local Testing Before Deploy

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python app.py

# Or with gunicorn (like Heroku)
gunicorn app:app --workers 2 --threads 2
```

Open http://localhost:5000

## Cloudflare Page Rules (Optional)

Add page rules for better performance:

1. **Cache Everything** for static assets:
   - URL: `*YOUR-DOMAIN.com/static/*`
   - Setting: Cache Level → Cache Everything
   - Edge Cache TTL → 1 month

2. **Bypass Cache** for API:
   - URL: `*YOUR-DOMAIN.com/api/*`
   - Setting: Cache Level → Bypass

## Free Tier Limits

### Heroku Free Tier
- 550 dyno hours/month
- Sleeps after 30 min inactivity
- Custom domain supported
- SSL included

### Cloudflare Free Tier
- Unlimited bandwidth
- DDoS protection
- SSL certificate
- Basic analytics
- 3 page rules

## Troubleshooting

### If deployment fails:
```bash
# Check buildpack
heroku buildpacks:set heroku/python

# Clear cache and redeploy
heroku plugins:install heroku-repo
heroku repo:purge_cache -a YOUR-APP-NAME
git push heroku main
```

### If custom domain doesn't work:
1. Wait for DNS propagation (up to 48h, usually < 1h)
2. Check Cloudflare SSL settings (must be Full, not Full Strict)
3. Verify CNAME target is correct
4. Clear browser cache

## Next Steps

After deployment:
1. Share your validator URL
2. Monitor usage in Heroku dashboard
3. Set up alerts in Cloudflare for traffic spikes
4. Consider upgrading if you exceed free tier limits

## Example Domains
- `digital-sangha.com` → Main site
- `validator.digital-sangha.com` → This validator
- `api.digital-sangha.com` → API endpoint

---

**Ready to validate AI dialogs with empirical rigor! 🚀**