from flask import Flask, render_template, request, jsonify, Response
import traceback
import requests
import time
import azure.cognitiveservices.speech as speechsdk
import base64
from io import BytesIO

# Importing the required libraries
import os
from dotenv import load_dotenv
from requests import HTTPError

load_dotenv()
# Load the values from .env
key = os.environ.get("TRANSLATOR_KEY")
endpoint = os.environ.get("TEXT_TRANSLATION_ENDPOINT")
region = os.environ.get('LOCATION')
speechKey = os.environ.get('SPEECH_KEY')

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

languages = {"ar": "Arab", "zh": "Chinese", \
             "en": "English", "fr": "French", "de": "German", \
             "he": "Hebrew", "it": "Italian", "ja": "Japanese", "ru": "Russian", \
             "es": "Spanish", "uk": "Ukraine", "zu": "Zulu", "hi": "Hindi"}


@app.context_processor
def inject_now():
    return {'now': lambda: str(int(time.time()))}


def index_get():
    return render_template('index.html')


def index_post():
    # Read the values from the form
    text_to_translate = request.form['text']
    if 'language' not in request.form:
        print('Error: language not found')
    target_language_code = request.form.get('language')

    # Construct the request headers and body
    headers = {
        "Ocp-Apim-Subscription-Key": key,
        "Content-Type": "application/json",
        "Ocp-Apim-Subscription-Region": region  # Replace with your region, e.g., "westus"
    }

    body = [{
        "text": text_to_translate
    }]

    try:
        # Make the request
        response = requests.post(endpoint, headers=headers, json=body, params={"to": target_language_code})
        json_response = response.json()
        translated_text = json_response[0]['translations'][0]['text']
        # print(f"Translated text: {translated_text}")
        # print(f"Detected language: ", json_response[0])
        detected_language = json_response[0].detectedLanguage.language
        # print('after detected language')
        # print(f'detected_language: {detected_language}')
        detected_language_score = json_response[0].detectedLanguage.score
        # print(f'detected_language_score {detected_language_score}')

        # Call render template, passing the translated text,
        # original text, and target language to the template
        return render_template(
            'results.html',
            translated_text=translated_text,
            text_to_translate=text_to_translate,
            target_language_code=target_language_code,
            detected_language=detected_language,
            detected_language_score=detected_language_score
        )
    except HTTPError as exception:
        if exception.error is not None:
            print(f"Error Code: {exception.error.code}")
            print(f"Message: {exception.error.message}")


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == 'POST':
        # Read the values from the form
        text_to_translate = request.form['text']
        # print(text_to_translate)
        target_language_code = request.form['language']
        # print(target_language_code)

        # Load the values from .env
        key = os.getenv("TRANSLATOR_KEY")
        endpoint = os.getenv("TEXT_TRANSLATION_ENDPOINT")
        location = os.getenv('LOCATION')

        # Set up the header information
        headers = {
            'Ocp-Apim-Subscription-Key': key,
            'Ocp-Apim-Subscription-Region': location,
            'Content-type': 'application/json'
        }

        # Create the body of the request with the text to be
        # translated
        body = [{'text': text_to_translate}]
        # print('body', body)

        # Make the call using post
        response = requests.post(endpoint, headers=headers, json=body, params={"to": target_language_code})

        # Check the response
        if response.status_code == 200:
            json_response = response.json()

            # print(json_response)

            translated_text = json_response[0]['translations'][0]['text']
            # print(f"Translated text: {translated_text}")

            detected_language_code = json_response[0]['detectedLanguage']['language']
            detected_language_score = json_response[0]['detectedLanguage']['score']
            # print("detected", detected_language_code, detected_language_score)

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


import os
import azure.cognitiveservices.speech as speechsdk
from io import BytesIO

def generate_speech_from_text(text,voice):
    speech_config = speechsdk.SpeechConfig(
        subscription=speechKey,
        region=region
    )
    speech_config.speech_synthesis_voice_name = voice # "en-US-JennyNeural"
    speech_config.set_speech_synthesis_output_format(
        speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3
    )
    
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
    result = synthesizer.speak_text_async(text).get()
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return BytesIO(result.audio_data)
    else:
        raise Exception(f"Speech synthesis failed: {result.error_details}")

@app.route("/synthesize", methods=["GET"])
def synthesize():
    # print("in textToSpeech")
    text_works = request.args.get('text')
    voice = request.args.get('voice')
    if text_works:
        try:
            audio_stream = generate_speech_from_text(text_works,voice)
            return Response(audio_stream.getvalue(), mimetype="audio/wav")
        except Exception as err:
            print(err)
            return "Error in text-to-speech synthesis", 500
    else:
        return "Text not provided", 404
       
@app.route('/start_recognition', methods=['GET'])
def start_recognition():
    # print("start recognition")
    language_code = request.args.get("language_code")
    # print("language code:", language_code)
    speech_config = speechsdk.SpeechConfig(subscription=speechKey, region=region)
    source_language_config = speechsdk.languageconfig.SourceLanguageConfig(language_code)
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config,source_language_config=source_language_config,audio_config=audio_config)
    speech_recognition_result = speech_recognizer.recognize_once_async().get()
    # print("speech result", speech_recognition_result)
    # print("result text", speech_recognition_result.text)

    if speech_recognition_result.reason == speechsdk.ResultReason.RecognizedSpeech:
        # print("RecognizedSpeech")
        return jsonify({'text': speech_recognition_result.text})
    elif speech_recognition_result.reason == speechsdk.ResultReason.NoMatch:
        # print("No Match")
        return jsonify({'text': 'No speech could be recognized'})
    else:
        # print("Cancelled")
        return jsonify({'text': 'Speech recognition canceled'})


if __name__ == '__main__':
    app.run(debug=True)
