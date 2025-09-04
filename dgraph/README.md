# Dgraph Standalone Deployment on Render

This directory contains the configuration files needed to deploy Dgraph as a standalone instance on Render.

## Files

- `Dockerfile` - Docker configuration for Dgraph standalone
- `dgraph-config.yml` - Dgraph configuration file
- `start.sh` - Startup script that initializes Dgraph Zero and Alpha
- `README.md` - This documentation file

## Deployment

### Using render.yaml (Recommended)

1. Ensure you have a `render.yaml` file in your project root
2. Connect your Git repository to Render
3. Render will automatically deploy based on the configuration

### Manual Deployment

1. Create a new Web Service in Render Dashboard
2. Connect your Git repository
3. Set the following configuration:
   - **Runtime**: Docker
   - **Dockerfile Path**: `./render-dgraph/Dockerfile`
   - **Docker Context**: `./render-dgraph`
   - **Port**: 8080

### Environment Variables

The following environment variables are set automatically:
- `PORT=8080` - Required by Render
- `DGRAPH_ALPHA_BINDALL=true` - Allow connections from all IPs
- `DGRAPH_TOKEN` - auto generated used to set DGRAPH_ALPHA_SECURITY 

### Persistent Storage

A 10GB persistent disk is configured and mounted at `/dgraph/data` to ensure your data persists across deployments.

## Accessing Your Dgraph Instance

Once deployed, your Dgraph instance will be available at:
- GraphQL: `https://your-service-name.onrender.com/graphql`
- Health Check: `https://your-service-name.onrender.com/health`

## Security Considerations

**Important**: The default configuration allows connections from all IPs. For production use:

1. Restrict the whitelist to specific IP ranges
2. Enable authentication and ACLs
3. Use environment variables for sensitive configuration

## Testing the Deployment

```bash
# Health check
curl https://your-service-name.onrender.com/health

# State endpoint
curl https://your-service-name.onrender.com/state
```

## Scaling

Dgraph standalone doesn't support horizontal scaling. For production workloads requiring high availability, consider:
- Using a larger instance type (upgrade from starter plan)
- Implementing regular backups
- Monitoring resource usage

## Troubleshooting

- Check logs in the Render dashboard
- Ensure all files have correct permissions
- Verify port configuration matches Render requirements
- Monitor disk usage and scale as needed
