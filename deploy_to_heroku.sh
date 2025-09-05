#!/bin/bash

echo "==================================="
echo "🚀 Digital Sangha Heroku Deployment"
echo "==================================="
echo ""
echo "This script will help you deploy to Heroku."
echo ""

# Step 1: Login to Heroku
echo "Step 1: Login to Heroku"
echo "------------------------"
echo "Please run: heroku login"
echo "Press Enter after you've logged in..."
read

# Step 2: Create Heroku app
echo ""
echo "Step 2: Create Heroku app"
echo "-------------------------"
echo "Trying to create app 'digital-sangha'..."
heroku create digital-sangha 2>/dev/null

if [ $? -ne 0 ]; then
    echo "Name 'digital-sangha' is taken. Trying 'digital-sangha-validator'..."
    heroku create digital-sangha-validator 2>/dev/null
    
    if [ $? -ne 0 ]; then
        echo "That's also taken. Trying 'digital-sangha-aop'..."
        heroku create digital-sangha-aop 2>/dev/null
        
        if [ $? -ne 0 ]; then
            echo ""
            echo "❌ All suggested names are taken."
            echo "Please create manually with: heroku create YOUR-UNIQUE-NAME"
            echo "Enter your app name: "
            read APP_NAME
            heroku create $APP_NAME
        fi
    fi
fi

# Step 3: Get app info
echo ""
echo "Step 3: Getting app info..."
echo "---------------------------"
APP_URL=$(heroku info -s | grep web_url | cut -d= -f2)
APP_NAME=$(heroku info -s | grep name | cut -d= -f2)

echo "✅ App created!"
echo "Name: $APP_NAME"
echo "URL: $APP_URL"

# Step 4: Add custom domains
echo ""
echo "Step 4: Adding custom domains"
echo "-----------------------------"
heroku domains:add digital-sangha.org
heroku domains:add www.digital-sangha.org
echo "✅ Domains added!"

# Step 5: Set environment variables
echo ""
echo "Step 5: Setting environment variables"
echo "-------------------------------------"
SECRET_KEY=$(python3 -c 'import secrets; print(secrets.token_hex(32))')
heroku config:set SECRET_KEY=$SECRET_KEY
heroku config:set FLASK_ENV=production
echo "✅ Environment configured!"

# Step 6: Deploy
echo ""
echo "Step 6: Deploying to Heroku"
echo "---------------------------"
git push heroku main

if [ $? -ne 0 ]; then
    echo "Trying to push from current branch..."
    BRANCH=$(git branch --show-current)
    git push heroku $BRANCH:main
fi

# Step 7: Open the app
echo ""
echo "==================================="
echo "✅ DEPLOYMENT COMPLETE!"
echo "==================================="
echo ""
echo "Your app is deployed at: $APP_URL"
echo ""
echo "Next steps:"
echo "1. Configure Cloudflare DNS:"
echo "   - Add CNAME record: @ -> $APP_NAME.herokuapp.com"
echo "   - Add CNAME record: www -> digital-sangha.org"
echo ""
echo "2. In Cloudflare SSL/TLS settings:"
echo "   - Set encryption mode to 'Full' (not Full Strict)"
echo "   - Enable 'Always Use HTTPS'"
echo ""
echo "3. Your site will be live at:"
echo "   https://digital-sangha.org"
echo ""
echo "Opening your Heroku app now..."
heroku open