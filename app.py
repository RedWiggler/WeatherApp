"""
    Web page displaying the following:
        1.Current weather data for two cities or more.
        2.An input field to allow the user to search any location.
"""

from flask import Flask, render_template, request
from getforecast import locationweather, nearbyweather
from autocomplete import get_autocomplete_list

app = Flask(__name__)


@app.route('/')
@app.route("/home", methods=["POST", "GET"])
def home():
    weather_data = nearbyweather()
    return render_template('home.html', weather_data=weather_data)


@app.route("/weather", methods=["POST", "GET"])
def weather():
    location = request.form.get("location")
    if not location:
        return render_template('fail.html', title="Failure", location=location)
    loc_data = locationweather(location)
    if loc_data:
        return render_template('weather.html', title=location, loc_data=loc_data)
    else:
        return render_template('fail.html', title="Failure", location=location)


@app.route("/autocomplete")
def autocomplete():
    # input = request.args.get('input')
    # prediction_list = get_autocomplete_list(input)
    return render_template('autoco.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0")
