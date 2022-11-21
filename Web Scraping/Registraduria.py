import requests

url = "https://apitude.co/api/v1.0/requests/registraduria-co/"
payload = {'date_expedition': '2016-01-16', 'document_number': '1030683998'}
headers = {
    'x-api-Token': 'C2g8qqtHlYSUx1NLaVTXozgyA',
    'Content-Type': 'json',
    'username':'user@example.com',
    'password':'AFakePassword'
}
response = requests.post(url, headers=headers, data=payload)
print(response.json())