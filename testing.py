import requests

# Define ThingSpeak parameters
channel_id = '2473359'
read_api_key = 'KJYHGSGHE6NE2CG7'
num_entries = 100  # Number of entries to retrieve

# Make GET request to ThingSpeak API
url = f'https://api.thingspeak.com/channels/{channel_id}/feeds.json?api_key={read_api_key}&results={num_entries}'
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    # Parse JSON response
    data = response.json()
    # Extract relevant fields from response (e.g., sensor data)
    entries = data['feeds']
    for entry in entries:
        # Process and use the retrieved data as needed
        print("Acceleration (x,y,z):", entry['field1'], entry['field2'], entry['field3'])
        print("Average Acceleration:", entry['field4'])
        print("Gravitational Force (g):", entry['field5'])
        print("\n")
else:
    print('Failed to retrieve data from ThingSpeak')
