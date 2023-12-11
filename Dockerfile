# Use an official Python runtime as a parent image
FROM python:3.8-slim


COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN apt-get update && apt-get install -y libgomp1 && pip install -r requirements.txt 


WORKDIR /app

COPY . /app

EXPOSE 5000

# Run api.py when the container launches
CMD ["python", "./app/api.py"]

