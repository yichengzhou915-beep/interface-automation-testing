import base64
import hashlib
import uuid
import time


def make_hua5_auth(authentication='', api_config=None, time_difference=0):
    hua5_auth = ''
    if api_config is None:
        raise ValueError("error")

    app_id = api_config.get('appId')
    app_secret = api_config.get('appSecret')

    timestamp = int(time.time() * 1000) + time_difference

    uid = ''

    split_token = authentication.split("USERID ")[1]
    uid = base64.b64decode(split_token).decode().split(":")[2]


    nonce = str(uuid.uuid4()).replace('-', '')[:32]
    sign = hashlib.md5((app_id + str(timestamp) + nonce + uid + app_secret).encode('utf-8')).hexdigest()

    auth_string = f"{app_id}:{timestamp}:{nonce}:{uid}:{sign}"
    hua5_auth = base64.b64encode(auth_string.encode('utf-8')).decode('utf-8')

    return hua5_auth


api_config = {
    'appId': 'hua5_text',
    'appSecret': 'hua5_123456'
}

authentication = "USERID aHVhNV90ZXh0OkZ6NmxrQTEzSGNaV2Zwdm44c3RlYkxPVlJEU0dUbTRLOjcwNDA4MDow"
hua5_auth = make_hua5_auth(authentication, api_config)
print(hua5_auth)
