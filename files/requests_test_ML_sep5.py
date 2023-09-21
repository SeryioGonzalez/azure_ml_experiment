import requests
import random
import string
import chardet


def detect_encoding(file_path):
    rawdata = open(file_path, "rb").read()
    result = chardet.detect(rawdata)
    return result['encoding']


def generate_prediction_id():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(10))


url = "https://qqqqqq.execute-api.us-east-1.amazonaws.com/dev/pred"
X_test_encoding = detect_encoding("./X_test.txt")
text_file = open("./X_test.txt", "r", encoding=X_test_encoding)
X_test = text_file.readlines()

num_requests = 1234
success_count = 0
failure_count = 0
valid_request = 0

for _ in range(num_requests):
    random_index = random.randint(0, len(X_test) - 1)
    random_payload = X_test[random_index].strip()

    prediction_id = generate_prediction_id()
    headers = {
        'pred-id': prediction_id,
        'Content-Type': 'text/csv'
    }

    response = requests.post(url, headers=headers, data=random_payload)
    response_dict = response.json()
    if response.status_code == 200:  # Assuming success response has status code 200
        success_count += 1
        if response_dict['pred-id'] == prediction_id:
            valid_request += 1
    else:
        failure_count += 1
    print(response_dict)
    print(f"Request ID: {prediction_id}, Status Code: {response.status_code}")

print(f"Total Requests: {num_requests}")
print(f"Successful Requests: {success_count}")
print(f"Failed Requests: {failure_count}")
print(f"Request Validated : {valid_request}")
