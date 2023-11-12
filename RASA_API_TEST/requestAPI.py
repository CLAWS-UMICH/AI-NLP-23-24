# Test client for interacting with Rasa bot

import requests

sender = input("What is your name?\n")

bot_message = ""
while bot_message != "Bye":
    message = input("What's your message?\n")

    print("Sending message now...")

    r = requests.post('http://localhost:5005/webhooks/rest/webhook/', json={"sender": sender, "message": message})
    for i in r.json():
        bot_message = i['text']
        print(f"{i['text']}")