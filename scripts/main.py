from time import time
import requests
import datetime
import pandas as pd
import sqlite3

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# EXTRACT

USER_ID = "11135754916"
TOKEN = "BQAZS8n3G-b0D2sL7m5uJmYTLyoGoz04gepWWDQ-jwYn8faLD_PDJCf-Tc5LA0J5oQOJUEtPoypFAFfdBIDp9P5Z3PKy25n-_eiI_dhnPz0GRzMs_3pJLdu9SiAYGvPLI3nIaF956e_QBLsoXx4CM04o25bIjlv6EfsaQFNcvEYjz2mQOrF8eg"  # token expires after 3600 s

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

# request (up to 50 songs, max from spotify API)
try:
    req = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix), headers=headers)
    data = req.json()

except Exception as e : 
    print(e)


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

# print(df.head())
# print(df.shape)


# TRANSFORM

def check_data_validation(df):
    # check if the Datframe is empty
    bool_val = True

    if df.empty:
        print("No songs were downloaded. Finishing execution")
        bool_val = False

    # check if primary key is unique, no duplicates
    if pd.Series(df["Played at"]).is_unique:
        pass
    else:
        raise Exception("There are duplicated values. Primary key check violated.")

    # check if df has NaN
    if df.isnull().values.any():
        raise Exception("Null values found.")
    
    # # check if timestamp is indeed from last 24 hours
    # yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    # yesterday = yesterday.replace(hour=0, minute=0, second=0, microsecond=0)

    # print(yesterday)

    # timestamps = df["Timestamp"].tolist()

    # for tst in timestamps :
    #     if datetime.datetime.strptime(tst, "%Y-%m-%d") != yesterday:
    #         print(datetime.datetime.strptime(tst, "%Y-%m-%d"))
    #         print(yesterday)
    #         raise Exception("At least one song was not from the 24 hours range")
    
    return bool_val

if check_data_validation(df):
    print("Data is valid Proceed to Load stage.")



# LOAD

try:
    conn = sqlite3.connect('./database/pass.db')
    cur = conn.cursor()

except Exception as e:
    print(e)




# TODO : github + extract done-> transform part