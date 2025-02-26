

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