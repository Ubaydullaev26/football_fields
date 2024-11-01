FROM python:3.9-slim-buster

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/
# Install any dependencies
RUN pip install -r requirements.txt

RUN apt-get update -y \
    && apt-get install -y netcat gdal-bin libgdal-dev python3-gdal binutils libproj-dev


# Copy the current directory contents into the container at /app
COPY . /app/

# Expose port 8000 for the Django app
EXPOSE 8000