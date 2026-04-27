FROM python:3.9-slim

# Install system dependencies + compilers needed for llama-cpp
RUN apt-get update && apt-get install -y \
    git \
    nmap \
    gcc \
    g++ \
    make \
    cmake \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Define the token argument for private clones
ARG HF_TOKEN

# Clone private repositories
RUN git clone https://Cunt1257:${HF_TOKEN}@github.com/yourmomsucks357-blip/fah-qu1257.git /app/src/fah_qu
RUN git clone https://Cunt1257:${HF_TOKEN}@github.com/yourmomsucks357-blip/gangster.git /app/models/gangster

# Copy local files
COPY . .

# Install python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment paths
ENV PYTHONPATH="${PYTHONPATH}:/app/src:/app/src/fah_qu"

# Expose the mandatory Hugging Face port
EXPOSE 7860

# Launch the app
CMD ["python", "web/app.py"]
