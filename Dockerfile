# Start with an appropriate Alpine Linux base image with Python 3.8
FROM python:3.8-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    APP_PORT=8000 \
    VIRTUAL_ENV=/opt/venv

# Create a directory for the virtual environment
RUN python -m venv $VIRTUAL_ENV

# Update PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install dependencies
RUN apk update && apk add --no-cache gcc musl-dev libffi-dev

# Set the working directory
WORKDIR /app

# Copy the application requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application source code
COPY . .

# Expose the application port
EXPOSE $APP_PORT

# Define a volume for persistent storage
VOLUME ["/app/data"]

# Set the command to run the application with Gunicorn
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:${APP_PORT}", "wsgi:app"]
