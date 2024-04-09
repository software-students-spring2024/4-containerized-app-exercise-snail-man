# Use the official Python image as a base image
FROM python:3

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app.py \
    FLASK_RUN_HOST=localhost \
    FLASK_RUN_PORT=5000

# Set the working directory in the container
WORKDIR /web-app

# Copy the requirements file into the container
COPY requirements.txt .

# Install virtualenv and create a virtual environment
RUN pip install virtualenv && \
    virtualenv venv

# Activate the virtual environment
SHELL ["/bin/bash", "-c"]
RUN source venv/bin/activate && \
    pip install -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose port 5000
EXPOSE 5000

# Run the Flask application within the virtual environment
CMD ["venv/bin/python", "app.py"]
