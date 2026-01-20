
import requests

url = 'http://127.0.0.1:5000/submit'
files = {'file': ('data.csv', 'open("data.csv", "rb")')}
data = {
    'weights': '1,1,1,1',
    'impacts': '+,+,+,-',
    'email': 'test@example.com'
}

# Create a dummy csv if not exists
with open('data.csv', 'w') as f:
    f.write('A,B,C,D\n1,2,3,4\n5,6,7,8')

try:
    print("Sending request...")
    files = {'file': open('data.csv', 'rb')}
    response = requests.post(url, data=data, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response Text: {response.text}")
except Exception as e:
    print(f"Error: {e}")
