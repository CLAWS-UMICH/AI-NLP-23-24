import requests

TEST_ENDPOINT = "https://localhost:8000/IntentClassifier/webhook" # Double check this

def send_post_request(message=""):
    request_obj = {
        'message': message,
        'sender': "sender"
    }
    return requests.post(TEST_ENDPOINT, json=request_obj)

def run_test_case(message, expected_response):
    response = send_post_request(message)
    print(response)
    return expected_response == respones.text

if __name__ == '__main__':
    run_test_case("TEST", "TEST")