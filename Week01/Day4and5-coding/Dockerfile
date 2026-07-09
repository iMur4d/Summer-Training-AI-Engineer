FROM python:3.11-slim

# Install system packages required by WeasyPrint and fonts for text rendering
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libpangocairo-1.0-0 \
    libcairo2 \
    libffi-dev \
    shared-mime-info \
    fonts-noto-core \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the pipeline logic, the Streamlit UI, and the external system prompt
COPY pipeline.py .
COPY app.py .
COPY system_prompt.txt .

# Streamlit's default port
EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]