import requests
import json
import uuid

def send_discord_request():
    """
    Send a Discord API request with a generated partnerUserId.

    :return: Response object.
    """
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

    return response, token

# Number of requests to make
num_requests = 5  # Change this to the desired number of requests

# Open the output file in write mode
with open('output.txt', 'w') as output_file:
    for _ in range(num_requests):
        # Send the request and get the response and token
        response, token = send_discord_request()

        # Write the output to the file
        output_line = f'https://discord.com/billing/partner-promotions/1180231712274387115/{token}/\n'
        output_file.write(output_line)

        # Print the response
        print(f"Status Code: {response.status_code}")
        print(f"Output Line: {output_line}")
