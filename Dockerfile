FROM python:3.12-slim

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_SYSTEM_PYTHON=1 \
    PATH="/root/.local/bin:${PATH}"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Copy dependency file
COPY pyproject.toml ./

# Install Python dependencies with uv
RUN /root/.local/bin/uv pip install --system \
    crewai>=1.3.0 \
    crewai-tools>=1.3.0 \
    streamlit>=1.51.0 \
    pandas>=2.3.3 \
    pyyaml>=6.0.3 \
    python-dotenv>=1.2.1 \
    plotly>=6.3.1 \
    openpyxl>=3.1.5

# Copy application code
COPY . .

# Create outputs directory
RUN mkdir -p outputs

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]