# ==========================================
# Stage 1: Build Frontend (Node.js)
# ==========================================
FROM node:20-alpine as frontend-builder

WORKDIR /app/client
COPY client/package*.json ./
RUN npm install
COPY client/ ./
# Build to /app/client/dist
RUN npm run build

# ==========================================
# Stage 2: Build Backend (Python) & Serve
# ==========================================
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies (ffmpeg is required for MoviePy)
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Copy Backend requirements and install
COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy Backend Code
COPY server/ .

# Copy Built Frontend from Stage 1 to where FastAPI expects it
# We configured main.py to look in app/static_ui
COPY --from=frontend-builder /app/client/dist /app/app/static_ui

# Create storage directory for persistence
RUN mkdir -p /app/storage

# Environment Variables
ENV PORT=8000
ENV HOST=0.0.0.0

# Expose port
EXPOSE 8000

# Run Command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
