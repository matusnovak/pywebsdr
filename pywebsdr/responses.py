from flask import jsonify

def ok(body):
    response = jsonify(body)
    response.status_code = 200
    return response

def badRequest(message):
    response = jsonify({'message': message})
    response.status_code = 200
    return response