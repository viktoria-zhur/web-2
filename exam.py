import requests
url = 'http://217.71.129.139:6030/task/7ad9'
data = {
    "key": "7ad+98a9+9a",
    "name": "Журавлева Виктория Александровна",
    "group": "ФБИ-34"
}
response = requests.delete(url, json=data)
print(response.text)
