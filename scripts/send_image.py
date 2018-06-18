""" Sending image with requests """
import requests
from PIL import Image
import base64

im = Image.open('im.png')
im_b = im.tobytes()

try:
    url = 'http://127.0.0.1/api/update-graph/'
    im_s = base64.b64encode(im_b).decode('utf-8')
    json = {
        'graph_id': 1,
        'image': {
            'width': im.width,
            'height': im.height,
            'mode': im.mode,
            'data': im_s
        }
    }
    resp = requests.post(url, json=json)
    print(resp.text)
except requests.exceptions.ConnectionError:
    print('Connection error.')
