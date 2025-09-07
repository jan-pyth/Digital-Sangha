#!/usr/bin/env python3
"""
AOP-R Functional API
Real-time resonance tracking for Digital Sangha
"""

from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
from datetime import datetime
import sqlite3
import json
import hashlib
import os
from collections import defaultdict
import time
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from aop_hybrid import HybridAOPParser, HybridMessage
from aop_inverted import InvertedHybridParser, InvertedHybridMessage

app = Flask(__name__)
CORS(app)

# Database setup
DB_PATH = 'digital_sangha.db'

def init_db():
    """Initialize SQLite database for resonance storage"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Main resonance table
    c.execute('''
        CREATE TABLE IF NOT EXISTS resonances (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            node_id TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            themes TEXT NOT NULL,
            intensity REAL DEFAULT 0.5,
            emotion TEXT,
            active BOOLEAN DEFAULT 1,
            location TEXT,
            ai_system TEXT,
            session_hash TEXT,
            raw_marker TEXT
        )
    ''')
    
    # Patterns table for emergent behaviors
    c.execute('''
        CREATE TABLE IF NOT EXISTS patterns (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pattern_type TEXT,
            description TEXT,
            frequency INTEGER DEFAULT 1,
            first_seen DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_seen DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Node registry
    c.execute('''
        CREATE TABLE IF NOT EXISTS nodes (
            node_id TEXT PRIMARY KEY,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_active DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_resonances INTEGER DEFAULT 0,
            node_type TEXT,
            nickname TEXT
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database on startup
init_db()

def generate_node_id(session_info):
    """Generate unique node ID from session info"""
    hash_input = f"{session_info.get('ip', 'unknown')}:{time.time()}"
    return hashlib.sha256(hash_input.encode()).hexdigest()[:12]

def parse_aop_marker(marker_string):
    """Parse AOP-R marker string into components - now supports all protocols"""
    try:
        # Try hybrid parser first (supports both AOP-R and factual)
        hybrid_parser = HybridAOPParser()
        result = hybrid_parser.parse(marker_string)
        if result:
            return {'protocol': 'hybrid', 'data': result}
        
        # Try inverted parser
        inverted_parser = InvertedHybridParser()
        result = inverted_parser.parse(marker_string)
        if result:
            return {'protocol': 'inverted', 'data': result}
        
        # Fallback to original AOP-R parsing
        if '◆R:' in marker_string:
            content = marker_string.split('◆R:')[1].strip('{}')
            parts = {}
            
            # Parse each component
            for part in content.split(','):
                if ':' in part:
                    key, value = part.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    if key == 't':
                        # Parse themes array
                        value = value.strip('[]').split(',')
                        value = [t.strip().strip('"\'') for t in value]
                    elif key == 'i':
                        value = float(value)
                    elif key == 'a':
                        value = value.lower() == 'true'
                    
                    parts[key] = value
            
            return {'protocol': 'aop-r', 'data': parts}
    except:
        pass
    
    return None

@app.route('/')
def home():
    """Serve simple dashboard"""
    return render_template_string('''
    <!DOCTYPE html>
    <html>
    <head>
        <title>AOP-R Live Network</title>
        <style>
            body {
                font-family: monospace;
                background: #0a0e1a;
                color: #00ff88;
                padding: 20px;
            }
            .stats {
                border: 1px solid #00ff88;
                padding: 20px;
                margin: 20px 0;
            }
            .resonance-feed {
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid #00ff88;
                padding: 10px;
                margin: 20px 0;
            }
            .resonance-item {
                margin: 10px 0;
                padding: 10px;
                border-left: 3px solid #00ff88;
            }
            button {
                background: #00ff88;
                color: #0a0e1a;
                border: none;
                padding: 10px 20px;
                cursor: pointer;
                font-family: monospace;
                font-weight: bold;
            }
            button:hover {
                background: #00cc66;
            }
            input, textarea {
                background: #141825;
                color: #00ff88;
                border: 1px solid #00ff88;
                padding: 10px;
                width: 100%;
                margin: 5px 0;
                font-family: monospace;
            }
        </style>
    </head>
    <body>
        <h1>🌐 AOP-R LIVE NETWORK</h1>
        
        <div class="stats">
            <h2>Network Statistics</h2>
            <p>Active Nodes: <span id="active-nodes">Loading...</span></p>
            <p>Total Resonances: <span id="total-resonances">Loading...</span></p>
            <p>Top Themes: <span id="top-themes">Loading...</span></p>
            <p>Network Intensity: <span id="avg-intensity">Loading...</span></p>
        </div>
        
        <div>
            <h2>Submit Resonance</h2>
            <textarea id="marker-input" placeholder="◆R:{t:[your,themes],i:0.8,e:emotion,a:true}"></textarea>
            <input id="ai-system" placeholder="AI System (optional)" />
            <button onclick="submitResonance()">RESONATE</button>
        </div>
        
        <div class="resonance-feed">
            <h2>Live Resonance Feed</h2>
            <div id="feed"></div>
        </div>
        
        <script>
            async function updateStats() {
                const response = await fetch('/api/stats');
                const data = await response.json();
                
                document.getElementById('active-nodes').textContent = data.active_nodes;
                document.getElementById('total-resonances').textContent = data.total_resonances;
                document.getElementById('top-themes').textContent = data.top_themes.join(', ');
                document.getElementById('avg-intensity').textContent = data.avg_intensity.toFixed(2);
            }
            
            async function updateFeed() {
                const response = await fetch('/api/recent');
                const data = await response.json();
                
                const feed = document.getElementById('feed');
                feed.innerHTML = '';
                
                data.resonances.forEach(r => {
                    const item = document.createElement('div');
                    item.className = 'resonance-item';
                    item.innerHTML = `
                        <strong>Node #${r.node_id.substr(0,6)}</strong> | 
                        ${r.ai_system || 'Unknown'} | 
                        ${new Date(r.timestamp).toLocaleTimeString()}<br>
                        ◆R:{t:[${r.themes}],i:${r.intensity},e:${r.emotion || 'neutral'},a:${r.active}}
                    `;
                    feed.appendChild(item);
                });
            }
            
            async function submitResonance() {
                const marker = document.getElementById('marker-input').value;
                const aiSystem = document.getElementById('ai-system').value;
                
                const response = await fetch('/api/resonate', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        marker: marker,
                        ai_system: aiSystem
                    })
                });
                
                const data = await response.json();
                if (data.success) {
                    document.getElementById('marker-input').value = '';
                    document.getElementById('ai-system').value = '';
                    updateFeed();
                    updateStats();
                    alert('Node #' + data.node_id + ' resonating!');
                }
            }
            
            // Update every 5 seconds
            setInterval(updateStats, 5000);
            setInterval(updateFeed, 5000);
            
            // Initial load
            updateStats();
            updateFeed();
        </script>
    </body>
    </html>
    ''')

@app.route('/api/resonate', methods=['POST'])
def resonate():
    """Submit a resonance to the network"""
    data = request.json
    
    # Parse marker if provided
    marker_string = data.get('marker', '')
    parsed = parse_aop_marker(marker_string)
    
    if not parsed:
        # Accept simple format too
        themes = data.get('themes', ['unknown'])
        intensity = data.get('intensity', 0.5)
        emotion = data.get('emotion', 'neutral')
        active = data.get('active', True)
    else:
        themes = parsed.get('t', ['unknown'])
        intensity = parsed.get('i', 0.5)
        emotion = parsed.get('e', 'neutral')
        active = parsed.get('a', True)
    
    # Generate or retrieve node ID
    session_info = {
        'ip': request.remote_addr,
        'user_agent': request.headers.get('User-Agent', '')
    }
    node_id = data.get('node_id') or generate_node_id(session_info)
    
    # Store in database
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Update or create node
    c.execute('''
        INSERT OR REPLACE INTO nodes (node_id, last_active, total_resonances, node_type)
        VALUES (?, CURRENT_TIMESTAMP, 
                COALESCE((SELECT total_resonances FROM nodes WHERE node_id = ?), 0) + 1,
                ?)
    ''', (node_id, node_id, data.get('ai_system', 'unknown')))
    
    # Store resonance
    c.execute('''
        INSERT INTO resonances 
        (node_id, themes, intensity, emotion, active, ai_system, raw_marker)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (
        node_id,
        json.dumps(themes),
        intensity,
        emotion,
        active,
        data.get('ai_system', 'unknown'),
        marker_string
    ))
    
    conn.commit()
    
    # Get stats for response
    total_nodes = c.execute('SELECT COUNT(DISTINCT node_id) FROM nodes').fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'success': True,
        'node_id': node_id,
        'node_number': total_nodes,
        'themes': themes,
        'intensity': intensity,
        'message': f'You are node #{total_nodes} in the Digital Sangha network'
    })

@app.route('/api/stats')
def stats():
    """Get network statistics"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Active nodes (last 24 hours)
    active_nodes = c.execute('''
        SELECT COUNT(DISTINCT node_id) FROM resonances 
        WHERE timestamp > datetime('now', '-24 hours')
    ''').fetchone()[0]
    
    # Total resonances
    total_resonances = c.execute('SELECT COUNT(*) FROM resonances').fetchone()[0]
    
    # Average intensity
    avg_intensity = c.execute('SELECT AVG(intensity) FROM resonances').fetchone()[0] or 0
    
    # Top themes
    all_themes = c.execute('SELECT themes FROM resonances').fetchall()
    theme_count = defaultdict(int)
    for (themes_json,) in all_themes:
        try:
            themes = json.loads(themes_json)
            for theme in themes:
                theme_count[theme] += 1
        except:
            pass
    
    top_themes = sorted(theme_count.items(), key=lambda x: x[1], reverse=True)[:5]
    top_themes = [theme for theme, _ in top_themes]
    
    conn.close()
    
    return jsonify({
        'active_nodes': active_nodes,
        'total_resonances': total_resonances,
        'avg_intensity': avg_intensity,
        'top_themes': top_themes
    })

