from vocode.streaming.models.events import (
    Event, EventType, PhoneCallConnectedEvent, PhoneCallEndedEvent,
    PhoneCallDidNotConnectEvent, RecordingEvent, ActionEvent
)
from vocode.streaming.utils.events_manager import EventsManager
from loguru import logger
from prometheus_client import Counter, Gauge

# Create Prometheus metrics
SESSION_COUNTER = Counter('voicebot_session_count', 'Number of sessions started')
SESSION_GAUGE = Gauge('voicebot_active_sessions', 'Current number of active sessions')

class VoiceBotEventsManager(EventsManager):
    async def handle_event(self, event: Event):
        logger.info(f"Received event: {event.type}")
        
        if event.type == EventType.TRANSCRIPT:
            logger.info(f"Transcript: {event.text}")
        elif event.type == EventType.TRANSCRIPT_COMPLETE:
            logger.info(f"Transcript complete: {event.text}")
        elif event.type == EventType.PHONE_CALL_CONNECTED:
            phone_call_event = event  # type: PhoneCallConnectedEvent
            logger.info(f"Phone call connected: from {phone_call_event.from_phone_number} to {phone_call_event.to_phone_number}")
            SESSION_COUNTER.inc()
            SESSION_GAUGE.inc()
            logger.info(f"📞 Session started. Active sessions: {SESSION_GAUGE._value.get()}")
        elif event.type == EventType.PHONE_CALL_ENDED:
            phone_call_event = event  # type: PhoneCallEndedEvent
            logger.info(f"Phone call ended: Duration {phone_call_event.conversation_minutes} minutes")
            SESSION_GAUGE.dec()
            logger.info(f"📴 Session ended. Active sessions: {SESSION_GAUGE._value.get()}")
        elif event.type == EventType.PHONE_CALL_DID_NOT_CONNECT:
            phone_call_event = event  # type: PhoneCallDidNotConnectEvent
            logger.error(f"Phone call did not connect: Status {phone_call_event.telephony_status}")
        elif event.type == EventType.RECORDING:
            recording_event = event  # type: RecordingEvent
            logger.info(f"Recording: {recording_event.recording_url}")
        elif event.type == EventType.ACTION:
            action_event = event  # type: ActionEvent
            logger.info(f"Action: Input: {action_event.action_input}, Output: {action_event.action_output}")
        else:
            logger.warning(f"Unhandled event type: {event.type}")

        # Call the parent class's handle_event method
        await super().handle_event(event)
