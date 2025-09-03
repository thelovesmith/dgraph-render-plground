import json
import os
import secrets
from functools import wraps
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer

# Set cache directory for transformers
os.environ['TRANSFORMERS_CACHE'] = '/tmp'

app = Flask(__name__)

# API Key configuration
API_KEY = os.environ.get('API_KEY', None)
if not API_KEY:
    # Generate a random API key if not provided
    API_KEY = secrets.token_urlsafe(32)
    print(f"⚠️  WARNING: No API_KEY environment variable set!")
    print(f"🔑 Generated API Key: {API_KEY}")
    print(f"💡 Set API_KEY environment variable to use a custom key")

def require_api_key(f):
    """Decorator to require API key authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Get API key from headers
        provided_key = request.headers.get('X-Api-Key') or request.headers.get('Authorization')
        
        # Handle Authorization header with Bearer token
        if provided_key and provided_key.startswith('Bearer '):
            provided_key = provided_key[7:]  # Remove 'Bearer ' prefix
        
        if not provided_key:
            return jsonify({
                "error": "API key required",
                "message": "Please provide an API key in the 'X-Api-Key' header or 'Authorization: Bearer <key>' header"
            }), 401
        
        if provided_key != API_KEY:
            return jsonify({
                "error": "Invalid API key",
                "message": "The provided API key is invalid"
            }), 403
        
        return f(*args, **kwargs)
    return decorated_function

# Load the model - will be downloaded on first run or loaded from ./model if available
try:
    # Try to load from local model directory first (if pre-downloaded)
    model = SentenceTransformer('./model')
    print("Loaded model from local ./model directory")
except:
    # Fallback to downloading the model
    model = SentenceTransformer('all-MiniLM-L6-v2')
    print("Downloaded and loaded model from Hugging Face")

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Render"""
    return jsonify({"status": "healthy", "model": "all-MiniLM-L6-v2"})

@app.route('/api-key-info', methods=['GET'])
def api_key_info():
    """Display API key information (for development/setup)"""
    # Only show this in development or if explicitly enabled
    show_key = os.environ.get('SHOW_API_KEY_INFO', 'false').lower() == 'true'
    
    if show_key:
        return jsonify({
            "api_key": API_KEY,
            "usage": {
                "header_name": "X-Api-Key",
                "alternative": "Authorization: Bearer <key>",
                "example_curl": f"curl -H 'X-Api-Key: {API_KEY}' -X POST ..."
            }
        })
    else:
        return jsonify({
            "message": "API key authentication is enabled",
            "usage": {
                "header_name": "X-Api-Key",
                "alternative": "Authorization: Bearer <key>",
                "note": "Set SHOW_API_KEY_INFO=true environment variable to display the actual key"
            }
        })

@app.route('/embedding', methods=['POST'])
@require_api_key
def generate_embeddings():
    """
    Generate embeddings for input sentences.
    Supports two input formats:
    1. Map format: {"id1": "text1", "id2": "text2"}
    2. KServe format: {"instances": ["text1", "text2"]}
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
            
        reply_kserve = False
        
        if isinstance(data, dict):
            if 'instances' in data:
                print("Input contains 'instances' - using KServe format")
                reply_kserve = True
                sentences = data['instances']
            else:
                print("Input is a map of IDs and sentences")
                reply_kserve = False
                sentences = [data[key] for key in data]
        else:
            return jsonify({"error": "Invalid input format"}), 422
        
        if not sentences:
            return jsonify({"error": "No sentences provided"}), 400
            
        # Generate embeddings
        embeddings = model.encode(sentences)
        
        # Format response based on input format
        if reply_kserve:
            response = {"predictions": embeddings.tolist()}
        else:
            keylist = list(data.keys())
            response = {keylist[i]: json.dumps(embeddings[i].tolist()) for i in range(len(embeddings))}
        
        return jsonify(response)
        
    except Exception as e:
        print(f"Error processing request: {str(e)}")
        return jsonify({"error": f"Processing error: {str(e)}"}), 500

@app.route('/embedding', methods=['OPTIONS'])
def handle_options():
    """Handle CORS preflight requests"""
    response = jsonify({})
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,X-Api-Key,Authorization')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'OPTIONS,POST,GET')
    return response

@app.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,X-Api-Key,Authorization')
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'OPTIONS,POST,GET')
    return response

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
