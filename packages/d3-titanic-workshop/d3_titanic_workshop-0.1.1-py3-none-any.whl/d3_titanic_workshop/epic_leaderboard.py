import re
import requests
import hashlib


def clean_team_name(team_name):
    if team_name == "change_me":
        raise Exception(
            "Change your team_name to something other than the default."
        )
    
    if len(team_name) > 20:
        team_name = team_name[0:20]
    
    regex = re.compile("[^A-Za-z0-9]")
    team_name = regex.sub("", team_name)
    
    return team_name

def get_headers():
    headers = {
        "User-Agent": "X-UnrealEngine-EpicLeaderboard",
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/vnd.epicleaderboard.v2+json"
    }
    return headers

def get_leaderboard_info():
    info = ("8c5a12fc290fe521b2aea4efdf9bed97", "4f92a40344")
    return info

def upload_score(team_name, score):
    headers = get_headers()
    url = "http://epicleaderboard.com/api/submitScore.php"
    score = f"{score:.3f}"
    leaderboard_id, key = get_leaderboard_info()
    metadata = ""
    
    hash_str = f"{team_name}{score}{key}{metadata}"
    data = {
        "accessID": leaderboard_id,
        "username": team_name,
        "score": score,
        "meta": metadata,
        "hash": str(hashlib.md5(hash_str.encode("utf-8")).hexdigest())
    }
    r = requests.post(url, headers=headers, data=data)
    return r.json()
