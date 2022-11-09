import base64
from time import time
import requests
import datetime
import pandas as pd
import sqlite3

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)




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


def run_spotify_etl():
    
    # EXTRACT


    ## AUTHENTICATION

    CLIENT_ID = "58da794fd65e448f96ccbf816bfb673c"
    CLIENT_SECRET = "6dc17c50974046f3bcf206d737f7fe80"

    def get_auth_tkn(client_id, client_secret):

        # Necessary encoding/deconding credentials
        client_creds = f"{client_id}:{client_secret}"
        base64Bytes = base64.b64encode(client_creds.encode('ascii'))
        client_creds_final = base64Bytes.decode('ascii')

        # # header data settings
        # data = {}
        # data['grant_type'] = "client_credentials"
        # # data['json'] = True
        # # data["scope"]= "user-read-recently-played"

        # headers_auth = {}
        # headers_auth["Authorization"] = f"Basic {client_creds_final}"

        token_data = {
            'grant_type': 'authorization_code',
            'response_type': 'code',
            'redirect_uri': 'https://localhost:8888/callback'  # currently on localhost and whitelisted on Spotify
        }


        token_header = {
            'Authorization': f'Basic {client_creds_final}',
            'Content-Type': 'application/x-www-form-urlencoded'
            }

        # AUTH_URL = 'https://accounts.spotify.com/authorize?client_id=58da794fd65e448f96ccbf816bfb673c&response_type=code&redirect_uri=https%3A%2F%localhost:8888%2Fcallback&scope=user-read-recently-played'

        # TOKEN access request
        auth_response = requests.post(
            'https://accounts.spotify.com/api/token', data=data, headers=headers_auth)
        auth_data_json = auth_response.json()

        access_token = auth_data_json['access_token']

        print(access_token)
        print(auth_response.status_code)

        return access_token

    acc_token = get_auth_tkn(CLIENT_ID, CLIENT_SECRET)

    ## TO CHANGE EVERYTIME
    # TOKEN = "BQB8mJO4N66nUUytRQJku3wmppnc5fBgewOvEH0YgscND3tqfJKiYkHdFuHFO9G7nT02kAwnwLl7Qe6drUPm1LnNTl-XTLDX0nXRkpfO2UTc4tLpLW2GF5cV2FmS8wfVJ3vBzWs2_fyuzlEYvI_R3tWxLlHq2IUVRJGC7eLaYoCgR_wV5rYWdQ"

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    # over the last 24 hours
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=1)
    yesterday_unix = int(yesterday.timestamp()) * 1000

    # request (up to 50 songs, max from spotify API)

    try:
        req = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(time=yesterday_unix), headers=headers)
        print("Request status : ", req.status_code)
        data = req.json()

    except Exception as e:
        print(e)
        print("The script is shutting.")
        exit()

    # print(data)
    # print(data["items"][:2])

    song_name = []
    album_name = []
    artist = []
    played_at = []
    tmstp = []

    for item in data["items"]:
        song_name.append(item["track"]["name"])
        album_name.append(item["track"]["album"]["name"])
        artist.append(item["track"]["artists"][0]["name"])
        played_at.append(item["played_at"])
        tmstp.append(item["played_at"][:10])


    df = pd.DataFrame(columns=["song_name", "artist",
                    "album_name", "played_at", "tmstp"])

    df["song_name"] = song_name
    df["artist"] = artist
    df["album_name"] = album_name
    df["played_at"] = played_at
    df["tmstp"] = tmstp




    # TRANFORM CF
    if check_data_validation(df):
        print("Data is valid. Proceed to Load stage.")




    # LOAD
    try:
        conn = sqlite3.connect('./dags/spotify_data_database.db')
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
        # cur.execute("DELETE FROM my_recently_played_songs;")
        df.to_sql("my_recently_played_songs", con=conn, if_exists='replace', index=False)  # if_exists=append instead => adds news to the actual data
        print("Data was successfully added to the table.")
    except Exception as e:
        print("Error occured while updating table :", e)

    # inserted_data = cur.execute("SELECT * FROM my_recently_played_songs").fetchall()
    # for data in inserted_data:
    #     print(data)

    conn.close()

run_spotify_etl()


