# AI-NLP-23-24
how to run:
open three terminal shells
in the first shell go to the RASA folder and run "rasa run --enable-api"
in the second shell go to the django_site folder and run "python manage.py runserver"
in the third shell execute your curl command for testing. Ex: "curl -d "command=<voice_command>" -X POST http://localhost:8000/IntentClassifier/webhook/". Replace voice_command with the sentence the astronaut would say