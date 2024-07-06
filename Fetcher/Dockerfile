# Use the official Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create and set the working directory
WORKDIR /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    postgresql-client

# Copy requirements file
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Install additional dependencies for testing
RUN pip install pytest pytest-flask sqlalchemy-utils

# Run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]

# Add a test stage to run pytest
FROM python:3.9-slim as test

WORKDIR /app

COPY --from=0 /app /app

RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    postgresql-client

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install pytest pytest-flask sqlalchemy-utils

# Run pytest
CMD ["pytest"]
