from time import time
from numpy import append
import requests
import datetime
import pandas as pd
import sqlite3

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

# EXTRACT

# USER_ID = "11135754916"
TOKEN = "BQDEGnHvEAxJZbEpcsnrRWzj85Pyb4GF_-KtJmsgiwJV1HucxSA_ffbm7p4Vv2efDhK1NxZdj4p457nps3aITFs9KGu8NQIlMkXTSpV6JovMz-kY1F00xvoTHygAVXU47qKYxVSLrrRgL8mrhjm79uiqmReLzmEEc2y5P0xLVuyGHDBbFgpH5g"  # token expires after 3600 s

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
    req = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(
        time=yesterday_unix), headers=headers)
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

df = pd.DataFrame(columns=["song_name", "artist",
                  "album_name", "played_at", "tmstp"])

df["song_name"] = song_name
df["artist"] = artist
df["album_name"] = album_name
df["played_at"] = played_at
df["tmstp"] = tmstp

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
    if pd.Series(df["played_at"]).is_unique:
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
    print("Data is valid. Proceed to Load stage.")



# LOAD

try:
    conn = sqlite3.connect('./database/spotifydata_database.db')
    cur = conn.cursor()

except Exception as e:
    print(e)


cur.execute("""

CREATE TABLE IF NOT EXISTS my_recently_played_songs (
    song_name VARCHAR(200),
    album_name VARCHAR(200),
    artist VARCHAR(200),
    played_at VARCHAR(200) PRIMARY KEY,
    tmstp VARCHAR(200)
)

""")

print("Database opened.")

try:
    df.to_sql("my_recently_played_songs", con=conn, if_exists='replace', index=False) #append instead when done
    print("Data was successfully added to the table.")
except Exception as e : 
    print("Error occured :",e)

# inserted_data = cur.execute("SELECT * FROM my_recently_played_songs").fetchall()
# for data in inserted_data:
#     print(data)

conn.close()


# TODO : github udpates + Load + orchestration + getting token automation