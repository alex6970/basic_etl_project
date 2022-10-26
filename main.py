import requests
import datetime
import pandas as pd

USER_ID = "11135754916"
TOKEN = "BQCrXOzqVAReebAnOB31mx7RZtSe8ayLe6iuQN_l76C47otd2gnd02O8LJZKdax64HtEK0TxVVpvaTOPV8-ZcMGVPREt6PWxTktN3FB-nUn89AByYMPqw0Jd-Bv57WlQ1G98TQAyHXg9c1rePRt-_k85g-WCGgbwKB0tAC9dZrej28q-n96r2g"  # token expires after 3600 s

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "Authorization" : "Bearer {token}".format(token = TOKEN)
}

# over the last 24 hours
today = datetime.datetime.now()
yesterday = today - datetime.timedelta(days=1)

# converting to unix milliseconds, as accepted by the API
yesterday_unix = int(yesterday.timestamp()) * 1000 

req = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterday_unix), headers = headers)
data = req.json()

# print(data)
# print(data["items"][:2])

song_name = []
album_name = []
artist = []
played_at = []
tmstp = []

for item in data["items"] : 
    song_name.append(item["track"]["name"])
    album_name.append(item["track"]["album"]["name"])
    artist.append(item["track"]["artists"][0]["name"])
    played_at.append(item["played_at"])
    tmstp.append(item["played_at"][:10])


# for x in range(2):
#     print(song_name[x])
#     print(album_name[x])
#     print(artist[x])
#     print(played_at[x])
#     print(tmstp[x])
#     print("\n")

df = pd.DataFrame(columns=["Song", "Artist", "Album", "Played at", "Timestamp"])

df["Song"] = song_name
df["Artist"] = artist
df["Album"] = album_name
df["Played at"] = played_at
df["Timestamp"] = tmstp

print(df.head())

# TODO : github + extract done-> transform part