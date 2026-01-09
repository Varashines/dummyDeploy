# Use a Python base image
FROM python:3.9-slim-bookworm

# Copy uv from the official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set the working directory
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy project files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
# --frozen ensures we use the exact lockfile
# --no-install-project skips installing the project itself as a package for now
RUN uv sync --frozen --no-install-project --no-dev

# Copy the application code
COPY . .

# Expose port 8000 for FastAPI
EXPOSE 8000

# Run the app using uvicorn (inside the uv virtualenv)
# --no-project ensures uv doesn't try to install the 'flask-app' package in editable mode
CMD ["/bin/uv", "run", "--no-project", "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
