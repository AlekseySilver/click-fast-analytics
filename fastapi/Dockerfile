# Base image
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY ./req.txt /app/req.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/req.txt

# Copy application code
COPY ./app /app

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]