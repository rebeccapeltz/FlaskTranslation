from flask import Flask, render_template, request
import requests

# Importing the required libraries
import os
import uuid
import json
from dotenv import load_dotenv
from requests import HTTPError

load_dotenv()

languages = {"en":"English","fr":"French","de":"German","it":"Italian","ja":"Japanese","ru":"Russian","es":"Spanish"}

app = Flask(__name__)

def index_get():
    return render_template('index.html')

def index_post():
	# Read the values from the form
	text_to_translate = request.form['text']
	if 'language' not in request.form:
		print('Error: language not found')
	print('before target language')
	target_language_code = request.form.get('language')
	print('target language',target_language_code)

	# Load the values from .env
	key = os.environ.get("TRANSLATOR_KEY")
	endpoint = os.environ.get("TEXT_TRANSLATION_ENDPOINT")
	region = os.environ.get('LOCATION')

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
		print(json_response)
		translated_text = json_response[0]['translations'][0]['text']
		print(f"Translated text: {translated_text}")

		detected_language = json_response[0].detectedLanguage.language
		print('after detected language')
		print(f'detected_language: {detected_language}')
		detected_language_score = json_response[0].detectedLanguage.score
		print(f'detected_language_score {detected_language_score}')


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

@app.route("/", methods=["GET","POST"])
def index():
	if request.method == 'POST':
		# Read the values from the form
		text_to_translate = request.form['text']
		print(text_to_translate)
		target_language_code = request.form['language']
		print(target_language_code)

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

			print(json_response)

			translated_text = json_response[0]['translations'][0]['text']
			print(f"Translated text: {translated_text}")

			detected_language_code = json_response[0]['detectedLanguage']['language']
			detected_language_score = json_response[0]['detectedLanguage']['score']
			print(detected_language_code, detected_language_score)

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


if __name__ == '__main__':
    app.run(debug=True)
