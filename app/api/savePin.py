import requests

def savePin(latitude, longitude, user_token):
    url = 'http://localhost:5000/api/savePin'
    data = {
        'latitude': latitude,
        'longitude': longitude
    }
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {user_token}'
    }
    response = requests.post(url, json=data, headers=headers)
    return response.json()
