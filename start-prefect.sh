#!/bin/sh

mkdir -p deployments

prefect deployment build league/workflows/get_summoner_data.py:get_summoner_data \
 --name get_summoner_data --output deployments/get_summoner_data.yaml --apply

prefect agent start -q default
