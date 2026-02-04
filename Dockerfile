FROM python:3.12-slim

# Undgå .pyc + buffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Installer system-deps (requests kan køre uden, men rart at have certs)
RUN apt-get update \
    && apt-get install -y --no-install-recommends ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Installer python deps først (bedre cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kopiér app-koden
COPY . .

# State gemmes her
VOLUME ["/app"]

# Start app
CMD ["python", "app.py"]
