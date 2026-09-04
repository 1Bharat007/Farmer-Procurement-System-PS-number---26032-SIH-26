FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    curl \
    netcat-openbsd \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend project
COPY . /app/

# Expose Django / Daphne port
EXPOSE 8000

# Default entrypoint runs daphne ASGI for Django Channels & HTTP
CMD ["daphne", "-b", "0.0.0.0", "-p", "8000", "core.asgi:application"]
