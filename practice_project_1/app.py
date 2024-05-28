from flask import Flask, jsonify
from data import country_data

app = Flask(__name__)

@app.route('/',methods=['GET'])
def hello():
    return 'Hello World!'

@app.route('/hello_world_post',methods=['POST'])
def hello_world_post():
    return 'Hello World!'
@app.route('/example/country_data',methods=['GET'])
def exaple_country_data
    return jsonify(country_data)


if __name__ == '__main__':
    app.run()
