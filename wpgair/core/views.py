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




def index(request):
    #? Defining the API endpoint
    api_url = "https://data.winnipeg.ca/resource/f58p-2ju3.json"

    #? Implementing a limit and the default as 10
    limit = int(request.GET.get('limit', 5))

    #? Base query parameters
    query_param = f"?$limit={limit}"

    #? Creating a search query and stripping it into keywords
    search_query = request.GET.get('search', '').lower().strip()

    #? Add search query to API call if it exists
    if search_query:
        query_param += f"&$q={search_query}"

    #? Fetch data from the API
    response = requests.get(f"{api_url}{query_param}")
    data = response.json()

    # if search_query:
    #     data = [observation for observation in data if search_query in observation.get("locationname", "").lower()]

    # result_data = data[:limit]
    
    #? If no data is returned
    no_data_message = None
    if not data:
        no_data_message = "No Data Available!"

    #? Invoke the function to format the time
    time_format(data)

    #? Context variables are defined here (right side variables) 
    #? and would be forwarded to the frontend (left side variables)
    context = {
        'air_quality_data': data,
        'limit': limit,
        'search_query': search_query,
        'no_data_message': no_data_message,
    }

    return render(request, 'core/index.html', context)

#  This code below works like a charm but optimize it.

# # View: Index
# def index(request):
#     # Define the API endpoint
#     api_url = "https://data.winnipeg.ca/resource/f58p-2ju3.json"

#     # Get the desired display limit and default to 5
#     limit = int(request.GET.get('limit', 5))

#     # Get search query and strip whitespace
#     search_query = request.GET.get('search', '').lower().strip()

#     # Fetch all data from the API (no limit in the API query)
#     response = requests.get(api_url)
#     data = response.json()

#     # Format observation times
#     time_format(data)

#     # Perform local filtering for partial matches (case-insensitive)
#     if search_query:
#         filtered_data = []  # Initialize an empty list for matched observations
#         for observation in data:
#             # Retrieve the location name and convert to lowercase
#             location_name = observation.get("locationname", "").lower()

#             # Check if the search query is in the location name
#             if search_query in location_name:
#                 filtered_data.append(observation)  # Add matching observation to the list

#         # Assign the filtered data back to the main data variable
#         data = filtered_data

#     # Apply the limit after filtering
#     result_data = data[:limit]

#     # Handle "No Data" message
#     no_data_message = None
#     if not result_data:
#         no_data_message = "No Data Available!"

#     # Context variables for the template
#     context = {
#         'air_quality_data': result_data,
#         'limit': limit,
#         'search_query': search_query,
#         'no_data_message': no_data_message,
#     }

#     return render(request, 'core/index.html', context)