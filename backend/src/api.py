import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)


db_drop_and_create_all()

## ROUTES

@app.route('/drinks')
def get_drinks():
    drinks = Drink.query.all()
    short_drinks = [drink.short() for drink in drinks]

    return jsonify({
        'status_code': 200,
        'sucsess': True,
        'drinks': short_drinks
    })


@app.route('/drinks-detail')
@requires_auth('get:drinks-detail')
def get_drinks_detailed(jwt):
    drinks = Drink.query.all()
    long_drinks = [drink.long() for drink in drinks]
    return jsonify({
        'status_code': 200,
        'sucsess': True,
        'drinks': long_drinks
    })

@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def create_drink(jwt):
    request_value = request.get_json()

    if request_value is None:
        abort(400)

    if request_value['title'] is None or request_value['recipe'] is None:
        abort(400)

    drink = Drink(
        title=request_value['title'],
        recipe=json.dumps(request_value['recipe'])
    )
    try: 
        Drink.insert(drink)
        return jsonify({
            'success': True,
            'status_code': 200,
            'drinks': [drink.long()]
        })
    except:
        return jsonify({
            'success': False,
            'status_code': 400,
            'message': 'There was a problem saving this drink. Please try again with another drink name.'
        })



@app.route('/drinks/<int:drink_id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def update_drinks(jwt, drink_id):
    data = request.get_json()
    if data['title'] is None or data['recipe'] is None:
        abort(400)

    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()
    
    if drink is None:
        abort(404)
    
    drink.title = data['title']
    drink.recipe = json.dumps(data['recipe'])
    try:
        drink.update()
        return jsonify({
            'status_code': 200,
            'success': True,
            'drinks': [drink.long()]
        })
    except:
        return jsonify({
            'success': False,
            'status_code': 400,
            'message': 'There was a problem updating this drink. Please try again with another drink name.'
        })


@app.route('/drinks/<int:drink_id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(jwt, drink_id):
    drink = Drink.query.filter(Drink.id == drink_id).one_or_none()

    if drink is None:
        abort(404)
    
    drink.delete()
    return jsonify({
        'status_code': 200,
        'success': True,
        'delete': drink.id
    })


## Error Handling
'''
Example error handling for unprocessable entity
'''
@app.errorhandler(400)
def bad_request(error):
    return jsonify({
                    "success": False, 
                    "error": 400,
                    "message": "bad request"
                    }), 400

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
                    "success": False, 
                    "error": 422,
                    "message": "unprocessable"
                    }), 422

@app.errorhandler(404)
def not_found(error):
    return jsonify({
                    "success": False, 
                    "error": 404,
                    "message": "Not found."
                    }), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({
                    "success": False, 
                    "error": 500,
                    "message": "Sorry, we couldn't handle your request."
                    }), 500


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
                    "success": False, 
                    "error": error.status_code,
                    "message": error.error['description']
                    }), error.status_code