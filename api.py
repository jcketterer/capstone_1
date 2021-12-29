import requests
API_URL = "https://api.openbrewerydb.org/breweries?by_type=micro&page=1"


def get_api_response():
    resp = requests.get(API_URL)
    data = resp.json()
    beers = data

    breweries = []

    for beer in beers:

        brewery = {
            'name': beer['name'],
            'state': beer['state']
        }

        breweries.append(brewery)
    return breweries
    # url = API_URL
    # breweries = []
    # page = 1

    # while True:
    #     print("*******")
    #     url = f"https://api.openbrewerydb.org/breweries?by_type=micro&page={page}"
    #     print("Requesting", url)

    #     resp = requests.get(url)
    #     data = resp.json()
    #     if len(data) == 0:
    #         break
    #     breweries.extend(data)
    #     page += 1
