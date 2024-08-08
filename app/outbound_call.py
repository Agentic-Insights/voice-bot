import os
import asyncio

from dotenv import load_dotenv

# Vocode Configs
from vocode.streaming.models.agent import ChatGPTAgentConfig
from vocode.streaming.models.message import BaseMessage
from vocode.streaming.models.telephony import TwilioConfig
from vocode.streaming.telephony.config_manager.redis_config_manager import RedisConfigManager
from vocode.streaming.telephony.conversation.outbound_call import OutboundCall

# ElevenLabsSynthesizerConfig
from vocode.streaming.synthesizer.eleven_labs_synthesizer import ElevenLabsSynthesizerConfig
from vocode.streaming.synthesizer.eleven_labs_synthesizer import AudioEncoding

load_dotenv()

BASE_URI = os.environ["BASE_URI"]

async def main():
    config_manager = RedisConfigManager()

    outbound_call = OutboundCall(
        BASE_URI=BASE_URI,
        to_phone=os.environ["TO_PHONE"],
        from_phone=os.environ["FROM_PHONE"],
        config_manager=config_manager,
        agent_config=ChatGPTAgentConfig(
            initial_message=BaseMessage(text="What up"),
            prompt_preamble="Have a pleasant conversation about life",
            generate_responses=True,
        ),
        telephony_config=TwilioConfig(
            account_sid=os.environ["TWILIO_ACCOUNT_SID"],
            auth_token=os.environ["TWILIO_AUTH_TOKEN"],
        ),
        synthesizer_config=ElevenLabsSynthesizerConfig(
            api_key=os.environ["ELEVEN_LABS_API_KEY"],
            voice_id=os.environ["ELEVEN_LABS_VOICE_ID"],
            sampling_rate=8000,
            audio_encoding=AudioEncoding.MULAW,
        ),
)

    input("Press enter to start call...")
    await outbound_call.start()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except RuntimeError as e:
        if str(e) == "Event loop is closed":
            print("Ignoring 'Event loop is closed' error. The call was likely successful.")
        else:
            raise
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise
