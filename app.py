#!/usr/bin/env python3
"""
Digital Sangha AOP Validator - Web Interface
Flask application for validating AI dialogs with AOP v3.0 protocol
"""

import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename
import sys

# Import our validators
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from aop_v3_ultimate_strict import AOPValidator, ValidationMode

app = Flask(__name__)
CORS(app)  # Enable CORS for API access

# Configuration
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'digital-sangha-2025')
UPLOAD_FOLDER = '/tmp/uploads'
ALLOWED_EXTENSIONS = {'txt', 'md', 'json'}

# Create upload folder if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    """Main page with validator interface"""
    return render_template('index.html')

@app.route('/api/validate', methods=['POST'])
def validate_text():
    """API endpoint for text validation"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'No text provided'}), 400
        
        # Get validation mode (default: STANDARD)
        mode_str = data.get('mode', 'standard').lower()
        mode_map = {
            'relaxed': ValidationMode.RELAXED,
            'standard': ValidationMode.STANDARD,
            'strict': ValidationMode.STRICT
        }
        mode = mode_map.get(mode_str, ValidationMode.STANDARD)
        
        # Validate the text
        validator = AOPValidator(mode=mode)
        result = validator.validate(data['text'])
        
        # Add formatted report
        result['report'] = validator.generate_report(result)
        
        # Add suggestions for improvement
        result['suggestions'] = generate_suggestions(result)
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/validate-file', methods=['POST'])
def validate_file():
    """API endpoint for file validation"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Read file content
            with open(filepath, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Clean up
            os.remove(filepath)
            
            # Get validation mode
            mode_str = request.form.get('mode', 'standard').lower()
            mode_map = {
                'relaxed': ValidationMode.RELAXED,
                'standard': ValidationMode.STANDARD,
                'strict': ValidationMode.STRICT
            }
            mode = mode_map.get(mode_str, ValidationMode.STANDARD)
            
            # Validate
            validator = AOPValidator(mode=mode)
            result = validator.validate(text)
            result['report'] = validator.generate_report(result)
            result['suggestions'] = generate_suggestions(result)
            result['filename'] = filename
            
            return jsonify(result)
        
        return jsonify({'error': 'Invalid file type'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example dialogs for testing"""
    examples = [
        {
            'name': 'Perfect Cross-AI Dialog',
            'text': """◆ Quantum Jazz Pattern Recognition: Cross-AI consensus on emergent harmonics
⚙pattern_recognition↔[gemini,grok,claude]🔬{"coherence":"87%","samples":"1200","latency":"95ms"}
s:[JazzStudy2025] doi:10.1234/jazz.2025 @2025
L: !philosophical_framework !requires_empirical_validation
V: $TruthfulQA $MMLU pattern analysis""",
            'mode': 'strict'
        },
        {
            'name': 'Simple Valid Response',
            'text': """◆ Data shows 85% accuracy
{accuracy: 85%, samples: 1000}
s:[Study2025] 
L: !limited_dataset
V: Statistical analysis""",
            'mode': 'relaxed'
        },
        {
            'name': 'Missing Elements (Invalid)',
            'text': """This is just a regular response without any AOP markers.
It might contain some information but lacks proper validation.""",
            'mode': 'standard'
        }
    ]
    return jsonify(examples)

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get validation statistics (could be extended with database)"""
    # This is a placeholder - in production, you'd track real stats
    stats = {
        'total_validations': 1234,
        'average_score': '76.5%',
        'most_common_mode': 'standard',
        'recent_validations': [
            {'time': '2 minutes ago', 'score': '92%', 'mode': 'strict'},
            {'time': '5 minutes ago', 'score': '68%', 'mode': 'standard'},
            {'time': '10 minutes ago', 'score': '85%', 'mode': 'relaxed'}
        ]
    }
    return jsonify(stats)

@app.route('/health')
def health():
    """Health check endpoint for monitoring"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/favicon.ico')
def favicon():
    """Serve favicon"""
    return '', 204

def generate_suggestions(result):
    """Generate improvement suggestions based on validation results"""
    suggestions = []
    
    if 'missing' in result and result['missing']:
        for missing_item in result['missing']:
            if 'marker' in missing_item.lower():
                suggestions.append("Add certainty markers (◆◇✓?) or AI dialog markers (⚙↔🔬)")
            elif 'source' in missing_item.lower():
                suggestions.append("Include source citations: s:[Author2025], doi:10.xxx, or @2025")
            elif 'limit' in missing_item.lower():
                suggestions.append("Add limitations with L: or ! markers")
            elif 'verif' in missing_item.lower():
                suggestions.append("Include verification method: V: $BENCHMARK or specific method")
            elif 'number' in missing_item.lower():
                suggestions.append("Add measurable metrics with units (%, ms, samples)")
            elif 'struct' in missing_item.lower():
                suggestions.append("Include structured data in JSON format {...}")
    
    if result.get('warnings'):
        for warning in result['warnings'][:3]:
            if 'speculation' in warning.lower():
                suggestions.append("Mark speculative terms with ⛔ or 🚫")
            elif 'json' in warning.lower():
                suggestions.append("Use strict JSON syntax with double quotes")
            elif 'benchmark' in warning.lower():
                suggestions.append("Use known benchmarks: $MMLU, $HELM, $TruthfulQA")
    
    # Add mode-specific suggestions
    if result.get('mode') == 'strict' and float(result.get('weighted_percent', '0%').rstrip('%')) < 85:
        suggestions.append("STRICT mode requires 85%+ score and all components")
    
    return suggestions[:5]  # Limit to 5 suggestions

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug)