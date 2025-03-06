# Example of setting the voice name for different languages
import os
import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
load_dotenv()

speech_config = speechsdk.SpeechConfig(subscription=os.environ.get('SPEECH_KEY'), region=os.environ.get('SPEECH_REGION'))


# speech_config.speech_synthesis_voice_name='en-US-AvaMultilingualNeural'
speech_config.speech_synthesis_voice_name = "it-IT-ElsaNeural"

synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

# Text to speech synthesis
text = "Ciao, come stai?"  # Example text in Italian
# text = "How are you?"
# text = "Bonjour comment allez-vous?"
result = synthesizer.speak_text_async(text).get()

if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized successfully.")
elif result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print(f"Speech synthesis canceled: {cancellation_details.reason}")

if result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = result.cancellation_details
    print(f"Speech synthesis canceled: {cancellation_details.reason}")
    print(f"Error details: {cancellation_details.error_details}")


