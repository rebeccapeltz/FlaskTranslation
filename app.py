from flask import Flask, render_template, request
import requests

# Importing the required libraries
import os
import uuid
import json
from dotenv import load_dotenv
from requests import HTTPError

load_dotenv()

app = Flask(__name__)

def index_get():
    return render_template('index.html')

def index_post():
	# Read the values from the form
	text_to_translate = request.form['text']
	target_language = request.form['language']

	# Load the values from .env
	key = os.getenv("TRANSLATOR_KEY")
	endpoint = os.getenv("TEXT_TRANSLATION_ENDPOINT")
	region = os.getenv('LOCATION')


	# key = "DnZJORsUuBJHHwh9V6KJBZStw85uxc7RZ47F2AC1SkT2SKVgiP4QJQQJ99BBAC8vTInXJ3w3AAAbACOGskZg"
	# endpoint = "https://api.cognitive.microsofttranslator.com/translate?api-version=3.0"

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
		response = requests.post(endpoint, headers=headers, json=body, params={"to": target_language})
		translations = response.json()
		translated_text = translations[0]['translations'][0]['text']
		print(f"Translated text: {translated_text}")

		# Call render template, passing the translated text,
		# original text, and target language to the template
		return render_template(
		'results.html',
			translated_text=translated_text,
			text_to_translate=text_to_translate,
			target_language=target_language
		)
	except HTTPError as exception:
		if exception.error is not None:
			print(f"Error Code: {exception.error.code}")
			print(f"Message: {exception.error.message}")

	# Indicate that we want to translate and the API
	# version (3.0) and the target language
	# path = '/translate?api-version=3.0'
	#
	# Add the target language parameter
	# target_language_parameter = '&to=' + target_language

	# Create the full URL
	# constructed_url = endpoint + path + target_language_parameter

	# Set up the header information, which includes our
	# subscription key
	# headers = {
	# 	'Ocp-Apim-Subscription-Key': key,
	# 	'Ocp-Apim-Subscription-Region': location,
	# 	'Content-type': 'application/json',
	# 	'X-ClientTraceId': str(uuid.uuid4())
	# }

	# Create the body of the request with the text to be
	# translated
	# body = [{'Text': original_text}]

	# Make the call using post
	# translator_request = request.post(
	# 	constructed_url, headers=headers, json=body)

	# Retrieve the JSON response
	# translator_response = translator_request.json()

	# Retrieve the translation
	# translated_text = translator_response[0]['translations'][0]['text']

	# Call render template, passing the translated text,
	# original text, and target language to the template
	# return render_template(
	# 	'results.html',
	# 	translated_text=translated_text,
	# 	original_text=original_text,
	# 	target_language=target_language
	# )

@app.route("/", methods=["GET","POST"])
def index():
	if request.method == 'POST':
		# Read the values from the form
		text_to_translate = request.form['text']
		print(text_to_translate)
		target_language = request.form['language']
		print(target_language)

		# Load the values from .env
		key = os.getenv("TRANSLATOR_KEY")
		# print(key)
		endpoint = os.getenv("TEXT_TRANSLATION_ENDPOINT")
		print(endpoint)
		location = os.getenv('LOCATION')
		print(location)

		# Indicate that we want to translate and the API
		# version (3.0) and the target language
		# path = 'translate?api-version=3.0'

		# Add the target language parameter
		#target_language_parameter \
		#	= '&from=en&to=' + target_language

		# Create the full URL
		# constructed_url = endpoint + path + target_language_parameter
		# print('constructed_url',constructed_url)

		# Set up the header information, which includes our
		# subscription key
		headers = {
			'Ocp-Apim-Subscription-Key': key,
			'Ocp-Apim-Subscription-Region': location,
			'Content-type': 'application/json'
		}

		# print('headers',headers)

		# Create the body of the request with the text to be
		# translated
		body = [{'text': text_to_translate}]
		# print('body', body)

		# Make the call using post
		response = requests.post(endpoint, headers=headers, json=body, params={"to": target_language})

		# response = requests.post(endpoint, headers=headers, \
		# 			 json=body, params={"to": target_language})

		# Check the response
		if response.status_code == 200:
			translations = response.json()
			print(translations)
			translated_text = translations[0]['translations'][0]['text']
			print(f"Translated text: {translated_text}")
			return render_template(
				'results.html',
				translated_text=translated_text,
				text_to_translate=text_to_translate,
				target_language=target_language
			)
		else:
			print(f"Error Code: {response.status_code}")
			print(f"Message: {response.text}")
	else:
		return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
