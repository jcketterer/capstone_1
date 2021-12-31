import requests

API_URL = "https://api.openbrewerydb.org/breweries"


def get_api_response():
    resp = requests.get(f'{API_URL}')
    data = resp.json()
    brews = data

    breweries = []

    for brew in brews:

        beer = {
            'name': brew['name'],
            'brewery_type': brew['brewery_type'],
            'state': brew['state'],
            'city': brew['city'],
            'country': brew['country'],
            'website_url': brew['website_url'],
        }

        breweries.append(beer)
    return breweries


# def api_response():
#     page = 1
#     breweries = []

#     while True:
#         print("----")
#         url = f"{API_URL}?by_state=california&page={page}&per_page=50"
#         print("Requesting url:", url)

#         resp = requests.get(url)
#         data = resp.json()

#         if len(data) == 0:
#             break
#         breweries.extend(data)
#         page += 1


# def get_api_response():
#     resp = requests.get(API_URL)
#     data = resp.json()
#     beers = data

#     breweries = []

#     for beer in beers:

#         brewery = {
#             'name': beer['name'],
#             'state': beer['state']
#         }

#         breweries.append(brewery)
#     return breweries
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
