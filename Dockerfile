# ─── Base image ───────────────────────────────────────────────────────────────
FROM python:3.12-slim

# ─── System dependencies required by Playwright / Chromium ───────────────────
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    gnupg \
    libglib2.0-0 \
    libnss3 \
    libnspr4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libdbus-1-3 \
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

# ─── Working directory ────────────────────────────────────────────────────────
WORKDIR /app

# ─── Install Python dependencies ─────────────────────────────────────────────
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─── Install Playwright Chromium only (keeps image lean) ─────────────────────
RUN playwright install chromium
RUN playwright install-deps chromium

# ─── Copy project source (respects .dockerignore) ────────────────────────────
COPY . .

# ─── Ensure report directories exist ─────────────────────────────────────────
RUN mkdir -p reports/html/assets reports/screenshots runners/reports

# ─── Headless must be true inside Docker — override the environments.json value
ENV ENV=QA
ENV HEADLESS=true

# ─── Run tests ────────────────────────────────────────────────────────────────
CMD ["python", "-m", "pytest", "tests/", \
     "--html=reports/html/report.html", \
     "--self-contained-html", \
     "-v"]
