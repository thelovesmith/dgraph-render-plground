# Dgraph Standalone on Render

A secure, production-ready deployment of Dgraph standalone database on Render.com with authentication and nginx reverse proxy.

## 🏗️ Architecture Overview

This project deploys a secure Dgraph infrastructure with two main components:

1. **Dgraph Standalone** - Graph database service for storing and querying connected data
2. **Nginx Proxy** - Reverse proxy with authentication and SSL termination for secure access

## 🚀 Services

### 1. Dgraph Standalone (`dgraph/`)

A standalone Dgraph instance for graph database operations with persistent storage.

**Features:**
- 💾 Persistent storage (10GB disk)
- 🔧 Standalone configuration
- 🌐 GraphQL and admin interfaces
- 📈 Monitoring and health checks
- 🔐 Token-based authentication

**Key Endpoints:**
- GraphQL interface at `/graphql`
- Admin UI at port 8080
- Health check at `/health`
- gRPC endpoint at port 9080

### 2. Nginx Proxy (`nginx-proxy/`)

A reverse proxy service that provides secure access to Dgraph with authentication and SSL termination.

**Features:**
- 🔐 API token authentication
- 🌐 CORS enabled for web applications
- 🔒 SSL termination (handled by Render)
- 🏥 Health monitoring endpoints
- ⚡ gRPC and HTTP/2 support

**Key Endpoints:**
- `GET /health` - Proxy health check
- `/dgraph/*` - HTTP access to Dgraph (requires API token)
- `/` - gRPC access to Dgraph (requires API token)

## 📁 Project Structure

```
dgraph-render-plground/
├── README.md                    # This file
├── render.yaml                  # Render deployment configuration
├── dgraph/                      # Dgraph database service
│   ├── Dockerfile              # Container configuration
│   ├── dgraph-config.yml       # Dgraph configuration
│   ├── start.sh                # Startup script
│   └── README.md               # Service-specific documentation
└── nginx-proxy/                 # Nginx reverse proxy service
    ├── Dockerfile              # Container configuration
    ├── nginx.conf              # Nginx configuration
    └── README.md               # Service-specific documentation
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
  - type: pserv
    name: dgraph-standalone
    runtime: docker
    rootDir: dgraph/
    healthCheckPath: /health
    disk:
      name: dgraph-data
      mountPath: /dgraph/data
      sizeGB: 10
    # ... additional configuration
    
  - type: web
    name: nginx-proxy
    runtime: docker
    rootDir: nginx-proxy/
    healthCheckPath: /health
    # ... additional configuration
```

## 🔧 Configuration

### Environment Variables

#### Dgraph Service
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `PORT` | Server port | `8080` | Yes |
| `DGRAPH_ALPHA_BINDALL` | Allow all IP connections | `true` | Yes |
| `DGRAPH_TOKEN` | Dgraph authentication token | Auto-generated | Yes |
| `API_TOKEN` | Custom middleware token | Auto-generated | Yes |

#### Nginx Proxy Service
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `api_token` | API authentication token | Auto-generated | Yes |
| `dgraph_service_url` | Dgraph service URL | Auto-generated | Yes |

### Storage

- **Dgraph Data**: 10GB persistent disk mounted at `/dgraph/data`

## 🔑 Getting Your API Token

After deployment, you'll need to get your API token to access Dgraph:

1. **Go to Render Dashboard** → Your nginx-proxy service
2. **Navigate to Environment** tab
3. **Copy the `api_token` value** (auto-generated)
4. **Use this token** in your requests as `X-Api-Token` header

## 📊 Data Loading

### Loading Data into Dgraph

1. **Enable SSH** in Render for your Dgraph service
2. **Get SSH connection string** (click CONNECT > SSH)
3. **Copy exported files** to the Render disk:
```bash
scp ~/Downloads/pyp-export/* srv-d2sh3remcj7s73a5871g@ssh.oregon.render.com:/dgraph/data/export
```
4. **Load data** using dgraph live or bulk from the Render machine:
```bash
dgraph live -c 1 -f export/g01.rdf -s export/g01.schema -t "<DGRAPH_TOKEN>"
```

### Using the API

