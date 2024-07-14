# 🤖 Voice Bot Server

Voice Bot Server is a custom version of Vocode, designed for creating intelligent voice agents for phone calls. This project enables you to build and deploy conversational AI agents that can handle inbound and outbound phone calls for various use cases such as information collection, appointment scheduling, sales, customer support, and more.

## 🌟 Overview

Voice Bot Server leverages the power of Vocode to support using AI agents with inbound and outbound phone calls. Users can create their own custom agents and integrate them seamlessly into their telephony systems.

## 📋 Requirements

- 🐳 [Docker](https://www.docker.com/) (required for running the project)

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
   You'll need to get API keys for:
   - 🎙️ Deepgram (for speech transcription)
   - 🧠 OpenAI (for the underlying agent)
   - 🗣️ ElevenLabs (for speech synthesis)
   - 📞 Twilio (for telephony)

2. Set up hosting so that Twilio can hit your server. An easy way to do this is ngrok or cloudflare:
   ```
   ngrok http 6000
   ```
   Copy the URL that is tunneling localhost:3000 to your `.env` without `https://`, e.g.:
   ```
   BASE_URL=asdf1234.ngrok.app
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
4. Update the config to point the Webhook URL to `https://<YOUR BASE URL>/inbound_call`
5. Hit Save and call the number!

## 📤 Executing Outbound Calls

1. Ensure the server is running
2. In `outbound_call.py`, replace `to_phone` with the number you want to call and `from_phone` with your Twilio number
3. Run the script:
   ```
   poetry run python outbound_call.py
   ```

## ⚙️ Configuration

Both the `OutboundCall` (in `outbound_call.py`) and `InboundCallConfig` (in `main.py`) classes can accept a `TranscriberConfig`, `AgentConfig`, or `SynthesizerConfig`. 

### 🎙️ Transcriber
The default transcriber is Deepgram

### 🗣️ Synthesizer
The default synthesizer is ElevenLabs
