# Use an Alpine Linux base image with Python 3.8
FROM python:3.8-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV APP_HOME=/app
ENV PORT=8000

# Create application directory
WORKDIR $APP_HOME

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a volume for persistent data storage
VOLUME ["/app/data"]

# Expose the port
EXPOSE $PORT

# Run the application with Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:$PORT", "app:app"]