```bash
# Example GraphQL query through nginx-proxy
curl -X POST https://your-nginx-proxy.onrender.com/dgraph/graphql \
  -H "Content-Type: application/json" \
  -H "X-Api-Token: YOUR_API_TOKEN" \
  -d '{"query": "{ query { ... } }"}'
```
## 🧪 Testing

### Nginx Proxy Service

```bash
# Health check (no auth required)
curl https://your-nginx-proxy.onrender.com/health

# Test HTTP access to Dgraph (requires API token)
curl -H "X-Api-Token: YOUR_API_TOKEN" \
     https://your-nginx-proxy.onrender.com/dgraph/health

# Test gRPC access to Dgraph (requires API token)
curl -H "X-Api-Token: YOUR_API_TOKEN" \
     https://your-nginx-proxy.onrender.com/
```

### Dgraph Service (Direct Access)

```bash
# Health check (internal service)
curl https://your-dgraph-service.onrender.com/health

# State endpoint (internal service)
curl https://your-dgraph-service.onrender.com/state
```

## 📊 Monitoring

### Service Health

Both services provide health check endpoints for monitoring:
- Monitor service status through Render Dashboard
- Set up alerts for service downtime
- Check logs for performance metrics

### Resource Usage

- **Dgraph**: Varies based on data size (10GB disk allocated)
- **Nginx Proxy**: Lightweight, minimal resource usage
- **CPU**: Optimized for single-worker configurations

## 🔒 Security Considerations

### Nginx Proxy Service
- API token authentication required for all Dgraph access
- CORS configured for web application access
- SSL termination handled by Render
- Environment-based configuration for sensitive data

### Dgraph Service
⚠️ **Important**: Default configuration allows all IP connections

For production use:
1. Restrict `DGRAPH_ALPHA_WHITELIST` to specific IP ranges
2. Enable Dgraph authentication and ACLs
3. Use environment variables for sensitive configuration
4. Regular security updates

### Authentication Flow
1. All external requests go through nginx-proxy
2. nginx-proxy validates API token before forwarding to Dgraph
3. Dgraph service is not directly accessible from external networks
4. Tokens are auto-generated and can be rotated as needed

## 🚀 Performance

### Nginx Proxy Service
- **Response Time**: <100ms for proxy operations
- **Concurrency**: High throughput with nginx
- **Timeout**: 60 seconds configured for gRPC
- **SSL**: Terminated by Render for optimal performance

### Dgraph Service
- **Scaling**: Vertical scaling only (standalone mode)
- **Storage**: 10GB persistent disk
- **Backup**: Manual backup procedures recommended
- **gRPC**: Optimized for high-performance queries

## 🛠️ Local Development

### Dgraph Service

```bash
cd dgraph/
docker build -t dgraph-local .
docker run -p 8080:8080 -p 9080:9080 dgraph-local
```

### Nginx Proxy Service

```bash
cd nginx-proxy/
docker build -t nginx-proxy-local .
docker run -p 80:80 nginx-proxy-local
```

### Full Stack Local Development

```bash
# Terminal 1: Start Dgraph
cd dgraph/ && docker-compose up

# Terminal 2: Start Nginx Proxy
cd nginx-proxy/ && docker-compose up
```

## 📚 Documentation

- [Dgraph Service Documentation](dgraph/README.md) - Database setup and configuration
- [Nginx Proxy Documentation](nginx-proxy/README.md) - Proxy configuration and setup
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

1. **Authentication Failures**
   - Verify API token is correctly set in environment variables
   - Check token format in request headers (X-Api-Token or Authorization: Bearer)
   - Ensure nginx-proxy service is running and accessible

2. **Database Connection Issues**
   - Verify Dgraph service is running
   - Check port configurations (8080 for HTTP, 9080 for gRPC)
   - Review whitelist settings
   - Ensure nginx-proxy can reach Dgraph service

3. **Deployment Failures**
   - Check `render.yaml` syntax
   - Verify Dockerfile configurations
   - Review build logs in Render Dashboard
   - Ensure service dependencies are correct

4. **Proxy Configuration Issues**
   - Verify nginx.conf syntax
   - Check environment variable substitution
   - Review service URL configurations

### Getting Help

- Check service logs in Render Dashboard
- Review individual service README files
- Open an issue in this repository
- Contact Render support for platform-specific issues

---

