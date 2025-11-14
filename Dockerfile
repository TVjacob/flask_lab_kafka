# ===============================
# Base image for Python + Node
# ===============================
FROM python:3.11-slim

# Install Node 20 (official Debian repo)
RUN apt-get update && apt-get install -y curl gnupg \
    && curl -fsSL https://deb.nodesource.com/setup_20.x | bash - \
    && apt-get install -y nodejs supervisor \
    && apt-get clean

WORKDIR /app

# ------------------------------
# Install Python dependencies
# ------------------------------
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ------------------------------
# Install Vue frontend deps
# ------------------------------
COPY frontend/lab-frontend/package*.json ./frontend/lab-frontend/

# Remove lock file before install to avoid arch mismatch
RUN rm -f frontend/lab-frontend/package-lock.json \
    && cd frontend/lab-frontend \
    && npm install

# ------------------------------
# Copy backend + frontend source
# ------------------------------
COPY . .

# ------------------------------
# Supervisord config (runs both processes)
# ------------------------------
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 5080
EXPOSE 5177

CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
