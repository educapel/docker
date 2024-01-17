# Use a slim variant of Python 3.8
FROM python:3.8

# Set the working directory
WORKDIR /fastapi-app

# Copy only the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the CSV file and the entire app directory
COPY UCI_Credit_Card.csv .
COPY ./app ./app

# Create a non-root user and switch to it
RUN useradd -m myuser
USER myuser


# Command to run on container start
CMD ["python", "./app/main.py"]
