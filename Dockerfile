# Use an official nginx image as a base
FROM nginx:alpine
# Copy the contents of the current directory to the nginx html folder
COPY . /usr/share/nginx/html
