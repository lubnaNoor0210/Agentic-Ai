# Use the official Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy all files
COPY . .

# Install pip and uv (for your virtual env needs)
RUN pip install --upgrade pip && pip install uv

# Install Python dependencies
RUN uv pip install -r requirements.txt

# Expose the port Chainlit will run on
EXPOSE 7860

# Run Chainlit
CMD ["chainlit", "run", "main.py", "-h", "0.0.0.0", "--port", "7860"]
