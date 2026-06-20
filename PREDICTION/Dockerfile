FROM python:3.11-slim

WORKDIR /app

# System deps some sklearn/pandas wheels still want at build time
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first (better layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# App code + models + db
COPY . .

EXPOSE 5000

# server.py exposes /traffic on 0.0.0.0:5000 (Flask dev server, debug=True kept as in source)
CMD ["python", "server.py"]
