from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Car, car_schema, cars_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
@token_required
def getdata():
    return { 'some': 'value'}


# CREATE CAR ENDPOINT
@api.route('/cars', methods = ['POST'])
@token_required
def create_car(current_user_token):
    nickname = request.json['nickname']
    make = request.json['make']
    model = request.json['model']
    year = request.json['year']
    engine = request.json['engine']
    original_price = request.json['original_price']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    car = Car(nickname, make, model, year, engine, original_price, user_token = user_token )

    db.session.add(car)
    db.session.commit()

    response =car_schema.dump(car)
    return jsonify(response)


# RETRIEVE ALL CARS ENDPOINT
@api.route('/cars', methods = ['GET'])
@token_required
def get_cars(current_user_token):
    owner = current_user_token.token
    cars = Car.query.filter_by(user_token = owner).all()
    response = cars_schema.dump(cars)
    return jsonify(response)


# RETRIEVE ONE CAR ENDPOINT
@api.route('/cars/<id>', methods = ['GET'])
@token_required
def get_car(current_user_token, id):
    owner = current_user_token.token
    if owner == current_user_token.token:
        car = Car.query.get(id)
        response = car_schema.dump(car)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401



# UPDATE CAR ENDPOINT
@api.route('/cars/<id>', methods = ['POST','PUT'])
@token_required
def update_car(current_user_token,id):
    car = Car.query.get(id) # GET CAR INSTANCE

    car.nickname = request.json['nickname']
    car.make = request.json['make']
    car.model = request.json['model']
    car.year = request.json['year']
    car.engine = request.json['engine']
    car.original_price = request.json['original_price']
    car.user_token = current_user_token.token

    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)


# DELETE CAR ENDPOINT
@api.route('/cars/<id>', methods = ['DELETE'])
@token_required
def delete_car(current_user_token, id):
    car = Car.query.get(id)
    db.session.delete(car)
    db.session.commit()
    response = car_schema.dump(car)
    return jsonify(response)
