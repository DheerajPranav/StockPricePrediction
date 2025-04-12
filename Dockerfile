# Use a Python 3.9 base image
FROM python:3.9

# Set the working directory in the container
WORKDIR /app

# Copy all files from the current directory to the container's working directory
COPY . /app

# Install the dependencies from the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the Flask API will use (5000)
EXPOSE 5000

# Set the command to run the Flask app and the prediction pipeline when the container starts
CMD ["python", "main.py"]