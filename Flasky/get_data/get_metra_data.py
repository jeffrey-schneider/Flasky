import os
import pandas as pd
import requests
from requests.auth import HTTPBasicAuth
from get_data import read_credentials
from markupsafe import Markup



dir_path = os.path.dirname(os.path.realpath(__file__))

file_name = "creds.txt"
file_path = dir_path + "/" + file_name


def main():
    #json = get_position_json("stops")
    #print(f"{json = }")
    #print(f"{json_to_table(json)}")
    get_stops_times("stops_times")



def get_json(credentials, report_type=None):
    if not report_type:
        rpt = 'url_positions'
    else:
        rpt = 'url_' + report_type

    # Replace with your actual URL
    response = ""
    url = credentials.get(rpt)
    username = credentials.get('username')
    password = credentials.get('password')

    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        # Make the GET request with basic authentication
        response.raise_for_status()  # Raise an error for bad status codes

        # Print the response content for debugging
        # print("Response Content:", response.content)
        data = response.json()
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Handle HTTP errors
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occurred: {req_err}')  # Handle general requests errors
    except ValueError as json_err:
        print(f'JSON decoding failed: {json_err}')  # Handle JSON decoding errors
        print("Response Text:", response.text)  # Print the response text for debugging



def get_json_single_trip(trip_id=None):
    credentials = {}
    credentials = read_credentials(file_path)
    if trip_id:
        url = f"https://gtfsapi.metrarail.com/gtfs/schedule/stop_times/{trip_id}"
    else:
        url = "https://gtfsapi.metrarail.com/gtfs/schedule/stop_times"
    # Replace with your actual URL
    response = ""
    username = credentials.get('username')
    password = credentials.get('password')

    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        # Make the GET request with basic authentication
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Handle HTTP errors
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occurred: {req_err}')  # Handle general requests errors
    except ValueError as json_err:
        print(f'JSON decoding failed: {json_err}')  # Handle JSON decoding errors
        print("Response Text:", response.text)  # Print the response text for debugging

def get_json_single_stop(stop_id=None):
    credentials = read_credentials(file_path)
    url = "https://gtfsapi.metrarail.com/gtfs/schedule/stop_times"
    response = ""
    username = credentials.get('username')
    password = credentials.get('password')

    try:
        response = requests.get(url, auth=HTTPBasicAuth(username, password))
        # Make the GET request with basic authentication
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        return data

    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')  # Handle HTTP errors
    except requests.exceptions.RequestException as req_err:
        print(f'Request error occurred: {req_err}')  # Handle general requests errors
    except ValueError as json_err:
        print(f'JSON decoding failed: {json_err}')  # Handle JSON decoding errors
        print("Response Text:", response.text)  # Print the response text for debugging


def get_position_json(report_type=None):
    creds = {}
    creds = read_credentials(file_path)
    json = get_json(creds, report_type)
    res = []
    df = pd.json_normalize(json)
    for column in df.columns:
        li = df[column].tolist()
        res.append(li)
    return json_to_table(json)



def get_stops_times(trip_id = None):
    creds = read_credentials(file_path)
    if trip_id:
        json = get_json_single_trip(trip_id)
    else:
        json = get_json(creds, 'stops_times')
    df = pd.json_normalize(json)
    # Group by 'trip_id'
    grouped = df.groupby('trip_id')

    # Create a dictionary to store each group in HTML format
    tables = {}
    for trip_id, group in grouped:
        # Drop the 'trip_id' column for the table
        group = group.drop(columns=['trip_id'])
        # Convert group DataFrame to HTML table
        tables[trip_id] = group.to_html(index=False, escape=False)
    return tables

def get_stops_detail(stop_id = None):
    creds = read_credentials(file_path)
    if stop_id:
        json = get_json_single_stop(stop_id)
    else:
        json= get_json_single_stop('AURORA')
    df = pd.json_normalize(json)
    # Group by 'stop_id'
    grouped = df.groupby('stop_id')
    tables={}
    for stop_id, group in grouped:
        group = group.drop(columns=['stop_id'])
        tables[stop_id] = group.to_html(index=False, escape=False)
    return tables


def json_to_table(json) -> str:
    link_text_pre = '<a href="/api/data/stops_times/'
    link_text_middle = '">'
    link_text_post = '</a>'
    for item in json:
        if 'trip_id' in item:
            stuff = link_text_pre + item['trip_id'] + link_text_middle + item['trip_id'] + link_text_post
            the_text = stuff
            item['stop_link'] = the_text
        if 'trip_id' in item.get('vehicle',{}).get('trip',{}):
            stuff = f"{item.get('vehicle',{}).get('trip',{})['trip_id']}"
            the_text = link_text_pre + stuff + link_text_middle + stuff + link_text_post
            item['stop_link'] = the_text

    df = pd.json_normalize(json, max_level=2)
    ret_val = df.to_html(classes='dataframe',border=1, index=False, table_id="table_id", render_links=True, escape=False)
    return ret_val







if __name__ == '__main__':
    main()