# Use the base image from Ollama
FROM ollama/ollama

# Expose the port for the Ollama server
EXPOSE 11434

# Preload models (add each model you want to preload here)
RUN ollama pull llama3.2 \
    && ollama pull llama3.2:1b \
# Entrypoint to start the Ollama server
ENTRYPOINT ["ollama", "serve", "--port", "11434"]
