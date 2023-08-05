import requests
from pprint import pprint as pp
from . import exceptions
from . import baseUrl
from . import myhttp


class BaseApi:
    def __init__(self, token):
        if not token:
            raise ValueError("Invalid Token")
        self._token = token

    def getCompetitions(self):
        competition_url = baseUrl.Url.mainUrl() + baseUrl.Url.competitionsUrl()
        response = myhttp.Http.get(competition_url, self._token)
        return response

    def getCompetitionsById(self, Id):
        competition_by_id_url = baseUrl.Url.mainUrl() + baseUrl.Url.competitionsByIdUrl(Id)
        response = myhttp.Http.get(competition_by_id_url, self._token)
        return response

    def getMatches(self, Id):
        matches_url = baseUrl.Url.mainUrl() + baseUrl.Url.competitionsByIdUrl(Id) + \
            baseUrl.Url.matchesUrl()
        response = myhttp.Http.get(matches_url, self._token)
        return response

    def getTeams(self, Id):
        teams_url = baseUrl.Url.mainUrl() + baseUrl.Url.competitionsByIdUrl(Id) + \
            baseUrl.Url.teamsUrl()
        response = myhttp.Http.get(teams_url, self._token)
        return response

    def getScores(self, Id):
        scores_url = baseUrl.Url.mainUrl() + baseUrl.Url.competitionsByIdUrl(Id) + \
            baseUrl.Url.scorersUrl()
        response = myhttp.Http.get(scores_url, self._token)
        return response

    def getStandings(self, Id):
        standings_url = baseUrl.Url.mainUrl() + baseUrl.Url.competitionsByIdUrl(Id) + \
            baseUrl.Url.standingUrl()
        response = myhttp.Http.get(standings_url, self._token)
        return response
