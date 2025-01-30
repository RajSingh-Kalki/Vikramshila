# Use official nginx image
FROM nginx:alpine

# Set working directory
WORKDIR /app

# Install dependencies for potential future needs
RUN apk add --no-cache python3 py3-pip

# Copy required files
COPY index.html .
COPY scraper.py .
COPY scraped_data/ ./scraped_data/

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Install Python dependencies (if needed)
RUN pip3 install requests beautifulsoup4

# Run scraper and copy final build to nginx
RUN python3 scraper.py && \
    cp -r /app/* /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start nginx
CMD ["nginx", "-g", "daemon off;"]
