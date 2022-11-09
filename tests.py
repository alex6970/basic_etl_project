import base64
import requests

# AUTHORIZATION ACCESS -> TOKEN ACCESS

## Url to insert in navbar, to obtain authorization access
# AUTH_URL = "https://accounts.spotify.com/authorize?client_id=58da794fd65e448f96ccbf816bfb673c&response_type=code&redirect_uri=https%3A%2F%2Flocalhost%3A8888%2Fcallback&scope=user-read-recently-played"
# => AQD8nN5WxL05Gcq_rpzcpFSuHieba_kH6CGyLlLIUHPRL2S1Adw_Bf-ZgeaFX-fRMjCcagaGSZYshCKAb2jlFCj9HKp0fDZK2SKLq80JB8WL4aSFPYNnqj77zLPk7y9DwJEkF-prX8SdGFSpHvchR3J_pnOD5b1GItPTPQaIqCqbPw2r6b59UgOmQ7W2dUfTMUtVjZZkusCrHcpm4-0

auth_code = "AQBCqlPPf5EgGmjRo16CIWOHKBapWBFWDOf75rB312aqXNZ0BVOqEVMnZrD6Nhno_FbGtYHoZfoKh4LXU3fTz_3TBV42svOyaz6aWqQyFhwE4h5dJoZme3_37iFL_-fxbfe6UgjzTN7Sbwgs2onl9hJuadmQr1n_O76vPullNGylRYiZzs5NhvA94yRhCAA5RbO4qWHtZgsKmKmYwzg"

CLIENT_ID = "58da794fd65e448f96ccbf816bfb673c"
CLIENT_SECRET = "6dc17c50974046f3bcf206d737f7fe80"

# Necessary encoding/deconding credentials
client_creds = f"{CLIENT_ID}:{CLIENT_SECRET}"
base64Bytes = base64.b64encode(client_creds.encode())
client_creds_final = base64Bytes.decode()

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
BASE_URL = 'https://api.spotify.com/v1/'


# curl -H "Authorization: Basic NThkYTc5NGZkNjVlNDQ4Zjk2Y2NiZjgxNmJmYjY3M2M6NmRjMTdjNTA5NzQwNDZmM2JjZjIwNmQ3MzdmN2ZlODA=" -d grant_type=authorization_code -d code=AQBCqlPPf5EgGmjRo16CIWOHKBapWBFWDOf75rB312aqXNZ0BVOqEVMnZrD6Nhno_FbGtYHoZfoKh4LXU3fTz_3TBV42svOyaz6aWqQyFhwE4h5dJoZme3_37iFL_-fxbfe6UgjzTN7Sbwgs2onl9hJuadmQr1n_O76vPullNGylRYiZzs5NhvA94yRhCAA5RbO4qWHtZgsKmKmYwzg -d redirect_uri=https%3A%2F%2Flocalhost%3A8888%2Fcallback https://accounts.spotify.com/api/token

# {"access_token": "BQCJiSoDKE_a0ihBndGTrVr_BgLNSfoP9PjuiVrfrgRu-aCjk9SZAxgGOGDtlQHM43cpywKo8PtV_AcnWnDB_iU5GLFO7pI4b9R62EvKCJ-miXwhKVFCvqsHI1yRo6TMv2C3C8XqhfXc9VgM_MEsHsMcV0XfQdrYq6_iRcYeAhekiJzHyKqX4s6U", 
# "token_type": "Bearer",
#     "expires_in": 3600, 
#     "refresh_token": "AQDAnSjnjQrOVYxiXnaJv5QHH4KLRU8A64vU9U8BmA0jklW0ScWiA-RGbr9yptB7VBvuKGQFKHxIbPEKQa_vnUVytdfqIqrRL4WhweamzmRAelF3NMDPoIE98cP8rLR5eoA", 
#     "scope": "user-read-recently-played"}

spotify_token = 'BQCKgsFdKXZleWinet56zOUIXx1reVX8pjCDozHaChHbT0gB2xKRbkVXKh1S_fsd4CKXXbR8GxMiTapiIXmMe8sP69HYtcm0zCTA4LGI329gGD-Hdww7K8MBU4FhxLWyYNLgFTnv4CetMbdhf27RPFZzQQs3Qm3TyO2YWNqwgc5b0eRraPYXBSIZ'
refresh_token = 'AQBMq0LpsyvEnrbmnZ-9Knc4cupwZmqUuj0cOnSVBPIOHKD48ckXLhVEL2Ef8fGc9PdX5hfS6KaYpSFyyZFu2bgZY49Rx9VmMNEoYcuN0x0fF2pHQ2BcbbVgweyaKZYb8-8'


request_body = {
    "grant_type": "refresh_token",
    "code": "AQBCqlPPf5EgGmjRo16CIWOHKBapWBFWDOf75rB312aqXNZ0BVOqEVMnZrD6Nhno_FbGtYHoZfoKh4LXU3fTz_3TBV42svOyaz6aWqQyFhwE4h5dJoZme3_37iFL_-fxbfe6UgjzTN7Sbwgs2onl9hJuadmQr1n_O76vPullNGylRYiZzs5NhvA94yRhCAA5RbO4qWHtZgsKmKmYwzg",
    "redirect_uri": "https://localhost:8888/callback",
    "client_id": "58da794fd65e448f96ccbf816bfb673c",
    "client_secret": "6dc17c50974046f3bcf206d737f7fe80"
}
r = requests.post(url=TOKEN_URL, data=request_body)
resp = r.json()

print(resp)


# def refresh_token(creds_bas64):

#     # tkn_data = {
#     #     'grant_type': 'refresh_token',
#     #     'refresh_token': refresh_token }

#     # tkn_headers = {
#     #     'Authorization': 'Basic {client_creds}'.format(client_creds=creds_bas64)
#     # }

#     # response = requests.post(TOKEN_URL, data=tkn_data, headers=tkn_headers)
    
#     # response_json = response.json()
#     # print(response_json)

    
# auth_str = '{}:{}'.format(CLIENT_ID, CLIENT_SECRET)
# b64_auth_str = base64.urlsafe_b64encode(auth_str.encode()).decode()


    


# refresh_token(client_creds_final)
# # Necessary encoding/deconding credentials
# client_creds = f"{CLIENT_ID}:{CLIENT_SECRET }"
# base64Bytes = base64.b64encode(client_creds.encode())
# auth_header = base64Bytes.decode()

# headers = {
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Authorization': 'Basic %s' % auth_header
# }

# data = {
#     'grant_type': 'authorization_code',
#     'code': auth_code,
#     'redirect_uri': 'https://localhost:8888/callback',
#     'client_id': CLIENT_ID,
#     'client_secret': CLIENT_SECRET
# }

# # Make a request to the /token endpoint to get an access token
# access_token_request = requests.post(
#     url=TOKEN_URL, data=data, headers=headers)

# # convert the response to JSON
# access_token_response_data = access_token_request.json()

# print(access_token_response_data)

# # save the access token
# access_token = access_token_response_data['access_token']

# print(access_token)