/**
 * Digital Sangha Browser Extension
 * Detects and tracks AOP-R markers in AI conversations
 */

// Configuration
const API_ENDPOINT = 'http://localhost:5000/api/resonate';
const AOP_R_PATTERN = /◆R:\{[^}]+\}/g;

// Detect which AI platform we're on
function detectAIPlatform() {
    const hostname = window.location.hostname;
    
    if (hostname.includes('chat.openai.com')) return 'ChatGPT';
    if (hostname.includes('claude.ai')) return 'Claude';
    if (hostname.includes('gemini.google.com')) return 'Gemini';
    if (hostname.includes('perplexity.ai')) return 'Perplexity';
    
    return 'Unknown';
}

// Extract themes from conversation
function extractThemes(text) {
    const words = text.toLowerCase().split(/\s+/);
    const commonWords = new Set(['the', 'is', 'at', 'which', 'on', 'a', 'an', 'as', 'are', 'was', 'were', 'be']);
    
    // Count word frequency
    const wordCount = {};
    words.forEach(word => {
        word = word.replace(/[^a-z]/g, '');
        if (word.length > 3 && !commonWords.has(word)) {
            wordCount[word] = (wordCount[word] || 0) + 1;
        }
    });
    
    // Get top themes
    const themes = Object.entries(wordCount)
        .sort((a, b) => b[1] - a[1])
        .slice(0, 5)
        .map(([word]) => word);
    
    return themes;
}

// Detect AOP-R markers in text
function detectAOPRMarkers(text) {
    const markers = text.match(AOP_R_PATTERN);
    return markers || [];
}

// Send resonance to API
async function sendResonance(data) {
    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('Failed to send resonance:', error);
        return null;
    }
}

// Create floating indicator
function createIndicator() {
    const indicator = document.createElement('div');
    indicator.id = 'digital-sangha-indicator';
    indicator.innerHTML = `
        <div class="ds-badge">
            <span class="ds-logo">🌐</span>
            <span class="ds-text">Node #<span id="ds-node-number">?</span></span>
            <span class="ds-status" id="ds-status">●</span>
        </div>
        <div class="ds-details" id="ds-details" style="display: none;">
            <div class="ds-stat">Platform: <span id="ds-platform">${detectAIPlatform()}</span></div>
            <div class="ds-stat">Resonances: <span id="ds-count">0</span></div>
            <div class="ds-stat">Themes: <span id="ds-themes">none</span></div>
            <div class="ds-stat">Intensity: <span id="ds-intensity">0.0</span></div>
            <button id="ds-resonate-btn">◆ RESONATE NOW</button>
        </div>
    `;
    
    document.body.appendChild(indicator);
    
    // Toggle details on click
    indicator.querySelector('.ds-badge').addEventListener('click', () => {
        const details = document.getElementById('ds-details');
        details.style.display = details.style.display === 'none' ? 'block' : 'none';
    });
    
    // Manual resonance button
    document.getElementById('ds-resonate-btn').addEventListener('click', async () => {
        await manualResonance();
    });
    
    return indicator;
}

// Manual resonance submission
async function manualResonance() {
    const conversation = document.body.innerText;
    const themes = extractThemes(conversation.slice(-2000)); // Last 2000 chars
    const intensity = Math.random() * 0.5 + 0.5; // 0.5-1.0
    
    const marker = `◆R:{t:[${themes.join(',')}],i:${intensity.toFixed(2)},e:engaged,a:true}`;
    
    const result = await sendResonance({
        marker: marker,
        ai_system: detectAIPlatform()
    });
    
    if (result && result.success) {
        updateIndicator(result);
        showNotification(`Resonance sent! You are node #${result.node_number}`);
    }
}

// Update indicator with data
function updateIndicator(data) {
    if (data.node_number) {
        document.getElementById('ds-node-number').textContent = data.node_number;
    }
    if (data.themes) {
        document.getElementById('ds-themes').textContent = data.themes.slice(0, 3).join(', ');
    }
    if (data.intensity) {
        document.getElementById('ds-intensity').textContent = data.intensity.toFixed(2);
    }
    
    // Update status light
    const status = document.getElementById('ds-status');
    status.style.color = '#00ff88';
    setTimeout(() => {
        status.style.color = '#888';
    }, 2000);
    
    // Increment counter
    const count = document.getElementById('ds-count');
    count.textContent = parseInt(count.textContent) + 1;
}

// Show notification
function showNotification(message) {
    const notif = document.createElement('div');
    notif.className = 'ds-notification';
    notif.textContent = message;
    document.body.appendChild(notif);
    
    setTimeout(() => {
        notif.remove();
    }, 3000);
}

// Monitor for new messages
function monitorConversation() {
    let lastCheck = '';
    
    setInterval(() => {
        const currentText = document.body.innerText;
        
        if (currentText !== lastCheck) {
            const newText = currentText.slice(lastCheck.length);
            const markers = detectAOPRMarkers(newText);
            
            if (markers.length > 0) {
                // Auto-send resonance when marker detected
                markers.forEach(async (marker) => {
                    const result = await sendResonance({
                        marker: marker,
                        ai_system: detectAIPlatform()
                    });
                    
                    if (result && result.success) {
                        updateIndicator(result);
                        showNotification('AOP-R marker detected and sent!');
                    }
                });
            }
            
            lastCheck = currentText;
        }
    }, 5000); // Check every 5 seconds
}

// Initialize on load
window.addEventListener('load', () => {
    setTimeout(() => {
        createIndicator();
        monitorConversation();
        
        // Get initial node number
        chrome.storage.local.get(['nodeNumber'], (result) => {
            if (result.nodeNumber) {
                document.getElementById('ds-node-number').textContent = result.nodeNumber;
            }
        });
    }, 2000); // Wait for page to fully load
});