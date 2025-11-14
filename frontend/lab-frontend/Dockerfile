# ========================
# Vue Frontend Dev Server
# ========================
FROM node:20

# Set working directory inside the container
WORKDIR /app

# Copy package files first for caching
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy all frontend source
COPY . .

# Expose dev port
EXPOSE 5177

# Enable hot reload (polling)
ENV CHOKIDAR_USEPOLLING=true
ENV PORT=5177

# Start Vite dev server
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0", "--port", "5177"]
