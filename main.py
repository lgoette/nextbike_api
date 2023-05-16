# This is a testscript for booking a nextbike by entering its number

import requests

# Step 1: Get API Key
response = requests.get('https://webview.nextbike.net/getAPIKey.json')
api_key = response.json()['apiKey']

# Set the base URL
base_url = 'https://api.nextbike.net/api/v1.1'
print(api_key)

# Step 2: Prompt for login details
mobile = input("Enter your phone number (Example: 4915750123456): ")
pin = input("Enter your PIN: ")

# Step 2: Send login request
login_url = f"{base_url}/login.json"
login_data = {
    'apikey': api_key,
    'mobile': mobile,
    'pin': pin,
    'show_errors': 1
}

login_response = requests.post(login_url, data=login_data)
print(login_response.text)
login_data = login_response.json()

if 'user' in login_data:
    mobile = login_data['user']['mobile']
    login_key = login_data['user']['loginkey']
    print(f"Logged in successfully! Mobile: {mobile}, Login Key: {login_key}")
else:
    print("Login failed!")

# Step 3: Prompt for bike number
bike_number = input("Enter the bike number: ")

# Step 3: Get place_id using bike number
bike_state_url = f"{base_url}/getBikeState.json"
bike_state_data = {
    'apikey': api_key,
    'loginkey': login_key,
    'bike': bike_number,
    'show_errors': 1
}
bike_state_response = requests.get(bike_state_url, params=bike_state_data)
bike_state_data = bike_state_response.json()

if 'bike' in bike_state_data:
    place_id = bike_state_data['bike']['place_id']
    print(f"Place ID for bike {bike_number}: {place_id}")
else:
    print("Failed to get place ID for the bike.")

# Step 3: Book a bike
booking_url = f"{base_url}/booking.json"
booking_data = {
    'apikey': api_key,
    'loginkey': login_key,
    'place': place_id,
    'num_bikes': 1,
    'show_errors': 1
}

booking_response = requests.post(booking_url, data=booking_data)
booking_data = booking_response.json()

if 'booking' in booking_data:
    booking_id = booking_data['booking']['id']
    print(f"Bike {bike_number} booked successfully! Booking ID: {booking_id}")
else:
    print("Booking failed!")