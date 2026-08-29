# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set PYTHONPATH so backend modules can be imported directly
ENV PYTHONPATH=/app/backend:/app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ src/
COPY backend/ backend/
COPY tests/ tests/

# Expose port
ENV PORT=8000
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request, os; port = os.getenv('PORT', '8000'); urllib.request.urlopen(f'http://localhost:{port}/health')" || exit 1

# Run the application
CMD exec uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
