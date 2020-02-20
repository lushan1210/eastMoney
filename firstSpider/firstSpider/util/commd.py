
import hashlib
import json
import requests
import base64
from io import BytesIO
from sys import version_info


def get_md5(url):
    if isinstance(url, str):
        url = url.encode('utf-8')
    m = hashlib.md5()
    m.update(url)
    return m.hexdigest()


def base64_captcha(img):
    data = {"username": 'lushan1210', "password": 'qq139319', "image": img}
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""