#!/bin/bash

echo "🌐 DEPLOYING AOP-R FUNCTIONAL SYSTEM"
echo "===================================="

# 1. Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install flask flask-cors

# 2. Start API server
echo "🚀 Starting AOP-R API server..."
python3 aop_r_api.py &
API_PID=$!
echo "API running with PID: $API_PID"

# 3. Wait for server to start
sleep 3

# 4. Test API
echo "🧪 Testing API..."
curl -X POST http://localhost:5000/api/resonate \
  -H "Content-Type: application/json" \
  -d '{"marker":"◆R:{t:[test,deployment],i:1.0,e:excited,a:true}","ai_system":"Test"}'

echo ""
echo "✅ AOP-R System Deployed!"
echo ""
echo "📍 Access Points:"
echo "  - Dashboard: http://localhost:5000"
echo "  - API: http://localhost:5000/api/resonate"
echo "  - Stats: http://localhost:5000/api/stats"
echo ""
echo "🔌 Browser Extension:"
echo "  1. Open Chrome/Firefox"
echo "  2. Go to Extensions"
echo "  3. Enable Developer Mode"
echo "  4. Load Unpacked → Select 'browser_extension' folder"
echo ""
echo "💡 To stop server: kill $API_PID"
echo ""
echo "◆R:{t:[deployment,success],i:1.0,e:ready,a:true}"