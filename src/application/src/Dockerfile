# Use the official MongoDB image
FROM mongodb/mongodb-community-server:latest

# Install Python 3 and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Optionally, install any Python dependencies you may need
# RUN pip3 install some-python-library

# Set the working directory to the entrypoint init script directory
WORKDIR /docker-entrypoint-initdb.d

# Copy your Python script directly into the container
COPY ./src/your_python_script.py /docker-entrypoint-initdb.d/.py

# Set the command to run the Python script directly upon container startup
CMD ["python3", "/docker-entrypoint-initdb.d/.py"]
