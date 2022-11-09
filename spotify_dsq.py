import base64
import requests

CLIENT_ID = "58da794fd65e448f96ccbf816bfb673c"
CLIENT_SECRET = "6dc17c50974046f3bcf206d737f7fe80"

auth_str = '{}:{}'.format(CLIENT_ID, CLIENT_SECRET)
b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()

## Url to insert in navbar, to obtain authorization access
# https://accounts.spotify.com/authorize?client_id=58da794fd65e448f96ccbf816bfb673c&response_type=code&redirect_uri=https%3A%2F%2Flocalhost%3A8888%2Fcallback&scope=user-read-recently-played


# Creds encoded : NThkYTc5NGZkNjVlNDQ4Zjk2Y2NiZjgxNmJmYjY3M2M6NmRjMTdjNTA5NzQwNDZmM2JjZjIwNmQ3MzdmN2ZlODA=

# curl -H "Authorization: Basic NThkYTc5NGZkNjVlNDQ4Zjk2Y2NiZjgxNmJmYjY3M2M6NmRjMTdjNTA5NzQwNDZmM2JjZjIwNmQ3MzdmN2ZlODA=" -d grant_type=authorization_code -d code=AQDQXFb8AwLNxjz43FcL_HRA7qJyNljL_FrbME1tOUm6h_7XiEvFVEDk1SsQaRuLqsqBqO7RtBCl7CUA1S1CZrMwYYk04uEXzPI0Hsy7imlcKfwJIMDI_3czfuEy9lVd5ncLssaWlxDGCXaI3vAuFVe3Z0N2xbh_1B0P4kVcNzoLfCFHcT7QPDvStbd7g-5C88EtPO9qmfhPXjlmSAE -d redirect_uri=https%3A%2F%2Flocalhost%3A8888%2Fcallback https://accounts.spotify.com/api/token

# => 

# {"access_token":"BQBsL1_5VrhMdD3BZUmks48b-a8Xka7AZMFHncGlwOk01MY7y3IYLZ-qnIOc_0ZZx__jhrMG-I6h9o2iyx54eb-dUpwAsQWO__kFNpOuhMMTwpg1Hc7qkAL6EH_zPzasrVzvzqlE0ST4e-TkC-2nbu5pUVgg7uBB3z7qiI_0ez4Bnj42fqIK0pzG","token_type":"Bearer","expires_in":3600,"refresh_token":"AQAvIqctxHcXJZsSMSqJ5yyxu4vAfA3PLRTVBv_kVvxVlpevms8NQu3_bmPUth1AsgZMXO4eNZoN6BC1S8eISHwZPngY1XjYFogULrIxwu_uuoMayyBwuaDLVG4Vv3U2cAI","scope":"user-read-recently-played"}

# acc = BQBsL1_5VrhMdD3BZUmks48b-a8Xka7AZMFHncGlwOk01MY7y3IYLZ-qnIOc_0ZZx__jhrMG-I6h9o2iyx54eb-dUpwAsQWO__kFNpOuhMMTwpg1Hc7qkAL6EH_zPzasrVzvzqlE0ST4e-TkC-2nbu5pUVgg7uBB3z7qiI_0ez4Bnj42fqIK0pzG

# ref = AQAvIqctxHcXJZsSMSqJ5yyxu4vAfA3PLRTVBv_kVvxVlpevms8NQu3_bmPUth1AsgZMXO4eNZoN6BC1S8eISHwZPngY1XjYFogULrIxwu_uuoMayyBwuaDLVG4Vv3U2cAI

url = "https://accounts.spotify.com/api/token"

response = requests.post(url, data={"grant_type": "refresh_token", "refresh_token": "AQAvIqctxHcXJZsSMSqJ5yyxu4vAfA3PLRTVBv_kVvxVlpevms8NQu3_bmPUth1AsgZMXO4eNZoN6BC1S8eISHwZPngY1XjYFogULrIxwu_uuoMayyBwuaDLVG4Vv3U2cAI"}, headers= {"Authorization": "Basic " + b64_auth_str})
response_data = response.json()
print(response_data["access_token"])
print(response_data)
