import requests

from league.models import Summoner, Queue


class RiotApiException(Exception):
    pass


class League:
    def __init__(self, api_url, token: str):
        self.api_url = api_url
        self.token = token

    def request_api(self, path):
        RIOT_API_KEY = self.token

        response = requests.get(f"{self.api_url}/{path}?api_key={RIOT_API_KEY}")

        try:
            if response.status_code == 403:
                raise RiotApiException(f"Invalid API_KEY: {response.json()}")

            response.raise_for_status()

        except Exception as err:
            raise RiotApiException(err)

        return response.json()

    def get_player_profile_data(self, summonerName: str):
        endpoint_url = f"lol/summoner/v4/summoners/by-name/{summonerName}"
        return self.request_api(endpoint_url)

    def get_player_queue_data(self, encryptedSummonerId: str):
        endpoint_url = f"lol/league/v4/entries/by-summoner/{encryptedSummonerId}"
        return self.request_api(endpoint_url)

    def save_player_data(self, player_data: dict):
        profile_data = player_data.get("profile")
        queue_data = player_data.get("queues")

        id = profile_data.pop("id")
        summoner, _ = Summoner.objects.update_or_create(id=id, defaults=profile_data)

        for queue in queue_data:
            queue_type = queue.pop("type")
            queue, _ = Queue.objects.update_or_create(
                summoner=summoner, type=queue_type, defaults=queue
            )
