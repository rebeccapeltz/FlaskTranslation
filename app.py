from flask import Flask, render_template, request, jsonify, send_file
import traceback
import requests
import time
import azure.cognitiveservices.speech as speechsdk
import io
import struct
import os

from dotenv import load_dotenv
load_dotenv()

# Get the environment variables
key = os.environ.get("TRANSLATOR_KEY")
endpoint = os.environ.get("TEXT_TRANSLATION_ENDPOINT")
region = os.environ.get('LOCATION')
speechKey = os.environ.get('SPEECH_KEY')

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

languages = {"ar": "Arabic", "zh": "Chinese", \
             "en": "English", "fr": "French", "de": "German","el":"Greek", \
             "he": "Hebrew", "it": "Italian", "ja": "Japanese", "ru": "Russian", \
             "es": "Spanish", "uk": "Ukrainian", "zu": "Zulu", "hi": "Hindi"}



@app.context_processor
def inject_now():
    """
    This function injects the current time into the template context.
    This is useful for reloading JavaScript libraries referenced in templates.
    Look at script tags in the templates for this: v=now()
    """
    return {'now': lambda: str(int(time.time()))}

@app.route("/about", methods=["GET"])
def about():
    """
    Render the about template.
    """
    return render_template('about.html')

@app.route("/", methods=["GET", "POST"])
def index():
    """
    If POST call the Azure Translator Text API to translate the text.
    If GET render the index template.
    The form on the index page will call this function with a POST request.
    The function will read the values from the form and call the Azure Translator Text API to translate the text.
    The response from the API will be returned to the results template.
    The results template will display the translated text and other information.
    Args:
        request (object): The request object.
    Returns:
        object: The response object.
    """
    if request.method == 'POST':
        # Read the values from the form
        text_to_translate = request.form['text']
        target_language_code = request.form['language']

        # Set up the header information
        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Ocp-Apim-Subscription-Region': region,
            'Content-type': 'application/json'
        }

        # Create the body of the request with the text to be translated
        body = [{'text': text_to_translate}]

        # Make the call using post
        response = requests.post(endpoint, headers=headers, json=body, params={"to": target_language_code})

        # Check the response
        if response.status_code == 200:
            json_response = response.json()
            translated_text = json_response[0]['translations'][0]['text']
            detected_language_code = json_response[0]['detectedLanguage']['language']
            detected_language_score = json_response[0]['detectedLanguage']['score']

            return render_template(
                'results.html',
                translated_text=translated_text,
                text_to_translate=text_to_translate,
                target_language_code=target_language_code,
                detected_language_code=detected_language_code,
                target_language=languages[target_language_code],
                detected_language=languages[detected_language_code],
                detected_language_score=detected_language_score
            )
        else:
            print(f"Error Code: {response.status_code}")
            print(f"Message: {response.text}")
    else:
        return render_template('index.html')


def pcm_to_wav(audio_data, num_channels, sample_rate, bits_per_sample):
    """
    Converts PCM audio data to WAV format.
    Args:
        audio_data (io.BytesIO): The PCM audio data.
        num_channels (int): The number of audio channels.
        sample_rate (int): The sample rate of the audio.
        bits_per_sample (int): The number of bits per sample.
    Returns:
        io.BytesIO: A BytesIO object containing the WAV formatted audio.
    """
    byte_rate = sample_rate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8

    # convert bytesIO to bytes and get data_size
    audio_data.seek(0)
    pcm_data = audio_data.read()
    data_size = len(pcm_data)
    file_size = 36 + data_size

    # Build RIFF/WAVE header
    header = struct.pack(
        '<4sI4s4sIHHIIHH4sI',
        b'RIFF',              # Chunk ID
        file_size,            # Chunk size
        b'WAVE',              # Format
        b'fmt ',              # Subchunk1 ID
        16,                   # Subchunk1 size (PCM)
        1,                    # Audio format (1 = PCM)
        num_channels,         # Number of channels
        sample_rate,          # Sample rate
        byte_rate,            # Byte rate
        block_align,          # Block align
        bits_per_sample,      # Bits per sample
        b'data',              # Subchunk2 ID
        data_size             # Subchunk2 size
    )

    # Combine header and PCM data
    combined = header + pcm_data
    return io.BytesIO(combined)


