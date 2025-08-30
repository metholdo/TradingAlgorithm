
FROM python:3.11-slim

# Install uv
RUN pip install --no-cache-dir uv==0.4.20

WORKDIR /app
COPY pyproject.toml README.md .
COPY trader ./trader
COPY config ./config
COPY scripts ./scripts
COPY tests ./tests
COPY .pre-commit-config.yaml .
COPY Makefile .

RUN uv sync --frozen --no-dev

ENV PYTHONUNBUFFERED=1
CMD ["uv", "run", "trader", "--help"]