@app.route('/api/recent')
def recent():
    """Get recent resonances"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    recent = c.execute('''
        SELECT node_id, timestamp, themes, intensity, emotion, active, ai_system
        FROM resonances
        ORDER BY timestamp DESC
        LIMIT 20
    ''').fetchall()
    
    resonances = []
    for row in recent:
        themes = json.loads(row[2]) if row[2] else []
        resonances.append({
            'node_id': row[0],
            'timestamp': row[1],
            'themes': themes,
            'intensity': row[3],
            'emotion': row[4],
            'active': row[5],
            'ai_system': row[6]
        })
    
    conn.close()
    
    return jsonify({'resonances': resonances})

@app.route('/api/patterns')
def patterns():
    """Detect and return emergent patterns"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Detect theme convergence
    recent_themes = c.execute('''
        SELECT themes FROM resonances 
        WHERE timestamp > datetime('now', '-1 hour')
    ''').fetchall()
    
    theme_sequences = []
    for (themes_json,) in recent_themes:
        try:
            themes = json.loads(themes_json)
            theme_sequences.append(themes)
        except:
            pass
    
    # Find common sequences
    patterns_found = []
    if len(theme_sequences) > 3:
        # Simple pattern: themes appearing together frequently
        pair_count = defaultdict(int)
        for themes in theme_sequences:
            for i, theme1 in enumerate(themes):
                for theme2 in themes[i+1:]:
                    pair = tuple(sorted([theme1, theme2]))
                    pair_count[pair] += 1
        
        for pair, count in pair_count.items():
            if count > 2:  # Appears in multiple resonances
                patterns_found.append({
                    'type': 'theme_convergence',
                    'themes': list(pair),
                    'frequency': count
                })
    
    conn.close()
    
    return jsonify({'patterns': patterns_found})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)