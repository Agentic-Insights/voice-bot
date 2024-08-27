from prometheus_client import Counter, Gauge

# Create Prometheus metrics
SESSION_COUNTER = Counter('voicebot_session_count', 'Number of sessions started')
SESSION_GAUGE = Gauge('voicebot_active_sessions', 'Current number of active sessions')