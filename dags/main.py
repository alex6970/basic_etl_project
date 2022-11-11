from time import time
import requests
import datetime
import pandas as pd
import sqlite3
from tkn_refresh import refresh_spotify_token

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

CLIENT_ID = ""  # TO INSERT
CLIENT_SECRET = ""  # TO INSERT
refresh_token_from_curl = ""  # TO INSERT

## AUTHENTICATION
ACCESS_TOKEN = refresh_spotify_token(CLIENT_ID, CLIENT_SECRET, refresh_token_from_curl)



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

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=ACCESS_TOKEN)
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
        # if_exists=append instead => adds new songs to the current database each time DAG runs
        df.to_sql("my_recently_played_songs", con=conn, if_exists='replace', index=False)
        print("Data was successfully added to the table.")
    except Exception as e:
        print("Error occured while updating table :", e)

    # inserted_data = cur.execute("SELECT * FROM my_recently_played_songs").fetchall()
    # for data in inserted_data:
    #     print(data)

    conn.close()

run_spotify_etl()


