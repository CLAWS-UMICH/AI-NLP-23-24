# AI-NLP-23-24
how to run:
open three terminal shells
in the first shell go to the RASA folder and run "rasa run --enable-api"
in the second shell go to the django_site folder and run "python manage.py runserver"
in the third shell execute your curl command for testing. Ex: "curl -d "command=<voice_command>" -X POST http://localhost:8000/IntentClassifier/webhook/". Replace voice_command with the sentence the astronaut would say

5/19/2024:
How to run full AI backend:
1. enter virtualenv
2. start lm studio server on 1234 port
3. start rasa server on 5005 port (rasa run --enable-api -m models/[model_name])
4. start server (python manage.py runserver)
5. use test scripts to verify each endpoint
