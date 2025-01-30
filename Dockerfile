# Use official nginx image
FROM nginx:alpine

# Set working directory to the main directory
WORKDIR /

# Install dependencies for potential future needs
RUN apk add --no-cache python3 py3-pip

# Copy required files to the root directory
COPY index.html .
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose new port
EXPOSE 8080

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
