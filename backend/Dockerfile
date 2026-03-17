FROM python:3.13-slim

# 1. Install uv directly
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# 2. Install system dependencies (needed for the DB driver)
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 3. Use uv to install dependencies
# This layer is cached unless pyproject.toml or uv.lock changes
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    uv sync --frozen --no-install-project --no-dev

# 4. Copy the source code
COPY . .

# 5. Final sync to install the app itself
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --frozen --no-dev

# 6. Set the path to use the uv virtual environment
ENV PATH="/app/.venv/bin:$PATH"

EXPOSE 8000

# 7. Use uvicorn to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
