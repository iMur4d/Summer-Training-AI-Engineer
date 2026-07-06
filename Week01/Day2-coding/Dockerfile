FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY prompt_fundamentals.py .

CMD ["python", "prompt_fundamentals.py"]