def generate_speech(text, language, voice_name):  
    """
    Generates speech audio from the given text using specified language and voice.

    Args:
        text (str): The text to be converted to speech.
        language (str): The language code for speech synthesis (e.g., 'en-US').
        voice_name (str): The name of the voice to be used for speech synthesis.

    Returns:
        io.BytesIO: A BytesIO object containing the synthesized speech audio in WAV format.

    Raises:
        Exception: If speech synthesis fails for any reason.
    """
    try:  
        speech_config = speechsdk.SpeechConfig(subscription=speechKey, region=region)  
        speech_config.speech_synthesis_language = language  
        speech_config.speech_synthesis_voice_name = voice_name  
        speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Riff24Khz16BitMonoPcm)  

        audio_output_callback = InMemoryStream()  
        audio_output_stream = speechsdk.audio.PushAudioOutputStream(audio_output_callback) 
        audio_config = speechsdk.audio.AudioOutputConfig(stream=audio_output_stream)  

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)  
        result = synthesizer.speak_text_async(text).get()  

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:  
            print("Speech synthesized successfully.")  
            audio_data = audio_output_callback.close() 
            audio_data.seek(0)  
            audio_data_with_header = pcm_to_wav(audio_data, num_channels=1, sample_rate=24000, bits_per_sample=16)
            audio_data_with_header.seek(0)
            return audio_data_with_header
        else:  
            raise Exception("Speech synthesis failed.")  
    except Exception as e:  
        print(f"Error in generate_speech: {e}")  
        raise e

class InMemoryStream(speechsdk.audio.PushAudioOutputStreamCallback):  
    """
    A class that handles in-memory audio stream callbacks for speech synthesis.
    This class inherits from PushAudioOutputStreamCallback and is used to capture
    synthesized speech audio data in memory.
    """
    def __init__(self):
        """
        Initializes the InMemoryStream instance.
        This constructor sets up an in-memory stream to capture audio data.
        """  
        super().__init__()  
        self._audio_data = io.BytesIO()  

    def write(self, buffer: memoryview) -> int: 
        """
        Writes audio data to the in-memory stream.
        This method is called by the speech synthesis engine to provide audio data.
        Args:
            buffer (memoryview): A memory view of the audio data to be written.
        Returns:
            int: The number of bytes written to the stream.
        """ 
        self._audio_data.write(buffer)  
        return len(buffer)  

    def close(self):
        """
        Closes the in-memory audio stream.
        This method is called to finalize the audio stream and return the captured data.
        Returns:
            io.BytesIO: A BytesIO object containing the captured audio data.
        """

        self._audio_data.seek(0)  
        return self._audio_data 


@app.route("/synthesize", methods=["GET"])
def synthesize():
    """
    Synthesizes speech from the input text using Azure Cognitive Services.
    This endpoint receives a GET request with parameters for text, voice, and language,
    and returns the synthesized speech audio in WAV format.
    Args:
        text (str): The input text to be synthesized.
        voice (str): The name of the voice to be used for synthesis.
        language (str): The language code for the synthesis (e.g., 'en-US').
    Returns:
        Response: A Flask response object containing the synthesized speech audio in WAV format.
    Raises:
        Exception: If there is an error during speech synthesis.
    """
    text_to_speak = request.args.get('input_text')
    voice = request.args.get('voice')
    language = request.args.get('language')
    if not text_to_speak:
        return jsonify({"error": "Missing 'text' parameter"}), 400
       
    try:
        audio_stream = generate_speech(text_to_speak,language, voice)
        return send_file(audio_stream, as_attachment=True, mimetype="audio/wav", download_name="output.wav")
    except Exception as e:
        print(f"Error in synthesize endpoint: {e}")
        traceback.print_exc()
        return str(e), 500
    
if __name__ == '__main__':
    app.run(debug=True)
