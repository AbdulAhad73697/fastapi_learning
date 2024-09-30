# Use an official Python runtime as a parent image
FROM python:3.12-slim

# Set the working directory in the container
WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Disable virtual environments in Poetry
RUN poetry config virtualenvs.create false

# Copy the dependency files first to leverage Docker layer caching
COPY pyproject.toml poetry.lock /app/

# Install dependencies directly into the container's global environment
RUN poetry install --only main

# Now copy the rest of the application code
COPY . /app

# Expose the port on which the FastAPI app will run
EXPOSE 8501

# Command to run the FastAPI application using Uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8501"]
