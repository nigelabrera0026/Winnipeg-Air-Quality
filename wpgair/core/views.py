from django.shortcuts import render

import requests

# Create your views here.
def index(request):
    #? Defining the API endpoint
    api_url = "https://data.winnipeg.ca/resource/f58p-2ju3.json"

    #? Implementing a limit and the set the default as 10
    limit = int(request.GET.get('limit', 10))

    #? Fetch data
    response = requests.get(f"{api_url}?$limit={limit}")

    #? Parsing
    data = response.json()

    context = {
        'air_quality_data': data,
        'limit' : limit,
    }
    
    return render(request, 'core/index.html', context)