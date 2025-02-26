

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