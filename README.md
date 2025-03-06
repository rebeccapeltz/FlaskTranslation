

## For Testing
```commandline
export FLASK_ENV=development
flask run
```

## Microsoft Python SDK
brew update && brew install azure-cli


https://learn.microsoft.com/en-us/python/api/overview/azure/ai-translation-text-readme?view=azure-python

## Get Key
az cognitiveservices account keys list --resource-group <your-resource-group-name> --name <your-resource-name>

az cognitiveservices account keys list --resource-group TranslatorAI --name bplangtrans

deploy: az webapp up --runtime PYTHON:3.13 --sku F1 --logs

## Deployment
    az webapp up --name <app-name> --resource-group <resource-group-name> --deployment-container-image-name <container-image-name>  --sku B1 --runtime <runtime-stack> --location <location> 

resource group: flask_translator_app
name: lask-translator-app

## set up speech service
https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-text-to-speech?tabs=macos%2Cterminal&pivots=programming-language-python

https://learn.microsoft.com/en-us/azure/ai-services/speech-service/get-started-speech-to-text?tabs=macos%2Cterminal&pivots=ai-studio

resource group: 
text to speech supported languages
https://learn.microsoft.com/en-us/azure/ai-services/speech-service/language-support?tabs=tts
I'm running the text to speech service and trying to get it speak an short text string using this voice: it-IT-ElsaNeural.  I'm getting this error:  Codec decoding is not started within 2s. 