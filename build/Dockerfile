FROM python:3.9

# Set the working directory
WORKDIR /app

# Copy all the files to the container
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port 1509 to access the Flask app
EXPOSE 1509

# Run the Flask app
CMD ["python", "predict.py"]
