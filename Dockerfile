# Use slim Python base; PySpark will pull Java dependencies as needed
FROM python:3.11-slim

# Install Java for Spark
RUN apt-get update && apt-get install -y --no-install-recommends openjdk-17-jre-headless \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:${PATH}"

# Create working directory
WORKDIR /app

# Copy Python app files
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY app/main.py /app/main.py

# Create output dir (will also work with bind mounts)
RUN mkdir -p /app/output

# Default command
CMD ["python", "/app/main.py"]
