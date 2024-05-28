from flask import Flask, jsonify
from data import country_data
from model.city import City
from data import place_data
from data import amenity_data
from data import place_to_amenity_data


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
    cities_list.append(City("Gotham",0).__dict__)
    cities_list.append(City("Metropolis", 1).__dict__)
    cities_list.append(City("#$%^&**", 2).__dict__)
    cities_list.append(City("Duckburg", 3).__dict__)
    return cities_list


@app.route('/example/places_amenities_raw', methods=['GET'])
def example_places_amenities_raw():
    return jsonify(place_to_amenity_data)



if __name__ == '__main__':
    app.run()
