[![alex6970 - basic_etl_project](https://img.shields.io/static/v1?label=alex6970&message=basic_etl_project&color=blueviolet&logo=github)](https://github.com/alex6970/basic_etl_project "Go to GitHub repo")
[![License](https://img.shields.io/badge/License-MIT-blueviolet)](#license)
[![GitHub commits](https://badgen.net/github/commits/alex6970/basic_etl_project)]()  
[![GitHub watchers](https://img.shields.io/github/watchers/alex6970/basic_etl_project.svg?style=social&label=Watchers&maxAge=2592000)]()



# Basic ETL Project


## About the project

This project was inteded to practice data engineering skills with some tools, such as python, Airflow, SQL and APIs in general.

<br>



## Table of Contents

- [Project Organization](#project-organization)
- [Features and uses](#features-and-uses-)
- [Technologies & packages](#technologies--packages-)
- [Credits](#credits-)

<br>



## Project Organization


    ├── dags
    │   │
    │   ├── main.py                   <- Main script, contains the Spotify API Data ETL
    │   │
    │   ├── spotify_de_dag.py         <- Airflow DAG script, with all parameters
    │   │
    │   ├── tkn_refresh.py            <- Script used to refresh the Spotify API
    │   │
    │   ├── auth_notes.md             <- Mardown describing how OAuth works on Spotify API
    │   │
    │   └── another_one.py            <- Yet another
    │
    ├── LICENSE                       <- MIT License
    │
    └── README.md                     <- The top-level README

<br>



## Features and uses 💻

First, you must create an app throught the Spotify Dashboard, where you'll get our credentials (id an secret). The create and run Airflow container with Docker (in docker-compose.yml, specify the path to your dag here).
Read the auth_notes to understand the token process. 

The ETL is intended to run daily (for practice purposes, every 5 mins here). It runs the main script which connects to Spotify user's data (with token), extracts the 50 recently played tracks (limit), proceeds to check data's integrity and load it to sqlite database.

<br>



## Technologies & packages 🔧

&rarr; Python  
&rarr; Requests  
&rarr; Base64  
&rarr; Pandas   
&rarr; Sqlite3   
&rarr; Airflow  
<!---
or `pip freeze > requirements.txt`
-->


<br>





## Credits 🤝

- [Stack Overflow](https://stackoverflow.com/)
- [Spotify documentation](https://developer.spotify.com/)
- [OAuth tutorial](https://www.youtube.com/watch?v=-FsFT6OwE1A)