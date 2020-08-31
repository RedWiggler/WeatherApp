"""
    Web scrapping weather data from google
"""
from requests_html import HTMLSession, AsyncHTMLSession
import requests
from bs4 import BeautifulSoup as bs


def get_weather_data_from_url(response):
    """
    Parsing the web page for weather data
    :param response: The response from google web page (of getting request)
    :return: loc_data - A dictionary object containing the weather data
    """
    try:
        loc_data = dict()
        loc_data['name'] = response.html.find("#wob_loc", first=True).text
        loc_data['time'] = response.html.find("#wob_dts", first=True).text
        loc_data['temp'] = response.html.find("#wob_tm", first=True).text
        loc_data['humidity'] = response.html.find("#wob_hm", first=True).text
        loc_data['wind'] = response.html.find("#wob_ws", first=True).text
        loc_data['icon'] = response.html.find("#wob_tci", first=True).attrs['src']
        loc_data['icon_alt'] = response.html.find("#wob_tci", first=True).attrs['alt']
    except:
        loc_data = None
        print("An exception occurred with getting the location weather data")
    return loc_data


def getweather(url):
    """
    Getting the web page from the url
    :param url: The desired web page url
    :return: loc_data: A dictionary object containing the weather data from the web page url
    """
    try:
        session = HTMLSession(mock_browser=True)
        response = session.get(url)
        print(response)
        loc_data = get_weather_data_from_url(response)
    except requests.exceptions.RequestException as e:
        loc_data = None
        print(e)
    return loc_data


def getnearbyweathers(url_list, weather_data):
    """
    Getting the weathers in multiple locations async - reducing delay time
    :param url_list: List of urls to get the weather data from
    :return: weather_data: List of dictionary objects containing the weather data
    """
    asession = AsyncHTMLSession()

    async def get_weaather1():
        r = await asession.get(url_list[0])

    async def get_weaather2():
        r = await asession.get(url_list[1])

    async def get_weaather3():
        r = await asession.get(url_list[2])

    responses = asession.run(get_weaather1(), get_weaather2(), get_weaather3())
    print(responses)
    for response in responses:
        weather_data.append(get_weather_data_from_url(response))

    return weather_data



def nearbyweather():
    """
    This function get the weather data for locations around the client
    :return: weather_data: List of dictionary objects containing the weather data
    """
    url = "https://www.google.com/search?q=weather+near+me&hl=en&gl=en"
    weather_data = [getweather(url)]
    mylocation = weather_data[0]['name']
    url_list = []
    for location in nearbyplaces(mylocation)[:2]:
        location = location.replace(' ', '+').replace('-', '+')
        url = f"https://www.google.com/search?q=weather+in+{location}&hl=en&gl=en"
        url_list.append(url)
        weather_data.append(getweather(url))

    # return getnearbyweathers(url_list, weather_data)
    return weather_data



def nearbyplaces(location):
    """
    The function getting a location and return a list of locations/cities around it
    :param location: name of a location/city
    :return: nearby_list: list of nearby locations/cities
    """
    location = location.replace(' ', '+').replace('-', '+')
    url = f"https://www.travelmath.com/cities-near/{location}"
    try:
        session = HTMLSession(mock_browser=True)
        response = session.get(url)
        print(response)
        try:
            nearby_list = (response.html.find("table", first=True).text).split('\n')
        except:
            print("An exception occurred while searching nearby locations")

    except requests.exceptions.RequestException as e:
        print(e)
    return nearby_list


def locationweather(location):
    """
    The function getting a location from the client and calling the getweather function
    :param location: the desired location for getting weather data
    :return: A dictionary object containing the weather data for this location
    """
    location = location.replace(' ', '+').replace('-', '+')
    url = f"https://www.google.com/search?q=weather+in+{location}&hl=en&gl=en"
    return getweather(url)


if __name__ == "__main__":
    print(locationweather('London')["temp"])
    # print(nearbyplaces('Netanya'))
    # print(nearbyweather())