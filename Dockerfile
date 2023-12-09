# Use the official Python image as the base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the application files into the working directory
COPY . /app

# Install the application dependencies
RUN pip3 install -r requirements.txt

# Expose the port
# This line exposes port 8080 which is the port used by the application
EXPOSE 8080

# Define the entry point for the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8080"]

#ổn



