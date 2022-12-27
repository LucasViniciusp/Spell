from rest_framework import mixins, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import GenericViewSet

from prefect.deployments import run_deployment

from league.models import Summoner
from league.serializers import SummonerSerializer


# Create your views here.
class SummonerViewset(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):

    queryset = Summoner.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = SummonerSerializer

    def create(self, request, *args, **kwargs):
        response = run_deployment(
            "get_summoner_data/get_summoner_data",
            parameters={"summonerName": request.data.get("name")},
            timeout=0,
        )
        return Response(response.__dict__, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()
