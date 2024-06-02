import json
import uuid
from datetime import datetime
from flask import Flask, jsonify, request, Response
from data import country_data
from model.city import City
from data import place_data
from data import amenity_data
from data import place_to_amenity_data
from data import user_data
from data import review_data
from model.user import User
from model.country import Country
from data import city_data

app = Flask(__name__)


@app.route('/', methods=['GET'])
def hello():
    return 'Hello World!'


@app.route('/', methods=['POST'])
def hello_world_post():
    return 'Hello World!'


@app.route('/example/country_data', methods=['GET'])
def example_country_data():
    return jsonify(country_data)


@app.route('/example/cities', methods=['GET'])
def example_cities():
    cities_list = []
    cities_list.append(City("Gotham", 0).__dict__)
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


@app.route('/api/v1/users/<user_id>', methods=['GET'])
def users_specific_get(user_id):
    user_list = user_data['User']
    for user in user_list:
        if user['id'] == user_id:
            return jsonify(user)

    return "User not found"


@app.route('/api/v1/users', methods=['POST'])
def users_post():
    if not request.json:
        return jsonify({"message": "Missing JSON in request"})

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid JSON data"})
    if 'email' not in data:
        return jsonify({"error": "Missing email"})
    if 'password' not in data:
        return jsonify({"error": "Missing password"})

    email = data['email']
    password = data['password']
    first_name = data.get('first_name', '')
    last_name = data.get('last_name', '')

    new_user = User(email, password, first_name, last_name)

    user_data['User'].append({
        'id': new_user.id,
        'created_at': new_user.created_at.isoformat(),
        'updated_at': new_user.updated_at.isoformat(),
        'first_name': new_user.first_name,
        'last_name': new_user.last_name,
        'email': new_user.email,
        'password': new_user.password
    })

    return_data = {
        'id': new_user.id,
        'created_at': new_user.created_at.isoformat(),
        'updated_at': new_user.updated_at.isoformat(),
        'first_name': new_user.first_name,
        'last_name': new_user.last_name,
        'email': new_user.email
    }

    return jsonify(return_data)


@app.route('/api/v1/users_modify', methods=['POST'])
def users_modify():
    if not request.json:
        return jsonify({"message": "Missing JSON in request"})

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Invalid JSON data"})

    user_id = data['id']
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    password = data.get('password')

    for user in user_data['User']:
        if user['id'] == user_id:
            user_modify = user
            break

    if user_modify is None:
        return jsonify({"error": "User not found"})

    if first_name:
        user_modify['first_name'] = first_name
    if last_name:
        user_modify['last_name'] = last_name
    if email:
        user_modify['email'] = email
    if password:
        user_modify['password'] = password

    user_modify['updated_at'] = datetime.now().isoformat()

    return jsonify(user_modify)


@app.route('/api/v1/countries', methods=['POST'])
def countries_post():
    if not request.json:
        return jsonify({"message": "Missing JSON in request"})

    data = request.get_json()

    if data is None:
        return jsonify({"error": "Missing JSON data"})
    if 'name' not in data:
        return jsonify({"error": "Missing name"})
    if data['name'] is None:
        return jsonify({"error": "Missing name"})
    if 'code' not in data:
        return jsonify({"error": "Missing code"})

    name = data['name']
    code = data['code']

    new_country = Country(code, name)

    country_data['Country'].append({
        'id': new_country.id,
        'created_at': new_country.created_at.isoformat(),
        'updated_at': new_country.updated_at.isoformat(),
        'name': new_country.name,
        'code': new_country.code
    })

    return_data = {
        'id': new_country.id,
        'created_at': new_country.created_at.isoformat(),
        'updated_at': new_country.updated_at.isoformat(),
        'name': new_country.name,
        'code': new_country.code
    }

    return jsonify(return_data)


@app.route('/api/v1/countries', methods=['GET'])
def countries_get():
    countries_list = country_data['Country']
    return countries_list


@app.route('/api/v1/countries/<country_code>', methods=['GET'])
def countries_specific_get(country_code):
    country_to_return = None
    for country in country_data['Country']:
        if country['code'] == country_code:
            country_to_return = country
            break

    if country_to_return is None:
        return jsonify({"error": "Country not found"})

    return jsonify(country_to_return)


