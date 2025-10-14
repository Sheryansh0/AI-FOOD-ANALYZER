# Use Node.js 20 alpine image
FROM node:20-alpine

# Set working directory
WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy frontend code
COPY . .

# Build the application
RUN npm run build

# Expose port 3000
EXPOSE 3000

# Install serve to run the built app
RUN npm install -g serve

# Serve the built application
CMD ["serve", "-s", "dist", "-l", "3000"]
