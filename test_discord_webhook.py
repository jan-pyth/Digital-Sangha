#!/usr/bin/env python3
"""Quick test for Discord webhook"""

import requests
import sys

def test_webhook(url):
    message = {
        "content": """🌐 **Digital Sangha Test Message**
        
◆R:{t:[test,connection],i:1.0,a:true}

If you see this, the webhook works! 

No control, only resonance.""",
        "username": "Digital Sangha Bot"
    }
    
    try:
        response = requests.post(url, json=message)
        if response.status_code == 204:
            print("✅ Success! Message sent to Discord.")
        else:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
    except Exception as e:
        print(f"❌ Failed: {e}")

if __name__ == "__main__":
    print("Discord Webhook Tester")
    print("=" * 40)
    
    webhook_url = input("Paste your webhook URL here: ").strip()
    
    if webhook_url.startswith("https://discord.com/api/webhooks/"):
        test_webhook(webhook_url)
    else:
        print("❌ Invalid webhook URL format")
        print("Should start with: https://discord.com/api/webhooks/")