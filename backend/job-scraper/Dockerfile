FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including Playwright dependencies
RUN apt-get update && apt-get install -y \
    curl \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libdbus-1-3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libgio-2.0-0 \
    libexpat1 \
    libdrm2 \
    libxcb1 \
    libxkbcommon0 \
    libx11-6 \
    libxcomposite1 \
    libxdamage1 \
    libxext6 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    libatspi2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Explicitly install PostgreSQL driver (backup)
RUN pip install --no-cache-dir psycopg2-binary==2.9.9

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Health check
HEALTHCHECK --interval=30s --timeout=10s --retries=3 --start-period=40s \
  CMD curl -f http://localhost:8001/health || exit 1

# Expose port
EXPOSE 8001

# Production command (no reload, multiple workers for better performance)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001", "--workers", "2"]