# Frontend Dockerfile
FROM node:18

# Set the working directory
WORKDIR /app

# Install dependencies
COPY package.json package-lock.json ./
RUN npm install

# Copy the app code
COPY . .

# Build the app
RUN npm run build

# Serve the app using a lightweight web server
RUN npm install -g serve
CMD ["serve", "-s", "dist", "-l", "3000"]

# Expose the application port
EXPOSE 3000