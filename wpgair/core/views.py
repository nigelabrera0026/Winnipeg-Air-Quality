from django.shortcuts import render

import requests
from datetime import datetime

# Create your views here.

def time_format(data):
    """
    Formats the time from the API dataset and using it for the index.html
    """
    #? Looping through all the data set.
    for observation in data:

        #? Initialize
        observation["formatted_time"] = ""
        
        #? retrieving observationtime section of the API
        observation_time = observation.get("observationtime", '')

        if observation_time:
            #? Format it
            #? The structure is by default is %Y-%m-%dT%H:%M:%S.%f
            #? I'm converting it with spaces "%b %d, %Y %I:%M %p"
            try:
                observation['formatted_time'] = datetime.strptime(
                    observation_time, "%Y-%m-%dT%H:%M:%S.%f"
                    ).strftime("%b %d, %Y %I:%M %p")
            
            #? If data is invalid which would be the API's fault.
            except ValueError:
                observation['formatted_time'] = "Invalid Date"

    return observation["formatted_time"]


def search(data, search_query):
    """
    Search for a specific function
    """
    results = []

    #? Looping through the data
    for observation in data:
        location_name = observation.get("locationname", '').lower()

        #? Check if the location name contains the search query
        if search_query in location_name:
            results.append(observation)

    return results



def index(request):
    #? Defining the API endpoint
    api_url = "https://data.winnipeg.ca/resource/f58p-2ju3.json"

    #? Implementing a limit and the set the default as 10
    limit = int(request.GET.get('limit', 10))

    #? Query Parameters
    query_param = f"?$limit={limit}"

    #? Fetch data for default (If page is refreshed for default)
    response = requests.get(f"{api_url}{query_param}")

    #? Parsing
    data = response.json()

    #? Invoke the function to format the time.
    time_format(data)

    #? Creating a search query and stripping it into keywords
    #? .get('search', '') is pointing in the input with the name search
    search_query = request.GET.get('search', '').lower().strip()

    result_data = []
    no_data_message = None

    if search_query:
        result_data = search(data, search_query)

        if not result_data:
            no_data_message = "No Data Available!"

    else: #? Show default information
        result_data = data
        no_data_message = None
    
    #? Context variables are defined here (right side variables) 
    #? and would be forwarded to the frontend (left side variables)
    context = {
        'air_quality_data': result_data,
        'limit' : limit,
        'search_query': search_query,
        'no_data_message': no_data_message,
    }
    
    return render(request, 'core/index.html', context)