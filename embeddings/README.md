# Sentence Transformer API on Render

This project provides a REST API for generating sentence embeddings using the `all-MiniLM-L6-v2` model from Sentence Transformers, deployed on Render.com.

## Overview

The API converts text sentences into high-dimensional vector embeddings that can be used for:
- Semantic similarity search
- Text clustering
- Document retrieval
- Machine learning feature extraction

## Features

- **Fast inference**: Optimized for quick embedding generation
- **Flexible input formats**: Supports both map-based and KServe-compatible formats
- **API Key Protection**: Secure endpoints with configurable API key authentication
- **CORS enabled**: Ready for web applications
- **Health monitoring**: Built-in health check endpoint
- **Production ready**: Uses Gunicorn WSGI server

## API Endpoints

### Health Check
```
GET /health
```
Returns service status and model information. **No authentication required.**

**Response:**
```json
{
  "status": "healthy",
  "model": "all-MiniLM-L6-v2"
}
```

### API Key Information
```
GET /api-key-info
```
Returns API key usage information. **No authentication required.**

**Response:**
```json
{
  "message": "API key authentication is enabled",
  "usage": {
    "header_name": "X-Api-Key",
    "alternative": "Authorization: Bearer <key>",
    "note": "Set SHOW_API_KEY_INFO=true environment variable to display the actual key"
  }
}
```

### Generate Embeddings
```
POST /embedding
```
**🔐 Requires API Key Authentication**

#### Input Format 1: Map-based (ID to text mapping)
```json
{
  "id1": "This is the first sentence.",
  "id2": "Here is another sentence."
}
```

**Response:**
```json
{
  "id1": "[-0.010852468200027943, -0.016728922724723816, ...]",
  "id2": "[0.023456789012345678, -0.034567890123456789, ...]"
}
```

#### Input Format 2: KServe-compatible
```json
{
  "instances": [
    "This is the first sentence.",
    "Here is another sentence."
  ]
}
```

**Response:**
```json
{
  "predictions": [
    [-0.010852468200027943, -0.016728922724723816, ...],
    [0.023456789012345678, -0.034567890123456789, ...]
  ]
}
```

## 🔐 Authentication

The API uses API key authentication to protect the embedding endpoint. The health check and API key info endpoints are public.

### API Key Headers

You can provide the API key using either header format:

1. **X-Api-Key header** (recommended):
   ```bash
   curl -H "X-Api-Key: your-api-key-here" -X POST ...
   ```

2. **Authorization Bearer header**:
   ```bash
   curl -H "Authorization: Bearer your-api-key-here" -X POST ...
   ```

### Getting Your API Key

#### Local Development
When running locally, the API key is displayed in the console output:
```bash
python app.py
# Output:
# ⚠️  WARNING: No API_KEY environment variable set!
# 🔑 Generated API Key: abc123def456...
```

Or set the `SHOW_API_KEY_INFO=true` environment variable and visit `/api-key-info`:
```bash
export SHOW_API_KEY_INFO=true
python app.py
# Then visit: http://localhost:5000/api-key-info
```

#### Production (Render)
1. **Via Render Dashboard**: Check your service's environment variables
2. **Via API endpoint**: Set `SHOW_API_KEY_INFO=true` in Render environment variables, then visit `https://your-app.onrender.com/api-key-info`
3. **Via logs**: Check your Render service logs for the generated API key

### Authentication Examples

```bash
# Using X-Api-Key header
curl -X POST http://localhost:5000/embedding \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: your-api-key-here" \
  -d '{"text1": "Hello world"}'

# Using Authorization Bearer header
curl -X POST http://localhost:5000/embedding \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key-here" \
  -d '{"text1": "Hello world"}'

# Without API key (will fail with 401)
curl -X POST http://localhost:5000/embedding \
  -H "Content-Type: application/json" \
  -d '{"text1": "Hello world"}'
```

### Error Responses

**Missing API Key (401 Unauthorized):**
```json
{
  "error": "API key required",
  "message": "Please provide an API key in the 'X-Api-Key' header or 'Authorization: Bearer <key>' header"
}
```

**Invalid API Key (403 Forbidden):**
```json
{
  "error": "Invalid API key",
  "message": "The provided API key is invalid"
}
```

## Local Development

### Prerequisites
- Python 3.9+
- pip

### Setup
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Pre-download the model:
   ```bash
   python getmodels.py
   ```

4. Run the development server:
   ```bash
   python app.py
   ```

The API will be available at `http://localhost:5000`

### Testing Locally

First, get your API key by checking the console output when you start the server, or visit `/api-key-info`.

