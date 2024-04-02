from flask import request, jsonify
from flask.views import MethodView
from uuid import uuid4
from flask_smorest import abort
from flask_jwt_extended import create_access_token, unset_jwt_cookies
from schemas import CarSchema, CarWithSaleReceiptSchema
from . import bp
from db import cars
from models.car_model import CarModel

@bp.route('/car', methods=['GET', 'POST'])
class CarList(MethodView):
    
    @bp.response(200, CarWithSaleReceiptSchema(many=True))
    def get(self):
        return CarModel.query.all()
    

    @bp.arguments(CarSchema)
    @bp.response(201, CarSchema)
    def post(self, data):
        try:
            car = CarModel()
            car.from_dict(data)
            car.save_car()
            return car
        except:
            abort(400, message='Forgot to add make and model!')
 

@bp.route('/car/<int:id>', methods=['GET', 'PUT', 'DELETE'])
class Car(MethodView):
    
    @bp.response(200, CarWithSaleReceiptSchema)
    def get(self, id):
        car = CarModel.query.get(id)
        if car:
            return car
        else:
            abort(400, message='Invalid car id')

    @bp.arguments(CarSchema)
    @bp.response(200, CarWithSaleReceiptSchema)
    def put(self, data, id):
        car = CarModel.query.get(id)
        if car:
            car.from_dict(data)
            car.save_car()
            return car
        else:
            abort(400, message='Invalid car id')    

    def delete(self, id):
        car = CarModel.query.get(id)
        if car:
            car.del_car()
            return {'message': f'Car: {car.make} {car.model} deleted'}
        abort(400, message='Invalid car id')    


@bp.route('/login', methods=['POST'])
def login():
    login_data = request.get_json()
    username = login_data['username']

    user = CarModel.query.filter_by(username=username).first()
    if user and user.check_password(login_data['password']):
        access_token = create_access_token(identity=user.id)
        return {'access_token': access_token}, 201

    abort(400, message="Invalid User Data")

@bp.route('/logout', methods=['POST'])
def logout():
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response
