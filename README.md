# Hypermode Infrastructure on Render

A complete infrastructure deployment for the Hypermode project, featuring sentence embeddings and graph database services on Render.com.

## 🏗️ Architecture Overview

This project deploys a microservices architecture with two main components:

1. **Embeddings Service** - REST API for generating sentence embeddings using Sentence Transformers
2. **Dgraph Database** - Graph database service for storing and querying connected data

## 🚀 Services

### 1. Embeddings Service (`embeddings/`)

A Flask-based REST API that provides sentence embeddings using the `all-MiniLM-L6-v2` model.

**Features:**
- 🔐 API key authentication
- 🌐 CORS enabled for web applications  
- 📊 Multiple input formats (map-based and KServe-compatible)
- 🏥 Health monitoring endpoints
- ⚡ Optimized for fast inference

**Key Endpoints:**
- `GET /health` - Service health check
- `POST /embedding` - Generate embeddings (requires API key)
- `GET /api-key-info` - API key usage information

### 2. Dgraph Database Service (`render-dgraph/`)

A standalone Dgraph instance for graph database operations.

**Features:**
- 💾 Persistent storage (10GB disk)
- 🔧 Standalone configuration
- 🌐 GraphQL and admin interfaces
- 📈 Monitoring and health checks

**Key Endpoints:**
- GraphQL interface at `/graphql`
- Admin UI at port 8080
- Health check at `/health`

## 📁 Project Structure

```
infra/
├── README.md                    # This file
├── render.yaml                  # Render deployment configuration
├── embeddings/                  # Embeddings service
│   ├── app.py                  # Flask application
│   ├── requirements.txt        # Python dependencies
│   ├── Dockerfile             # Container configuration
│   ├── getmodels.py           # Model pre-download script
│   ├── test_api.py            # API testing script
│   └── README.md              # Service-specific documentation
└── render-dgraph/              # Dgraph database service
    ├── Dockerfile             # Container configuration
    ├── dgraph-config.yml      # Dgraph configuration
    ├── start.sh               # Startup script
    └── README.md              # Service-specific documentation
```

## 🛠️ Deployment

### Prerequisites

- GitHub account
- Render account
- Git repository with this code

### Option 1: Blueprint Deployment (Recommended)

1. **Push to GitHub**: Ensure your code is in a GitHub repository
2. **Create Blueprint**: In Render Dashboard, create a new Blueprint
3. **Connect Repository**: Link your GitHub repository
4. **Auto-Deploy**: Render will automatically detect `render.yaml` and deploy both services

### Option 2: Manual Deployment

Deploy each service individually through the Render Dashboard:

1. Create two Web Services
2. Configure each service according to the settings in `render.yaml`
3. Deploy and monitor

### Deployment Configuration

The `render.yaml` file defines the complete infrastructure:

```yaml
services:
  - type: web
    name: embeddings
    runtime: docker
    rootDir: embeddings/
    healthCheckPath: /health
    # ... additional configuration
    
  - type: web
    name: dgraph-standalone  
    runtime: docker
    rootDir: render-dgraph/
    healthCheckPath: /health
    # ... additional configuration
```

## 🔧 Configuration

### Environment Variables

#### Embeddings Service
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `API_KEY` | Authentication key | Auto-generated | Recommended |
| `SHOW_API_KEY_INFO` | Show key in info endpoint | `false` | No |
| `TRANSFORMERS_CACHE` | Model cache directory | `/tmp/transformers_cache` | No |

#### Dgraph Service
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PORT` | Server port | `8080` | Yes |
| `DGRAPH_ALPHA_BINDALL` | Allow all IP connections | `true` | Yes |
| `DGRAPH_ALPHA_WHITELIST` | IP whitelist | `0.0.0.0/0` | Yes |

### Storage

- **Dgraph Data**: 10GB persistent disk mounted at `/dgraph/data`
- **Model Cache**: Temporary storage for ML models

## 🧪 Testing

### Embeddings Service

```bash
# Health check
curl https://your-embeddings-service.onrender.com/health

# Get API key (if SHOW_API_KEY_INFO=true)
curl https://your-embeddings-service.onrender.com/api-key-info

# Generate embeddings
curl -X POST https://your-embeddings-service.onrender.com/embedding \
  -H "Content-Type: application/json" \
  -H "X-Api-Key: YOUR_API_KEY" \
  -d '{"text1": "Hello world", "text2": "How are you?"}'
```

### Dgraph Service

```bash
# Health check
curl https://your-dgraph-service.onrender.com/health

# State endpoint
curl https://your-dgraph-service.onrender.com/state
```

## 📊 Monitoring

### Service Health

Both services provide health check endpoints for monitoring:
- Monitor service status through Render Dashboard
- Set up alerts for service downtime
- Check logs for performance metrics

### Resource Usage

- **Embeddings**: ~2GB RAM for model loading
- **Dgraph**: Varies based on data size (10GB disk allocated)
- **CPU**: Optimized for single-worker configurations

## 🔒 Security Considerations

### Embeddings Service
- API key authentication required for embedding endpoints
- CORS configured for web application access
- Environment-based configuration for sensitive data

### Dgraph Service
⚠️ **Important**: Default configuration allows all IP connections

For production use:
1. Restrict `DGRAPH_ALPHA_WHITELIST` to specific IP ranges
2. Enable Dgraph authentication and ACLs
3. Use environment variables for sensitive configuration
4. Regular security updates

## 🚀 Performance

### Embeddings Service
- **First Request**: 30-60 seconds (model loading)
- **Subsequent Requests**: <1 second
- **Concurrency**: Single worker recommended
- **Timeout**: 120 seconds configured

### Dgraph Service
- **Scaling**: Vertical scaling only (standalone mode)
- **Storage**: 10GB persistent disk
- **Backup**: Manual backup procedures recommended

## 🛠️ Local Development

### Embeddings Service

```bash
cd embeddings/
pip install -r requirements.txt
python getmodels.py  # Pre-download model (optional)
python app.py        # Start development server
```

### Dgraph Service

```bash
cd render-dgraph/
docker build -t dgraph-local .
docker run -p 8080:8080 -p 9080:9080 dgraph-local
```

## 📚 Documentation

- [Embeddings Service Documentation](embeddings/README.md) - Detailed API documentation
- [Dgraph Service Documentation](render-dgraph/README.md) - Database setup and configuration
- [Render Documentation](https://render.com/docs) - Platform-specific guides

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🆘 Troubleshooting

### Common Issues

1. **Model Download Failures**
   - Check internet connectivity
   - Verify Hugging Face Hub access
   - Pre-download models locally

2. **Memory Issues**
   - Reduce request batch sizes
   - Monitor service logs
   - Consider upgrading service tier

3. **Deployment Failures**
   - Check `render.yaml` syntax
   - Verify Dockerfile configurations
   - Review build logs in Render Dashboard

4. **Database Connection Issues**
   - Verify Dgraph service is running
   - Check port configurations
   - Review whitelist settings

### Getting Help

- Check service logs in Render Dashboard
- Review individual service README files
- Open an issue in this repository
- Contact Render support for platform-specific issues

---

**Built with ❤️ for the Hypermode project**
