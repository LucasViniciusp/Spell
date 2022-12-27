from rest_framework import serializers

from league.models import Summoner


class SummonerSerializer(serializers.ModelSerializer):
    queues = serializers.SerializerMethodField()

    class Meta:
        model = Summoner
        fields = ("id", "name", "profile_icon_id", "level", "queues")

    def get_queues(self, obj):
        return obj.queues.values()
