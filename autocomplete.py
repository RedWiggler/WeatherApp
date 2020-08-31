"""
    Autocomplete Cities and Locations Using the Google Places API
    Using google place API to create autocomplete bar for searching locations by the client
"""
from requests_html import HTMLSession
import requests


API_key = ""

def get_autocomplete_list(input):
    """
    Using google place API to create predictions list based on the input the client insert to the search box
    :param input: The input the client insert to the search box
    :return: list of predictions for locations based on the input
    """
    url = f"https://maps.googleapis.com/maps/api/place/autocomplete/json?input={input}&types=(cities)&language=pt_BR&key={API_key}"
    prediction_list = []
    try:
        r = requests.get(url)
        for city in r.json()["predictions"]:
            prediction_list.append(city["structured_formatting"]["main_text"])

    except requests.exceptions.RequestException as e:
        print(e)
    return prediction_list


if __name__ == "__main__":
    print(get_autocomplete_list("n"))
