# Dockerfile

# Use the official Python image
FROM python:3.12.2-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt /app/

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Copy the .env file
COPY .env-docker /app/.env

# Expose the port the app runs on
EXPOSE 8000

# Command to run the application
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
