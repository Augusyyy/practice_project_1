from flask import Flask, jsonify
from data import country_data

app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello():
    return 'Hello World!'


@app.route('/',methods=['POST'])
def hello_world_post():
    return 'Hello World!'


@app.route('/example/country_data',methods=['GET'])
def example_country_data():
    return jsonify(country_data)

@app.route('/example/cities',methods=['GET'])
def example_cities():
    cities = list(country_data.keys())
    return jsonify(cities)



if __name__ == '__main__':
    app.run()
