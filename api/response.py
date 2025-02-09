from flask import jsonify, make_response

def success(values, message):
    res = {
        'data' : values,
        'message' : message
    }
    return make_response(jsonify(res)),200
    
def BadRequest(values, message):
    res = {
        'data' : values,
        'message' : message
    }
    return make_response(jsonify(res)),400

def error(data, message):
    return make_response(jsonify({"data": data, "message": message}), 400)