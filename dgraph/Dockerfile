FROM dgraph/standalone:v25.0.0-preview6

# Create directories for data and config
RUN mkdir -p /dgraph/data /dgraph/config

# Copy configuration files
COPY dgraph-config.yml /dgraph/config/

# Set working directory
WORKDIR /dgraph/data

# Expose the Dgraph ports
EXPOSE 7080 8080 9080 8000

# Start Dgraph in standalone mode
COPY start.sh /
RUN chmod +x /start.sh

CMD ["/start.sh"]
