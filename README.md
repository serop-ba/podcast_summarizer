# Podcast Summary Generator

## Overview

This repository contains a FastAPI server and a Streamlit frontend that work together to generate summaries from podcast recordings using the Ollama server. With a simple setup using Docker Compose, you can quickly deploy both services and start generating insightful summaries from your podcast content.

## Features

- **FastAPI Server:** Handles requests to generate summaries from podcast recordings.
- **Streamlit Frontend:** Provides an intuitive user interface for interacting with the API and viewing summaries.
- **Ollama Integration:** Utilizes the Ollama server to process and generate summaries from podcast audio.

## Prerequisites

- [Docker](https://www.docker.com/get-started) (for containerization)
- [Docker Compose](https://docs.docker.com/compose/install/) (for managing multi-container Docker applications)

## Setup

1. **Clone the Repository**

2. **Start the Services:**

Simply run the following command to start both the FastAPI server and the Streamlit frontend:

```
docker-compose up
```

**3. Access the Streamlit Frontend:**

Open your browser and navigate to http://localhost:8501 to start using the frontend. You can upload podcast recordings and get summaries generated by the backend API.

-----
## Usage
**Upload a Podcast Recording**: Use the Streamlit interface to upload your podcast recording.

**Generate a Summary**: The frontend sends the audio to the FastAPI server, which then communicates with the Ollama server to generate a summary.

**View the Summary**: The generated summary will be displayed in the Streamlit frontend.

----

## Repository structure

```
├── LICENSE
├── README.md
├── api # fast api
│   ├── Dockerfile
│   ├── helper.py
│   ├── main.py
│   └── requirements.txt
├── docker-compose.yaml
├── external_service # ollama service
│   └── Dockerfile
├── frontend # frontend
│   ├── Dockerfile
│   ├── app.py
│   └── requirements.txt
└── main.py # run the script manually 
```