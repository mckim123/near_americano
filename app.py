import coffee_3
from flask import Flask, request, render_template, jsonify 

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods = ['POST'])
def getCafe():
    try:
        latlng = request.get_json()
        lat = str(latlng['lat'])
        lon = str(latlng['lon'])
        if latlng:
            return jsonify(coffee_3.americano(lat, lon))
        else:
            return jsonify("No data")
    except:
        return jsonify("No data")


if __name__ == "__main__":
    app.run(debug = True)
