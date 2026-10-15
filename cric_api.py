import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("RAPIDAPI_KEY")
API_HOST = "cricbuzz-cricket.p.rapidapi.com"

headers = {
    "x-rapidapi-key": API_KEY,
    "x-rapidapi-host": API_HOST
}


def get_scorecard(match_id):
    url = f"https://{API_HOST}/mcenter/v1/{match_id}/hscard"

    response = requests.get(url, headers=headers)

    response.raise_for_status()
    data = response.json()
    # print(data)
    print("SCORECARD KEYS:")
    print(data.get("scorecard",[{}])[0].keys())
    print("TOP LEVEL KEYS:",data.keys())
    print("FULL API DATA:",data)
    print("BOWLER DATA:")
    print(data.get("scorecard",[{}])[0].get("bowler"))
    print("FOW DATA:")
    print(data.get("scorecard",[{}])[0].get("fow"))
    
    return data
    # return response.json()


def get_match_info(match_id):
    url = f"https://{API_HOST}/mcenter/v1/{match_id}/hscard"

    response = requests.get(
        url,
        headers=headers
    )

    response.raise_for_status()

    return response.json()