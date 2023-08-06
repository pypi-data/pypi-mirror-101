# Pull base image
FROM python:3.9

EXPOSE 8000

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /code

COPY requirements.txt /code/
RUN python -m pip install -r requirements.txt

# Copy project
COPY . /code/