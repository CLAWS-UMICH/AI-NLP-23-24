import requests
def send_post_request(message=""):
    request_obj = {
        'message': message,
        'sender': "sender"
    }
    return requests.post('http://localhost:8000/IntentClassifier/webhook/', json=request_obj)


bot_message = ""

message = input("What's your message?\n")

print("Sending message now...")

r = send_post_request({"command":message, "tags":"color"})
print(r.text)