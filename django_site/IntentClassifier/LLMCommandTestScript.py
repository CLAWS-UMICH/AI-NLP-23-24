import requests
import json

TEST_ENDPOINT = "http://localhost:8000/IntentClassifier/webhook/" # Double check this

def send_post_request(message=""):
    request_obj = {
        'message': message,
        'sender': "sender"
    }
    return requests.post(TEST_ENDPOINT, json=request_obj)
def run_cases_from_file(filestr):
    readstr = ""
    with open(filestr, "r") as f:
        readstr = f.read().split("\n")
    for i in range(0, len(readstr), 3):
        voice_command = readstr[i]
        tags = readstr[i+1].split(", ")
        expected = json.loads(readstr[i+2])

        run_test_case({"voice_command": voice_command, "tags":tags}, expected)

def run_test_case(message, expected_response):
    response = send_post_request(message) 
    print("Running test case: {message}\n".format(message=message))

    json_str = (response.text.replace("\\\"", "'"))
    json_return = json.loads(json.loads(response.text))

    print (f"Expected Response: {expected_response}")
    print(f"Response: {json_return} \n")

    tags_correct = 0
    tags_total = len(expected_response.keys())
    extra_tags = 0

    for key, value in json_return.items():
        if key in expected_response:
            if value == expected_response[key]:
                tags_correct+=1
        else:
            extra_tags += 1

    print(f"Got {tags_correct} tags correct out of {tags_total}. Also gave {extra_tags} extraneous tags")
    return tags_correct, tags_total, extra_tags

if __name__ == '__main__':
    run_cases_from_file("testcasesGPT.txt")
    """run_test_case(
        {"voice_command": "create a geosample note which describes a red basaltic rock at location A", 
        "tags":["color, type, location"]}, 
        {'color':'red', 'type':'basaltic', 'location':'A'}
    )"""