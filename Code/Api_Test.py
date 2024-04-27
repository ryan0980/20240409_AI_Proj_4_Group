import requests
from callApi import GET, POST  # Ensure your actual file name is used here if it's not 'api_calls'

def main():
    # Instantiate the GET class and make a 'getRuns' API call
    get_instance = GET()
    get_instance.getRuns('1399', 10)  # Replace '1399' and '10' with your specific parameters
    response = requests.request("GET", url=get_instance.url, headers=get_instance.headers)
    print("getRuns Response:", response.text)

    # Instantiate the POST class and make an 'enterWorld' API call
    post_instance = POST()
    post_instance.enterWorld('1', '1399')  # Replace '1' and '1399' with your specific parameters
    response = requests.request("POST", url=post_instance.url, headers=post_instance.headers, data=post_instance.payload)
    print("enterWorld Payload:", post_instance.payload)
    print("enterWorld Response:", response.text)

    # Make a 'makeMove' API call
    post_instance.makeMove('1399', 'S', '0')  # Replace '1399', 'N', and '0' with your specific parameters
    response = requests.request("POST", url=post_instance.url, headers=post_instance.headers, data=post_instance.payload)
    print("makeMove Payload:", post_instance.payload)
    print("makeMove Response:", response.text)

if __name__ == "__main__":
    main()