@app.route('/api/v1/countries/<country_code>/cities', methods=['GET'])
def countries_specific_cities_get(country_code):
    data = []
    wanted_country_id = ""

    country_data_list = country_data['Country']
    city_data_list = city_data['City']

    for item in country_data_list:
        if item['code'] == country_code:
            wanted_country_id = item['id']

    for item in city_data_list:
        if item['country_id'] == wanted_country_id:
            data.append({
                "city_id": item['id'],
                "name": item['name'],
                "country_id": item['country_id'],
                "created_at": datetime.fromtimestamp(item['created_at']).isoformat(),
                "updated_at": datetime.fromtimestamp(item['updated_at']).isoformat()
            })

    return json.dumps(data)


@app.route('/api/v1/countries/<country_code>/places', methods=['GET'])
def countries_specific_places_get(country_code):
    data = []
    wanted_country_id = ""
    city_ids = []

    country_data_list = country_data['Country']
    city_data_list = city_data['City']
    place_data_list = place_data['Place']

    for item in country_data_list:
        if item['code'] == country_code:
            wanted_country_id = item['id']

    for item in city_data_list:
        if item['country_id'] == wanted_country_id:
            city_ids.append(item['id'])

    for item in place_data_list:
        if item['city_id'] in city_ids:
            data.append({
                "place_id": item['id'],
                "name": item['name'],
                "city_id": item['city_id'],
                "created_at": datetime.fromtimestamp(item['created_at']).isoformat(),
                "updated_at": datetime.fromtimestamp(item['updated_at']).isoformat()
            })

    return json.dumps(data)


@app.route('/api/v1/cities_post', methods=['POST'])
def cities_post():

    if not request.json:
        return jsonify({"message": "Missing JSON in request"})

    data = request.get_json()

    if 'name' not in data:
        return jsonify({"error": "Missing name"})
    if 'country_id' not in data:
        return jsonify({"error": "Missing country_id"})

    name = data['name']
    country_id = data['country_id']

    cities_data_list = city_data['City']
    for item in cities_data_list:
        if item['name'] == name and item['country_id'] == country_id:
            return jsonify({"error": "City already exists"})

    new_city = City(name, country_id)
    city_data['City'].append({
        "id": new_city.id,
        "name": new_city.name,
        "country_id": new_city.country_id,
        "created_at": new_city.created_at,
        "updated_at": new_city.updated_at
        })

    return jsonify({
        "id": new_city.id,
        "name": new_city.name,
        "country_id": new_city.country_id,
        "created_at": new_city.created_at,
        "updated_at": new_city.updated_at
    })


@app.route('/api/v1/cities_get', methods=['GET'])
def cities_get():
    city_data_list = city_data['City']
    return jsonify(city_data_list)


@app.route('/api/v1/cities_del_post', methods=['POST'])
def cities_del_post():
    if not request.json:
        return jsonify({"message": "Missing JSON in request"})

    data = request.get_json()

    if 'city_id' not in data:
        return jsonify({"error": "Missing city_id"})

    city_id = data['city_id']

    city_data_list = city_data['City']
    city_del = None

    for i in range(len(city_data_list)):
        if city_data_list[i]['id'] == city_id:
            city_del = i
            break

    if city_del is None:
        return jsonify({"error": "City not found"})

    del city_data_list[city_del]

    return jsonify(city_del)


@app.route('/api/v1/cities_modify_post', methods=['POST'])
def cities_modify_post():
    if not request.json:
        return jsonify({"message": "Missing JSON in request"}), 400

    data = request.get_json()

    if 'id' not in data:
        return jsonify({"error": "Missing id"}), 400

    city_id = data['id']
    new_name = data.get('name')
    new_country_id = data.get('country_id')

    city_data_list = city_data['City']
    city_to_modify = None

    for city in city_data_list:
        if city['id'] == city_id:
            city_to_modify = city
            break

    if city_to_modify is None:
        return jsonify({"error": "City not found"}), 404

    if new_name:
        city_to_modify['name'] = new_name
    if new_country_id:
        city_to_modify['country_id'] = new_country_id

    city_to_modify['updated_at'] = datetime.now().timestamp()

    return jsonify(city_to_modify)



if __name__ == '__main__':
    app.run()
