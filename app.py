from flask import Flask, render_template, request
import requests

# Importing the required libraries
import os
import uuid
import json
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)


def index_get():
    return render_template('index.html')

def index_post():
	# Read the values from the form
	original_text = request.form['text']
	target_language = request.form['language']

	# Load the values from .env
	key = os.getenv("TRANSLATOR_KEY")
	endpoint = os.getenv("TEXT_TRANSLATION_ENDPOINT")
	location = os.getenv('LOCATION')

	# Indicate that we want to translate and the API
	# version (3.0) and the target language
	path = '/translate?api-version=3.0'

	# Add the target language parameter
	target_language_parameter = '&to=' + target_language

	# Create the full URL
	constructed_url = endpoint + path + target_language_parameter

	# Set up the header information, which includes our
	# subscription key
	headers = {
		'Ocp-Apim-Subscription-Key': key,
		'Ocp-Apim-Subscription-Region': location,
		'Content-type': 'application/json',
		'X-ClientTraceId': str(uuid.uuid4())
	}

	# Create the body of the request with the text to be
	# translated
	body = [{'Text': original_text}]

	# Make the call using post
	translator_request = request.post(
		constructed_url, headers=headers, json=body)

	# Retrieve the JSON response
	translator_response = translator_request.json()

	# Retrieve the translation
	translated_text = translator_response[0]['translations'][0]['text']

	# Call render template, passing the translated text,
	# original text, and target language to the template
	return render_template(
		'results.html',
		translated_text=translated_text,
		original_text=original_text,
		target_language=target_language
	)

@app.route("/", methods=["GET","POST"])
def handle_request():
	if request.method == 'POST':
		# Read the values from the form
		original_text = request.form['text']
		target_language = request.form['language']

		# Load the values from .env
		key = os.getenv("TRANSLATOR_KEY")
		endpoint = os.getenv("TEXT_TRANSLATION_ENDPOINT")
		location = os.getenv('LOCATION')

		# Indicate that we want to translate and the API
		# version (3.0) and the target language
		path = 'translate?api-version=3.0'

		# Add the target language parameter
		target_language_parameter = '&from=en&to=' + target_language

		# Create the full URL
		constructed_url = endpoint + path + target_language_parameter
		print('constructed_url',constructed_url)

		# Set up the header information, which includes our
		# subscription key
		headers = {
			'Ocp-Apim-Subscription-Key': key,
			'Ocp-Apim-Subscription-Region': location,
			'Content-type': 'application/json',
			'X-ClientTraceId': str(uuid.uuid4())
		}

		print('headers',headers)

		# Create the body of the request with the text to be
		# translated
		body = [{'text': original_text}]
		print('body', body)

		# Make the call using post
		translator_request = requests.post(
			constructed_url, headers=headers, json=body)

		# Retrieve the JSON response
		translator_response = translator_request.json()
		print(translator_response)

		# Retrieve the translation
		translated_text = translator_response[0]['translations'][0]['text']

		# Call render template, passing the translated text,
		# original text, and target language to the template
		return render_template(
			'results.html',
			translated_text=translated_text,
			original_text=original_text,
			target_language=target_language
		)
	else:
		return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