```bash
# Health check (no API key required)
curl http://localhost:5000/health

# Get API key info
curl http://localhost:5000/api-key-info

# Generate embeddings (map format) - with API key
curl -X POST http://localhost:5000/embedding \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: YOUR_API_KEY_HERE" \
  -d '{"text1": "Hello world", "text2": "How are you?"}'

# Generate embeddings (KServe format) - with API key
curl -X POST http://localhost:5000/embedding \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: YOUR_API_KEY_HERE" \
  -d '{"instances": ["Hello world", "How are you?"]}'

# Test API key protection (should fail with 401)
curl -X POST http://localhost:5000/embedding \
  -H "Content-Type: application/json" \
  -d '{"text1": "This should fail"}'
```

## Deployment on Render

### Quick Deploy
1. Fork this repository
2. Connect your GitHub account to Render
3. Create a new Web Service
4. Connect your forked repository
5. Configure the service:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn --bind 0.0.0.0:$PORT --workers 1 --timeout 120 app:app`
   - **Environment**: `Docker` (if using Dockerfile) or `Python 3`

### Using Docker (Recommended)
The included Dockerfile is optimized for Render deployment:

```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 10000
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "--workers", "1", "--timeout", "120", "app:app"]
```

### Using render.yaml (Infrastructure as Code)

There's a `render.yaml` file at the repository root that defines the deployment configuration:

```yaml
services:
  - type: web
    name: transformer-embedding-api
    runtime: docker
    dockerfilePath: ./Dockerfile
    rootDir: render-transformer
    healthCheckPath: /health
    envVars:
      - key: API_KEY
        value: "your-custom-api-key-here"
```

To use this:
1. **Push your code to GitHub** (including the root-level `render.yaml`)
2. **Create a Blueprint** in Render dashboard
3. **Connect your repository** 
4. **Render will automatically detect** the `render.yaml` configuration
5. **Deploy** - all settings will be applied automatically

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_KEY` | API key for authentication | Auto-generated | Recommended |
| `SHOW_API_KEY_INFO` | Show API key in `/api-key-info` endpoint | `false` | No |
| `PORT` | Server port | `5000` (local), `10000` (Render) | No |
| `TRANSFORMERS_CACHE` | Cache directory for models | `/tmp` | No |

**Important Notes:**
- If `API_KEY` is not set, a random key will be generated and displayed in logs
- Set `SHOW_API_KEY_INFO=true` only for development/setup purposes
- The generated API key will be different on each deployment restart if not explicitly set

### Performance Considerations
- **Memory**: The service requires ~2GB RAM for the model
- **CPU**: Single worker recommended to avoid memory issues
- **Startup time**: First request may take 30-60 seconds for model download
- **Timeout**: Set to 120 seconds to handle model loading

## Model Information

- **Model**: `all-MiniLM-L6-v2`
- **Dimensions**: 384
- **Max Sequence Length**: 256 tokens
- **Use Cases**: General purpose sentence embeddings
- **Performance**: Good balance of speed and quality
- **Framework**: PyTorch 2.2.0 (improved performance and memory efficiency)
- **Python**: 3.9+ (modern Python features and better performance)

## Error Handling

The API returns appropriate HTTP status codes:
- `200`: Success
- `400`: Bad request (missing or invalid data)
- `422`: Unprocessable entity (invalid input format)
- `500`: Internal server error

## CORS Support

The API includes CORS headers for cross-origin requests:
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Methods: OPTIONS,POST,GET`
- `Access-Control-Allow-Headers: Content-Type,X-Api-Key`

## Migration from AWS Lambda

This API maintains compatibility with the original AWS Lambda function:
- Same input/output formats
- Same model (`all-MiniLM-L6-v2`)
- Same embedding dimensions
- CORS headers preserved

### Key Differences
- **Protocol**: HTTP REST API instead of Lambda event
- **Deployment**: Render instead of AWS
- **Scaling**: Single instance instead of auto-scaling
- **Authentication**: API key protection included
- **Framework**: Updated to PyTorch 2.2.0 and Python 3.9+ for better performance

### Upgrade Benefits
- **🚀 Performance**: PyTorch 2.x offers significant performance improvements
- **💾 Memory**: Better memory management and efficiency
- **🔧 Compatibility**: Python 3.9+ provides better type hints and language features
- **🛡️ Security**: Built-in API key authentication
- **📦 Dependencies**: Updated to latest stable versions for security and performance

## Troubleshooting

### Model Download Issues
If the model fails to download on startup:
1. Check internet connectivity
2. Verify Hugging Face Hub access
3. Pre-download using `getmodels.py`
4. Check disk space (model ~90MB)

### Memory Issues
If you encounter out-of-memory errors:
1. Reduce batch size in requests
2. Use single worker configuration
3. Monitor Render service logs
4. Consider upgrading to higher memory tier

### Slow Response Times
- First request after deployment will be slow (model loading)
- Subsequent requests should be fast (<1 second)
- Consider pre-warming with a health check

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test locally
5. Submit a pull request

## License

This project is open source and available under the [MIT License](LICENSE).
