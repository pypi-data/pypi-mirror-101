import requests


class Http:
    @staticmethod
    def get(url, token):
        headers = {'X-Auth-Token': token,
                   'content-type': 'application/json'}
        r = requests.get(url, headers)

        return r
