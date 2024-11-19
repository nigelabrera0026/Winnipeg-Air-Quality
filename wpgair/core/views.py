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


def search(data, query):
    """
    Append data if search query matches anything.
    """
    filtered_data = []

    #? Loops through data to check if query is in the retrieved data.
    for observation in data:
        location_name = observation.get("locationname", '').lower()

        if query in location_name:
            filtered_data.append(observation)

    return  filtered_data


def index(request):
    #? Defining the API endpoint
    api_url = "https://data.winnipeg.ca/resource/f58p-2ju3.json"

    #? Implementing a limit and the default as 10
    limit = int(request.GET.get('limit', 5))

    #! Base query parameters
    # query_param = f"?$limit={limit}"

    #? Creating a search query and stripping it into keywords
    search_query = request.GET.get('search', '').lower().strip()

    #? Fetch data from the API
    response = requests.get(api_url)
    data = response.json()

    time_format(data) # Invoke the function to format the time

    if search_query:
        data = search(data, search_query)
    #     data = [observation for observation in data if search_query in observation.get("locationname", "").lower()]

    result_data = data[:limit] # include limit 
    
    no_data_message = None

    #? If no data is returned
    if not data:
        no_data_message = "No Data Available!"

    #? Context variables are defined here (right side variables) 
    #? and would be forwarded to the frontend (left side variables)
    context = {
        'air_quality_data': result_data,
        'limit': limit,
        'search_query': search_query,
        'no_data_message': no_data_message,
    }

    return render(request, 'core/index.html', context)