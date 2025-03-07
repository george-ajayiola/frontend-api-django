# Builder stage
FROM python:3.13.0-alpine AS builder

# Install system dependencies
RUN apk update && \
    apk add --no-cache musl-dev libpq-dev gcc

RUN python -m venv /opt/venv

# Activate the virtual environment
ENV PATH="/opt/venv/bin:$PATH"

# Set the working directory
WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Operational stage
FROM python:3.13.0-alpine

# Install runtime dependencies
RUN apk update && apk add --no-cache libpq-dev

# Copy the virtual environment from the builder stage
COPY --from=builder /opt/venv /opt/venv

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PATH="/opt/venv/bin:$PATH"


WORKDIR /app


COPY . .

EXPOSE 8000


RUN pip install gunicorn

COPY start.sh /start.sh
RUN chmod +x /start.sh

# Run the startup script
CMD ["/start.sh"]