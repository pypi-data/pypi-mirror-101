from collections import namedtuple

from constants import key
from typing import NamedTuple
from datetime import datetime
import requests


class Insight:
    def __init__(self):
        """
        Provides per-Sol summary data for each of the last seven available Sols
        Insight API: https://api.nasa.gov/#insight

        """
        payload = {'api_key': key, 'feedtype': "json", 'ver': "1.0"}
        response = requests.get(f'https://api.nasa.gov/insight_weather/?', params=payload)
        self.limit = response.headers['X-RateLimit-Limit']
        self.remaining = response.headers['X-RateLimit-Remaining']
        response = response.json()
        self.solkeys = response['sol_keys']
        self.atmopres, self.utcs, self.seasons, self.month_ordinal = [], [], [], []
        for solk in self.solkeys:
            seasons = {
                "northern": response[solk]['Northern_season'],
                "season": response[solk]['Season'],
                "southern": response[solk]["Southern_season"]
            }
            utcs = {
                "first": response[solk]['First_UTC'],
                "last": response[solk]['Last_UTC']
            }
            self.atmopres.append(namedtuple("AtmoPressure", response[solk]['PRE'].keys())(*response[solk]['PRE'].values()))
            self.utcs.append(namedtuple("UTCS", utcs.keys())(*utcs.values()))
            self.seasons.append(namedtuple("Seasons", seasons.keys())(*seasons.values()))
            self.month_ordinal.append(response[solk]['Month_ordinal'])


class UTCS(NamedTuple):
    first: datetime
    last: datetime

