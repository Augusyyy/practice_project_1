from flask import Flask, jsonify
from data import country_data
from model.city import City


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
    cities_list = []
    cities_list.append("Gotham",0).__dict__)
    cities_list.append("Metropolis", 1).__dict__)
    cities_list.append("#$%^&**", 2).__dict__)
    cities_list.append("Duckburg", 3).__dict__)
    return cities_list



if __name__ == '__main__':
    app.run()
