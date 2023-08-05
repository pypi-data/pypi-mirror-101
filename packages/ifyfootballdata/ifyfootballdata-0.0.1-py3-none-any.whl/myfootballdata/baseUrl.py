class Url:
    @staticmethod
    def mainUrl():
        url = "http://api.football-data.org/v2"
        return url

    @staticmethod
    def competitionsUrl():
        url = "/competitions/"
        return url

    @staticmethod
    def competitionsByIdUrl(Id):
        url = "/competitions/" + str(Id)
        return url

    @staticmethod
    def matchesUrl():
        url = "/matches"
        return url

    @staticmethod
    def teamsUrl():
        url = "/teams"
        return url

    @staticmethod
    def standingUrl():
        url = "/standings"
        return url

    @staticmethod
    def scorersUrl():
        url = "/scorers"
        return url
