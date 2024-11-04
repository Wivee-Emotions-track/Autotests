FROM python:3.11-slim

# Set environment variable to disable Python output buffering
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    curl \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libgtk-3-0 \
    libasound2 \
    libpangocairo-1.0-0 \
    libxshmfence1 \
    libxrandr-dev \
    libxkbcommon0 \
    libx11-xcb1\
    tk \
    python3-tk \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -fsSL https://github.com/allure-framework/allurectl/releases/latest/download/allurectl_linux_amd64  \
    -o /usr/local/bin/allurectl \
    && chmod +x /usr/local/bin/allurectl

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml ./

# Install Poetry without venv
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$WORK_ENV" == production && echo "--no-dev") --no-interaction --no-ansi --no-cache

RUN playwright install

COPY . .

# Give execution permission to the Bash script
RUN chmod +x pytest_run.sh

# Command to execute the script
CMD ["bash", "pytest_run.sh"]
