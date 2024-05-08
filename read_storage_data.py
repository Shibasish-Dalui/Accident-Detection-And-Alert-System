import requests
import json
import time

# ThingSpeak channel details
CHANNEL_ID = '2473359'
READ_API_KEY = 'KJYHGSGHE6NE2CG7'

# URL for the ThingSpeak read API
url = f'https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json'

# Parameters for the read API request
params = {'api_key': READ_API_KEY}

# File to store data
file_path = 'thingspeak_data.json'


def write_to_file(data):
    with open(file_path, 'a') as file:
        json.dump(data, file)
        file.write('\n')


while True:
    try:
        # Sending GET request to ThingSpeak
        response = requests.get(url, params=params)

        # Checking if request was successful
        if response.status_code == 200:
            data = response.json()
            # Extracting feeds from response
            feeds = data['feeds']
            # Writing each entry to the file
            for entry in feeds:
                write_to_file(entry)
        else:
            print("Error:", response.status_code)
    except Exception as e:
        print("An error occurred:", str(e))

    # Wait for some time before fetching data again
    time.sleep(60)  # Fetch data every minute
