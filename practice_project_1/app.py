from flask import Flask, jsonify
from data import country_data
from model.city import City
from data import place_data
from data import amenity_data
from data import place_to_amenity_data
from data import user_data
from data import review_data


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


@app.route('/example/places_amenities_prettified_example', methods=['GET'])
def example_places_amenities_prettified():
    place_list = place_data['Place']
    amenity_list = amenity_data['Amenity']
    place_to_amenity_list = place_to_amenity_data['Place_to_Amenity']

    output = {}
    data = []

    for place_to_amenity_item in place_to_amenity_list:

        place_id = place_to_amenity_item["place_id"]
        amenity_id = place_to_amenity_item["amenity_id"]

        sub_out_put = {}

        for amenity_item in amenity_list:
            if amenity_item['id'] == amenity_id:
                sub_out_put['amenity'] = amenity_item

        for place_item in place_list:
            if place_item['id'] == place_id:
                sub_out_put['place'] = place_item

        data.append(sub_out_put)
    output['data'] = data
    return jsonify(output)

@app.route('/example/places_reviews', methods=['GET'])
def example_places_reviews():
    review_list = review_data['Review']
    place_list = place_data['Place']
    user_list = user_data['User']

    en_reviews = []

    for review_item in review_list:

        place_id = review_item["place_id"]
        user_id = review_item["commentor_user_id"]

        for place_item in place_list:
            if place_item['id'] == place_id:
                review_item['place'] = place_item

        for user_item in user_list:
            if user_item['id'] == user_id:
                review_item['user'] = user_item

    return jsonify(review_data)


if __name__ == '__main__':
    app.run()
