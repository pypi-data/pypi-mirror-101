import pickle
import pandas
import requests
import pkg_resources
from . import epic_leaderboard


def get_score(prediction_df):
    """Get the percent of the predictions that are correct.

    Args:
        prediction_df (`pandas.core.frame.DataFrame`): Dataframe containing 
            your predictions in the column named 'prediction'.
    
    Returns:
        float: The percent of the predictions which are correct.
    
    """
    if "prediction" not in list(prediction_df):
        raise KeyError(
            "The dataframe must contain the predictions in a column named "
            "'prediction'."
        )
    
    stream = pkg_resources.resource_stream(__name__, "res/checking_data.pkl")
    raw_data = pickle.load(stream)
    truth_df = pandas.DataFrame(raw_data, columns=["PassengerId", "truth"])

    both_df = prediction_df.merge(truth_df, on="PassengerId", how="inner")

    correct = both_df["prediction"] == both_df["truth"]
    perc_correct = sum(correct) / len(raw_data)
    return perc_correct


def percent_correct(team_name, prediction_df):
    """Get the overall accuracy of your predictions and upload to leaderboard.
    
    Args:
        team_name (str): Name of your team which will be published to the
            leaderboard. Max 20 characters and alphanumeric only!
        prediction_df (`pandas.core.frame.DataFrame`): Dataframe containing 
            your predictions in the column named 'prediction'.
    
    Returns:
        float: The percent of your predictions which were correct, between 0 and
            100, rounded to 3 decimal places.
    
    """
    team_name = epic_leaderboard.clean_team_name(team_name)
    score = get_score(prediction_df) * 100
    
    r = epic_leaderboard.upload_score(team_name, score)
    if r["result"] != True:
        raise Exception(
            f"Score not accepted by leaderboard. The score is {score} and "
            "should be 0 < score < 100. Check also that the team_name is valid."
        )
    
    return round(score, 3)


def leaderboard(team_name):
    """Return the leaderboard around your team.
    
    Args:
        team_name (str): Name of your team.
    
    Returns:
        `pandas.core.frame.DataFrame`
    
    """
    team_name = epic_leaderboard.clean_team_name(team_name)
    url = "http://epicleaderboard.com/api/getScores.php"
    headers = epic_leaderboard.get_headers()
    
    data = {
        "accessID": epic_leaderboard.get_leaderboard_info()[0],
        "username": team_name,
        "around": 1
    }
    r = requests.get(url, headers=headers, params=data)
    d = r.json()
    if "scores" not in d.keys():
        raise Exception("Failed to retrieve leaderboard.")
    
    cols_needed = ["rank", "username", "score", "timestamp"]
    cols_mapping = {
        "rank": "rank",
        "username": "team_name",
        "score": "percent_accurate",
        "timestamp": "timestamp"
    }
    
    df = pandas.DataFrame(d["scores"])[cols_needed]
    df.rename(columns=cols_mapping, inplace=True)\

    df["timestamp"] = (
        pandas.to_datetime(df["timestamp"])
            .dt.tz_localize("America/Los_Angeles")
            .dt.tz_convert("Europe/London")
            .dt.strftime("%Y-%m-%d %H:%M:%S")
    )
    return df
