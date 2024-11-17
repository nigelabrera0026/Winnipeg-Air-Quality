from django.shortcuts import render

import requests
from datetime import datetime
import re

# Create your views here.
def index(request):
    #? Defining the API endpoint
    api_url = "https://data.winnipeg.ca/resource/f58p-2ju3.json"

    #? Implementing a limit and the set the default as 10
    limit = int(request.GET.get('limit', 10))

    #? Creating a search query and stripping it into keywords
    search_query = request.GET.get('search', '').lower().strip()

    #? Query Parameters
    query_param = f"?$limit={limit}"

    #? Fetch data
    response = requests.get(f"{api_url}{query_param}")

    #? Parsing
    data = response.json()

    #? Formatting the time.
    for observation in data: #? Retrieve the observation time by looping in the data.
        observation_time = observation.get("observationtime", '')
        
        #? Validation if there's any data 
        if observation_time:
            try:
                #? Format it
                #? The structure is by default is %Y-%m-%dT%H:%M:%S.%f
                #? I'm converting it with spaces "%b %d, %Y %I:%M %p"
                observation['formatted_time'] = datetime.strptime(
                    observation_time, "%Y-%m-%dT%H:%M:%S.%f"
                ).strftime("%b %d, %Y %I:%M %p")
            
            #? If data is invalid which would be the API's fault.
            except ValueError:
                observation['formatted_time'] = "Invalid Date"
    
    result_data = []
    no_data_message = None
    #? Making the search query diverse
    if search_query:

        #? Process the search_query
        query_param += f"&$where=locationname LIKE '%{search_query}%'"

        for observation in data:
            location_name = observation.get('locationname', '').lower()

            # Check if the location name contains the search query
            if search_query in location_name:
                result_data.append(observation)
            
        # #? Splitting the query into keywords if there are spaces
        # search_terms = search_query.split()

        # #? Filtration of data based on location name if there is a match
        # for observation in data: #? for each data
        #     location_name = observation.get('locationname', '').lower()

        #     #? Check each keyword are found in the location name
        #     if any(term in location_name for term in search_terms):
        #         result_data.append(observation)

        # #? If there are no data available on the search query
        if not result_data:
            no_data_message = "No Data Available"

    else: #? If there are no data the show all
        result_data = data   

    context = {
        'air_quality_data': result_data,
        'limit' : limit,
        'search_query': search_query,
        'no_data_message': no_data_message,
    }
    
    return render(request, 'core/index.html', context)