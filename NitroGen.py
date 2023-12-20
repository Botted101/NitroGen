import requests
import json
import uuid
import threading
import math
from datetime import datetime

def load_config():
    """Load configuration settings from a file."""
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)
    return config

def send_discord_request(output_file):
    """Send a Discord API request with a generated partnerUserId."""
    url = 'https://api.discord.gx.games/v1/direct-fulfillment'
    headers = {
        'authority': 'api.discord.gx.games',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.opera.com',
        'referer': 'https://www.opera.com/',
        'sec-ch-ua': '"Opera";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': 'Windows',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0'
    }

    # Generate a new partnerUserId
    partner_user_id = str(uuid.uuid4())

    # Create the data payload with the generated partnerUserId
    data = {
        'partnerUserId': partner_user_id
    }

    # Convert data to JSON format
    json_data = json.dumps(data)

    # Perform the POST request
    response = requests.post(url, headers=headers, data=json_data)

    # Extract the token from the response
    token = json.loads(response.text).get('token', '')

    # Write the output to the file
    output_line = f'https://discord.com/billing/partner-promotions/1180231712274387115/{token}/\n'
    with open(output_file, 'a') as file:
        file.write(output_line)

    # Print the response
    print(f"Status Code: {response.status_code}")
    print(f"Output Line: {output_line}")

def main():
    # Load configuration from config.json
    config = load_config()

    # Number of threads
    num_threads = config.get('num_threads', 2)

    # Number of requests per thread
    num_requests_per_thread = config.get('num_requests_per_thread', 5)

    # Total number of requests to generate
    amount_to_generate = config.get('amount_to_generate', 20)

    # Calculate the number of threads needed
    num_threads = min(num_threads, amount_to_generate)

    # Calculate the number of requests per thread
    requests_per_thread = math.ceil(amount_to_generate / num_threads)

    # Create a timestamp for the output file
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")

    # Create the output filename with timestamp
    output_file = f'output_{timestamp}.txt'

    # Create a lock for thread safety
    lock = threading.Lock()

    # Function to be executed by each thread
    def threaded_function():
        for _ in range(requests_per_thread):
            # Check if the total number of requests has been reached
            with lock:
                nonlocal amount_to_generate
                if amount_to_generate <= 0:
                    return
                amount_to_generate -= 1

            # Send the request and get the response
            send_discord_request(output_file)

    # Create and start threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=threaded_function)
        threads.append(thread)
        thread.start()

    # Wait for all threads to finish
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()