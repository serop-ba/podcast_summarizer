# Podcast Summary Generator

## Overview

This repository contains a FastAPI server and a Streamlit frontend that work together to generate summaries from podcast recordings using the Ollama server. With a simple setup using Docker Compose, you can quickly deploy both services and start generating insightful summaries from your podcast content.

## Features

- **FastAPI Server:** Handles requests to generate summaries from podcast recordings.
- **Streamlit Frontend:** Provides an intuitive user interface for interacting with the API and viewing summaries.
- **Ollama Integration:** Utilizes the Ollama server to process and generate summaries from podcast audio.

----
## Project Setup
The project is deployed on Kubernetes.

This guide provides instructions for installing Istio and `istiod` in a Kubernetes cluster using Helm and `kubectl apply -f`. Please ensure you have the necessary tools installed and configured before proceeding.

### Prerequisites
- infrastructure installed (see below)
- Kubernetes cluster (version 1.14 or later)
- `kubectl` installed and configured to access your cluster
- Helm installed (version 3.x recommended)
- Sufficient permissions to create resources in the Kubernetes cluster

## Increasing Resource Limits

Due to resource size limitations in this setup, it is essential to **increase the resource limits** for LLM components. Ensure your Kubernetes cluster has enough CPU,GPU and memory allocated to accommodate these resources.

***I was using the free tier on GCP so no GPU support was there.***


# Infrastructure Setup

This guide provides instructions for setting up the infrastructure using Terragrunt. Please ensure you have the necessary tools installed and configured before proceeding.

## Prerequisites

- Terragrunt installed (version 0.35.x recommended)
- Google Cloud SDK installed and configured with sufficient permissions to create resources
- Access to the project where the infrastructure will be deployed

## Terragrunt Setup

1. Clone the repository:
```
git clone ...
```
2. Navigate to each infra folder and initialize:

For each folder where you have Terragrunt configurations, run the following commands:
Example for the cluster
```
cd infra/dev/cluster
terragrunt init --upgrade
terragrunt plan
```

3. Apply the configuration for each folder:

After planning, you can apply the configuration by running:
```
terragrunt apply
```
Review the output and confirm the changes.

Now that we have the infrastructure ready let's install the needed resources on our Kubernetes Cluster.

## Install Istio Using Helm

1. **Add the Istio repository:**
```
   helm repo add istio https://istio-release.storage.googleapis.com/charts
   helm repo update
```

2. **Install Istio base components:**
```
   kubectl create namespace istio-system
   helm install istio-base istio/base -n istio-system
```
3. **Install `istiod`:**
```
   helm install istiod istio/istiod -n istio-system --set global.hub=docker.io/istio --set global.tag=1.16.1
```
   Note: Make sure to adjust the `global.hub` and `global.tag` to the desired version if necessary.

4. **Verify the installation:**

   Check that all components are running:
```
   kubectl get pods -n istio-system
```
## Setup Ingress Gateway

1. **Install the Ingress Gateway:**
```
 helm install istio-ingressgateway istio/gateway \           
  --namespace istio-system \
  --set service.type=LoadBalancer
```
or you can install it from kubernetes file

2. **Verify the Ingress Gateway:**

   Check that the Ingress Gateway is running:
```
   kubectl -n istio-system get svc istio-ingressgateway
```
## Deploy Your Application
1. **Deploy Images to artifact registry***
You can run this script after adjusting it to your GCP project. You can run (on mac)
```
./build_images.sh
```
or run the commands in your terminal. 

2. **Apply the resources from the folder:**

   Make sure you have your application YAML files ready. You can apply them using:
```
   kubectl apply -f ./kubernetes
```

---

## HTTPs Support

The current setup is configured to support only HTTP traffic. If you require HTTPS support, please ensure to add TLS termination by modifying the Gateway configuration to include TLS settings.



# Testing 
## Accessing the Application

Once your Istio Gateway and Virtual Service are properly configured, you can access your application using the external IP address of the Istio Ingress Gateway.

1. **Get the External IP of the Istio Ingress Gateway:**

   Run the following command to retrieve the external IP address:
```
   kubectl get svc -n istio-system istio-ingressgateway
```
   Look for the `EXTERNAL-IP` in the output. This is the IP address you will use to access your application.

2. **Access the Application:**

   Open a web browser or use a tool like `curl` to access your application at the external IP:

   For HTTP:
   ```
   curl http://<EXTERNAL-IP>
    ```
   For example, if your external IP is `34.76.243.175`, you would access it with:

   curl http://34.76.243.175

   Ensure that the port number used matches the one specified in your Gateway configuration (default is usually 80 for HTTP).

3. **Troubleshooting:**

   - If you cannot access the application, verify that your Gateway and Virtual Service are correctly configured.
   - Check the status of your application pods and ensure they are running and healthy.
   - Make sure any firewall rules allow traffic on the necessary ports.
