from vocode.streaming.models.events import Event
from vocode.streaming.utils.events_manager import EventsManager
from loguru import logger
from prometheus_client import Counter, Gauge

# Create Prometheus metrics
SESSION_COUNTER = Counter('voicebot_session_count', 'Number of sessions started')
SESSION_GAUGE = Gauge('voicebot_active_sessions', 'Current number of active sessions')

class VoiceBotEventsManager(EventsManager):
    def handle_event(self, event: Event):
        logger.info(f"Received event: {event.type}")
        
        if event.type == "transcript":
            logger.info(f"Transcript: {event.data.get('text', '')}")
        elif event.type == "transcript_complete":
            logger.info(f"Transcript complete: {event.data.get('text', '')}")
        elif event.type == "phone_call_connected":
            logger.info(f"Phone call connected: {event.data}")
            SESSION_COUNTER.inc()
            SESSION_GAUGE.inc()
            logger.info(f"📞 Session started. Active sessions: {SESSION_GAUGE._value.get()}")
        elif event.type == "phone_call_ended":
            logger.info(f"Phone call ended: {event.data}")
            SESSION_GAUGE.dec()
            logger.info(f"📴 Session ended. Active sessions: {SESSION_GAUGE._value.get()}")
        elif event.type == "phone_call_did_not_connect":
            logger.error(f"Phone call did not connect: {event.data}")
        elif event.type == "recording":
            logger.info(f"Recording: {event.data}")
        elif event.type == "action":
            logger.info(f"Action: {event.data}")
        else:
            logger.warning(f"Unhandled event type: {event.type}")

        # Call the parent class's handle_event method
        super().handle_event(event)
