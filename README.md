# 🤖 Voice Bot

Voice Bot Server is a custom version of Vocode Telephony Server with FastAPI, designed for creating intelligent voice agents for phone calls. This project enables you to build and deploy conversational AI agents that can handle inbound and outbound phone calls for various use cases such as information collection, appointment scheduling, sales, customer support, and more.

## 🌟 Overview

Voice Bot leverages the power of Vocode to support using AI agents with inbound and outbound phone calls. Users can create their own custom agents and integrate them seamlessly into their telephony systems.

## 📋 Requirements

- 🐳 [Docker](https://www.docker.com/) (required for running the project)

API keys for:
   - 🎙️ Deepgram (for speech transcription)
   - 🧠 OpenAI (for the underlying agent)
   - 🗣️ ElevenLabs (for speech synthesis)
   - 📞 Twilio (for telephony)- 

The project uses the following components, which are automatically set up through Docker:

- 🎬 [ffmpeg](https://ffmpeg.org/) (for audio processing)
- 🗄️ [Redis](https://redis.io/) (for data storage and caching)

These dependencies are defined in the `docker-compose.yml` file and will be pulled in automatically when you run the project.

For local testing and development:

- 🌐 [Ngrok](https://ngrok.com/) or [Cloudflare Tunnels](https://www.cloudflare.com/products/tunnel/) (optional, used to expose your local server to the internet for testing purposes)

Note: Ngrok or Cloudflare Tunnels are not required for deployment but can be useful for local testing and development.

## 🛠️ Environment Setup

1. Copy the `.env.template` file and fill in the values of your API keys:
   ```
   cp .env.template .env
   ```

2. Set up hosting so that Twilio can hit your server. An easy way to do this is ngrok or cloudflare:
   ```
   ngrok http 6000
   ```
   Copy the URI that is tunneling localhost:3000 to your `.env` without `https://`, e.g.:
   ```
   BASE_URI=asdf1234.ngrok.app
   ```

## 📞 Telephony Server

The TelephonyServer is responsible for receiving and making phone calls. The server is built using FastAPI and utilizes Twilio for telephony services.

### 🚀 Running the Server

Choose one of these two options to run the server:

#### Option 1: Run everything with Docker

1. Build the telephony app Docker image:
   ```
   docker build -t voice-bot-server .
   ```
2. Run the application using docker-compose:
   ```
   docker-compose up
   ```

#### Option 2: Run Python directly

1. Install Poetry and dependencies:
   ```
   poetry install
   ```
2. Run Redis (default port 6379):
   ```
   brew services start redis
   ```
   Or using Docker:
   ```
   docker run -dp 6379:6379 -it redis/redis-stack:latest
   ```
3. Run the server with uvicorn:
   ```
   poetry run uvicorn main:app --port 3000
   ```

## 📥 Setting up an Inbound Number

1. Create a Twilio account
2. In your Twilio dashboard, go to Phone Numbers -> Manage -> Buy a number to get a phone number
3. Go to Phone Numbers -> Manage -> Active Numbers and select the number you want to set up
4. Update the config to point the Webhook URL to `https://<BASE_URI>/inbound_call`
5. Hit Save and call the number!

## 📤 Executing Outbound Calls

1. Ensure the server is running
2. Install Poetry and dependencies:
   ```
   poetry 
3. Ensure .env has `TO_PHONE` set as the number you want to call and `FROM_PHONE` with your Twilio number.
4. Run the script:
   ```
   poetry run python outbound_call.py
   ```

## ⚙️ Configuration

Both the `OutboundCall` (in `outbound_call.py`) and `InboundCallConfig` (in `inbound.py`) classes can accept a `TranscriberConfig`, `AgentConfig`, or `SynthesizerConfig`. 

### 🎙️ Transcriber
The default transcriber is Deepgram

### 🗣️ Synthesizer
The default synthesizer is ElevenLabs

## 🚀 Deployment with Helm and Kubernetes

### Prerequisites

- Kubernetes cluster (e.g., Minikube, EKS, GKE, AKS)
- Helm 3.0+
- kubectl configured to communicate with your cluster

### Deployment Steps

1. Clone the repository and navigate to the project directory:
   ```
   git clone https://github.com/yourusername/voice-bot-server.git
   cd voice-bot-server
   ```

2. Create a `my-values.yaml` file in the project root with your specific configuration:
   ```yaml
   env:
     BASE_URI: "application-base-uri"
     DEEPGRAM_API_KEY: "your-deepgram-key"
     OPENAI_API_KEY: "your-openai-key"
     OPENAI_BASE_URL: "your-openai-based-base-url"
     ELEVEN_LABS_API_KEY: "your-eleven-labs-key"
     ELEVEN_LABS_VOICE_ID: "your-eleven-labs-voice-id"
     TWILIO_ACCOUNT_SID: "your-twilio-sid"
     TWILIO_AUTH_TOKEN: "your-twilio-token"
     FROM_PHONE: "your-from-phone"
     TO_PHONE: "your-to-phone"
   ```

3. Install the Helm chart:
   ```
   helm install voice-bot ./kubernetes/voice-bot-helm/voice-bot -f my-values.yaml
   ```

4. Check the status of your deployment:
   ```
   kubectl get pods
   kubectl get services
   ```

5. To access your application, set up port-forwarding:
   ```
   k8s-port-forward.bat
   (TODO does not work) kubectl port-forward service/voice-bot 6000:3000 (/TODO)
   ```
   Your application should now be accessible at `http://localhost:6000`.

### Updating the Deployment

To update your deployment after making changes:

```
helm upgrade voice-bot ./kubernetes/voice-bot-helm/voice-bot -f my-values.yaml
```

### Uninstalling the Deployment

To remove the Voice Bot Server from your cluster:

```
helm uninstall voice-bot
```

### Troubleshooting

- If you encounter issues, check the logs of your pods:
  ```
  kubectl logs deployment/voice-bot
  ```

- For more detailed information about your deployment:
  ```
  kubectl describe deployment voice-bot
  kubectl describe service voice-bot
  ```

Remember to update your Twilio webhook URL to point to your new Kubernetes-hosted Voice Bot Server.
