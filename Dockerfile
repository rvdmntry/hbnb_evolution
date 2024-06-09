# Start with an Alpine Linux base image with Python 3.8
FROM python:3.8-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    APP_PORT=8000

# Install dependencies
RUN apk update && apk add --no-cache gcc musl-dev libffi-dev

# Create and set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . /app/

# Expose the application port
EXPOSE $APP_PORT

# Define a volume for persistent storage
VOLUME ["/app/data"]

# Set the command to run the application with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:${APP_PORT}", "wsgi:app"]
