"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

# create the jackson family object
jackson_family = FamilyStructure("Jackson")

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

# GET /members: Retorna todos los miembros de la familia
@app.route('/members', methods=['GET'])
def get_members():
    members = jackson_family.get_all_members()
    return jsonify(members), 200

# GET /member/<int:member_id>: Retorna el miembro con el id indicado
@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    member = jackson_family.get_member(member_id)
    if member is None:
        return jsonify({"error": "Member not found"}), 404
    return jsonify(member), 200

# POST /member: Agrega un nuevo miembro a la familia
@app.route('/member', methods=['POST'])
def add_member():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Bad request, no data provided"}), 400
    jackson_family.add_member(data)
    return jsonify({"done": True}), 200

# DELETE /member/<int:member_id>: Elimina el miembro con el id indicado
@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    success = jackson_family.delete_member(member_id)
    if not success:
        return jsonify({"error": "Member not found"}), 404
    return jsonify({"done": True}), 200

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
