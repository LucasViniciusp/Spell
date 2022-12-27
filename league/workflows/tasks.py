from datetime import timedelta

from prefect import task
from prefect.tasks import task_input_hash
from decouple import config as dotenv

from league.service import League


league_api = League(api_url=dotenv("RIOT_API_URL"), token=dotenv("RIOT_API_KEY"))


@task
def transform_player_data(data: dict):
    player_data = {
        "id": data.get("id"),
        "account_id": data.get("accountId"),
        "puuid": data.get("puuid"),
        "name": data.get("name"),
        "profile_icon_id": data.get("profileIconId"),
        "level": data.get("summonerLevel"),
        "revision_date": data.get("revisionDate"),
    }
    return player_data


@task
def transform_queue_player_data(data: dict):
    queues = []

    for queue in data:
        queue_player_data = {
            "league_id": queue.get("leagueId"),
            "type": queue.get("queueType"),
            "tier": queue.get("tier"),
            "rank": queue.get("rank"),
            "points": queue.get("leaguePoints"),
            "wins": queue.get("wins"),
            "losses": queue.get("losses"),
            "hotstreak": queue.get("hotStreak"),
            "is_veteran": queue.get("veteran"),
            "is_active": not queue.get("inactive"),
            "is_noob": queue.get("freshBlood"),
        }
        queues.append(queue_player_data)
    return queues


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(minutes=20))
def get_player_profile_data(summonerName: str):
    endpoint_url = f"lol/summoner/v4/summoners/by-name/{summonerName}"
    response = league_api.request_api(endpoint_url)
    return response


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(minutes=20))
def get_player_queue_data(encryptedSummonerId: str):
    endpoint_url = f"lol/league/v4/entries/by-summoner/{encryptedSummonerId}"
    response = league_api.request_api(endpoint_url)
    return response


@task
def save_player_data(player_data: dict):
    league_api.save_player_data(player_data)
