""" Sending image with requests """


import requests


try:
    url = 'http://192.168.51.74:8080/api/update-graph/'
    json = {
        'graph_id': 70,
        'point': {
            'x': 1,
            'y': 2
        }
    }
    resp = requests.post(url, json=json)
    print(resp.text)
except requests.exceptions.ConnectionError:
    print('Connection error.')
