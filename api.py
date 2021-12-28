def get_api_response(data):

    brewery = data[0]

    breweries = []

    for brew in brewery:

        breweries += brew['name'], brew['brewery_type'], brew['country']

    return breweries
