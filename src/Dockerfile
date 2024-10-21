# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the Poetry installer script and install Poetry
RUN apt-get update && apt-get install -y curl && \
    curl -sSL https://install.python-poetry.org | python3 -

# Export Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy only the pyproject.toml and poetry.lock to leverage Docker cache
COPY pyproject.toml ./
COPY poetry.lock ./

# Install dependencies
RUN poetry install --no-root

# Copy the current directory contents into the container at /app
COPY . .

# Copy PromptMage db
COPY .promptmage /app/.promptmage

# Copy the .env file into the container
COPY .env .env

# Expose port 8000 to the outside world
EXPOSE 8000

# Run the application
CMD ["poetry", "run", "promptmage", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]
