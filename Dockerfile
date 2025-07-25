# Use a specific, stable version of Python as the base image
FROM --platform=linux/amd64 python:3.10-slim

# Update packages, apply security patches, and then clean up
RUN apt-get update \
    && apt-get upgrade -y \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install all the Python dependencies with a longer timeout
RUN pip install --no-cache-dir --timeout=100 -r requirements.txt

# Copy all your project files into the container
COPY . .

# This is the command that will run when the container starts
CMD ["python", "main.py"]