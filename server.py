import requests
#import os
from flask import Flask, render_template

#API_KEY = os.environ.get("API_KEY", "6cc0b26070b46dc183d2596c28caf9f6")
API_KEY = "6cc0b26070b46dc183d2596c28caf9f6"
BASE_URL = "https://api.openweathermap.org/data/2.5"
CITY = "New York"
LAT = 41.2924
LON = 174.7787

app = Flask(__name__, static_url_path="", static_folder="web/static", template_folder="web/templates")

@app.route('/')
def hello_world():
    return render_template('index.html', message="Hello World!")

@app.route('/current')
def current():
    try:
        r = requests.get(f"{BASE_URL}/weather?q={CITY}&appid={API_KEY}")
        r.raise_for_status()
        data = r.json()
        #return r.json()

        current_weather ={
            "description": data["weather"][0]["description"].title(),
            "icon": data["weather"][0]["icon"],
            "name": data["name"],
            "temperature": '{:.2f}'.format(round((data["main"]["temp"] - 273.15), 2)),
            "wind": data['wind']['speed']
        }

        return render_template("index.html", weather=current_weather)
    except requests.exceptions.ConnectionError as err:
        return f"Error: {err}"
    except requests.exceptions.HTTPError as err:
        return f"Error: {err}"

@app.route('/forecast')
def forecast():
    r = requests.get(f"{BASE_URL}/onecall?lat={LAT}&lon={LON}&appid={API_KEY}").json()
    return render_template("index.html", forecast=r['daily'])

@app.errorhandler(404)
def page_not_found(error):
    return render_template('index.html', message=error), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)