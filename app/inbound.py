# Standard library imports
import os
import logging
from dotenv import load_dotenv

# Third-party imports
from fastapi import FastAPI
from loguru import logger

# Prometheus
from prometheus_client import start_http_server, Counter, Gauge
import time

# Prometheus
from prometheus_client import start_http_server, Counter, Gauge
import time


# Local application/library specific imports
# from app.speller_agent import SpellerAgentFactory, SpellerAgentConfig
from .prompt_handler import get_system_prompt

from vocode.logging import configure_pretty_logging
from vocode.streaming.models.agent import ChatGPTAgentConfig
# from vocode.streaming.models.agent import AnthropicAgentConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.models.telephony import TwilioConfig
from vocode.streaming.telephony.config_manager.redis_config_manager import RedisConfigManager
from vocode.streaming.telephony.server.base import TelephonyServer, TwilioInboundCallConfig, EventsManager
from vocode.streaming.models.events import Event, EventType

from vocode.streaming.synthesizer.eleven_labs_synthesizer import ElevenLabsSynthesizerConfig
from vocode.streaming.synthesizer.eleven_labs_synthesizer import AudioEncoding

from vocode.streaming.action.dtmf import TwilioDTMF

# if running from python, this will load the local .env
# docker-compose will load the .env file by itself
load_dotenv()
configure_pretty_logging()

logger.info("🤖 Voice Bot Server starting...")

# Create Prometheus metrics
SESSION_COUNTER = Counter('voicebot_session_count', 'Number of sessions started')
SESSION_GAUGE = Gauge('voicebot_active_sessions', 'Current number of active sessions')

def start_new_session(session_id):
    # Increment session counter
    SESSION_COUNTER.inc()
    SESSION_GAUGE.inc()
    logger.info(f"Session {session_id} started")

def end_session(session_id):
    # Decrement active sessions gauge
    SESSION_GAUGE.dec()
    logger.info(f"Session {session_id} ended")

# Start Prometheus HTTP server
start_http_server(8000)
logger.info("Prometheus metrics server started on port 8000")

app = FastAPI(docs_url=None)

REDIS_HOST = os.getenv("REDIS_HOST", "voice-bot-redis")
config_manager = RedisConfigManager()

BASE_URI = os.getenv("BASE_URI")

if not BASE_URI:
    raise ValueError("BASE_URI must be set in environment")

# Get the system prompt
system_prompt = get_system_prompt()

# anthropic_config=AnthropicAgentConfig(
#     api_key=os.environ["ANTHROPIC_API_KEY"],
#     model=os.environ["LLM_MODEL"],
#     prompt_preamble=system_prompt,
#     generate_responses=True,
# )

class SessionTrackingEventsManager(EventsManager):
    def __init__(self, subscriptions: List[EventType] = []):
        super().__init__(subscriptions)
        self.subscriptions.update({EventType.SESSION_START, EventType.SESSION_END})

    async def handle_event(self, event: Event):
        if event.type == EventType.SESSION_START:
            start_new_session(event.session_id)
        elif event.type == EventType.SESSION_END:
            end_session(event.session_id)

telephony_server = TelephonyServer(
    base_url=BASE_URI,
    config_manager=config_manager,
    inbound_call_configs=[
        TwilioInboundCallConfig(
            url="/inbound_call",
            event_manager=SessionTrackingEventsManager(),
            agent_config=ChatGPTAgentConfig(
                initial_message=BaseMessage(text="Hello there, what's your name?"),
                prompt_preamble=system_prompt,
                generate_responses=True,
                num_check_human_present_times=1,
                goodbye_phrases=["bye", "goodbye", "good bye", "goodbye!", "Please stay on the line", "this call lasted"],
                end_conversation_on_goodbye=True,
                send_filler_audio=True,
                allowed_idle_time_seconds=30,
                interrupt_sensitivity="high",
            ),
            
            # uncomment this to use the speller agent instead
            # agent_config=SpellerAgentConfig(
            #     initial_message=BaseMessage(
            #         text="im a speller agent, say something to me and ill spell it out for you"
            #     ),
            #     generate_responses=False,
            # ),
            twilio_config=TwilioConfig(
                account_sid=os.environ["TWILIO_ACCOUNT_SID"],
                auth_token=os.environ["TWILIO_AUTH_TOKEN"],          
            ),
            synthesizer_config=ElevenLabsSynthesizerConfig(
                api_key=os.environ["ELEVEN_LABS_API_KEY"],
                voice_id=os.environ["ELEVEN_LABS_VOICE_ID"],
                sampling_rate=8000,
                audio_encoding=AudioEncoding.MULAW,
                experimental_streaming=True,
                experimental_websocket=True
            ),
        )
    ],
)

app.include_router(telephony_server.get_router())
