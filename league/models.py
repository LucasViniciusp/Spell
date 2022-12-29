from django.db import models
from decouple import config as dotenv

if dotenv("PREFECT_AGENT_PROCESS", default=False):
    import django
    django.setup()

class Summoner(models.Model):
    id = models.CharField(primary_key=True, max_length=120)
    account_id = models.CharField(max_length=120)
    puuid = models.CharField(unique=True, max_length=120)
    name = models.CharField(max_length=40)
    profile_icon_id = models.IntegerField()
    level = models.IntegerField()
    revision_date = models.BigIntegerField()


class Queue(models.Model):
    summoner = models.ForeignKey(
        Summoner, on_delete=models.PROTECT, related_name="queues"
    )
    league_id = models.CharField(max_length=120)
    type = models.CharField(max_length=40)
    tier = models.CharField(max_length=40)
    rank = models.CharField(max_length=40)
    wins = models.IntegerField()
    losses = models.IntegerField()
    points = models.IntegerField()
    is_veteran = models.BooleanField()
    is_active = models.BooleanField()
    is_noob = models.BooleanField()
    hotstreak = models.BooleanField()
