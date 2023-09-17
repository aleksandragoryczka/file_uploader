# Use an official Python runtime as a parent image
FROM python:3.10

# Set environment variables for Django
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE file_uploader.settings

# Create and set the working directory
RUN mkdir /code
WORKDIR /code

# Copy the Pipfile and Pipfile.lock into the container and install dependencies
COPY requirements.txt /code/

# Install dependencies
RUN pip install -r requirements.txt

# Copy the rest of the application code into the container
COPY . /code/

# Expose the port your Django app will run on
EXPOSE 8000

# Start the Django application
CMD ["pipenv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
