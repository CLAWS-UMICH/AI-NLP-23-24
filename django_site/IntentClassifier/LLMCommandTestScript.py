import requests

TEST_ENDPOINT = "https://localhost:8000/IntentClassifier/webhook" # Double check this

def send_post_request(message=""):
    request_obj = {
        'message': message,
        'sender': "sender"
    }
    return requests.post(TEST_ENDPOINT, json=request_obj)

def run_test_case(message, expected_response, expected_data):
    response = send_post_request(message)
    print(response)
    return expected_response == response.text

if __name__ == '__main__':

    run_test_case(
        "create a geosample note which describes a red basaltic rock at location A", 
        "[geosample]", 
        {'color':'red', 'type':'basalt', 'location':'a'}
    )