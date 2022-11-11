# Authorization & Authentication token ⚠🔐

Three OAuth flows exist with Spotify API. The one used is this project is **Authorization Code Flow**, which allows to access user's personal data, thanks to a token (that lasts 3600s and must be refreshed).

<br>

## **Steps :**

Thesse steps only need to be performed once (first tages of the project), to obtain de the final refresh token.

<br>

### **1. Request User authorization :**
the auth request is made by getting a code. In My Dashboard/myapp insert your Redirect uri (must be identical to the one inserted in the following link) and the copy/paste this link in your favourite web browser (with the right parameters):

    https://accounts.spotify.com/authorize?client_id=[YOURCLIENT_ID]&response_type=code&redirect_uri=[YOURENCODED_REDIRECT_URI]&scope=[YOUR_SCOPES]


    Result : https://localhost:8888/callback?code=[your code is here]

<br>

### **2. Request first access token + refresh token :**
Spotify API tokens last 3600s each. They must be refreshed thanks to the refresh token.
To obtain these two type of tokens, we use curl (in the CMD) with the following parameters : 

        curl -H "Authorization: Basic [base64 CLIENT_ID:CLIENT_SECRET]" -d grant_type=authorization_code -d code=[code obtained in the last step, through url] -d redirect_uri=[YOURENCODED_REDIRECT_URI] https://accounts.spotify.com/api/token

        Result : {"access_token":"THE TOKEN","token_type":"Bearer","expires_in":3600,"refresh_token":"THE REFRESH TOKEN","scope":"your scopes"}








Props to [this tutorial](https://www.youtube.com/watch?v=-FsFT6OwE1A) and [the official documentation.](https://developer.spotify.com/documentation/general/guides/authorization/code-flow/)
