import http.server
import socketserver
import coffee_3
import os
from flask import Flask, request, render_template, jsonify 

'''
from flaskext.mysql import MySQL
'''
app = Flask(__name__)

'''
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = '1234'
app.config['MYSQL_DATABASE_DB'] = 'cafedata'  #DB중 cafedata에 접근
app.config['MYSQL_DATABASE_HOST'] = os.getenv('DBHOST', 'localhost')
mysql.init_app(app)
'''

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods = ['POST'])
def getCafe():
    try:
        lat = request.get_data().decode().split('&')[0][4:]
        lon = request.get_data().decode().split('&')[1][4:]

        if lat and lon:
            return jsonify(coffee_3.americano(lat, lon))
        else:
            return jsonify("No data")
    except:
        return jsonify("No data")


if __name__ == "__main__":
    app.run(debug = True)
