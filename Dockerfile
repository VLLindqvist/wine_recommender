# Stage 1: Build React frontend
FROM node:24-alpine AS frontend-build

WORKDIR /app
RUN corepack enable && corepack prepare pnpm@latest --activate
COPY app/package.json app/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile
COPY app/ ./
ENV DISABLE_ESLINT_PLUGIN=true
RUN pnpm run build

# Stage 2: Combined runtime
FROM python:3.8-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends nginx supervisor && \
    rm -rf /var/lib/apt/lists/*

# Install Python dependencies
WORKDIR /api
COPY api/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -c "import nltk; nltk.download('stopwords')"
COPY api/ .

# Copy React build to nginx
COPY --from=frontend-build /app/build /var/www/html

# Nginx config
COPY nginx.cloud-run.conf /etc/nginx/sites-available/default

# Supervisord config
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

EXPOSE 8080

CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
