import requests

TEST_ENDPOINT = "http://localhost:8000/IntentClassifier/webhook/" # Double check this

def send_post_request(message=""):
    request_obj = {
        'message': message,
        'sender': "sender"
    }
    return requests.post(TEST_ENDPOINT, json=request_obj)

def run_test_case(message, expected_response, expected_data):
    response = send_post_request(message)
    print("Running test case: {message}".format(message=message))
    print(response.text)
    if expected_response == response.text:
        # TODO: Test case response matches json response text
        print("CORRECT")
    else:
        # TODO: Test case response doesn't matche expected value
        print(expected_response == response.text)
        print("WRONG")        
    return expected_response == response.text

if __name__ == '__main__':

    run_test_case(
        "create a geosample note which describes a red basaltic rock at location A", 
        "[geosample]", 
        {'color':'red', 'type':'basalt', 'location':'a'}
    )