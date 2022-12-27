from prefect import flow

from tasks import (
    get_player_profile_data,
    get_player_queue_data,
    transform_player_data,
    transform_queue_player_data,
    save_player_data,
)


@flow(name="get_summoner_data")
def get_summoner_data(summonerName: str):
    player_profile_data = get_player_profile_data(summonerName)
    player_profile_data = transform_player_data(player_profile_data)

    encryptedSummonerId = player_profile_data.get("id")
    player_queue_data = get_player_queue_data(encryptedSummonerId)
    player_queue_data = transform_queue_player_data(player_queue_data)

    player_data = {"profile": player_profile_data, "queues": player_queue_data}
    save_player_data(player_data)
