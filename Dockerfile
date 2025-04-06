FROM python:3.9-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . ./app

# Expose the Flask app's port
EXPOSE 5000

# Run the Flask app
CMD flask run -h 0.0.0.0 -p 5000