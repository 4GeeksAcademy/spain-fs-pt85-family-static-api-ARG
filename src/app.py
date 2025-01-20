import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


jackson_family = FamilyStructure("Jackson")


@app.route('/members', methods=['GET'])
def get_members():
    try:
        members = jackson_family.get_all_members()
        return jsonify(members), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    try:
        # Verificar si el ID es válido
        if not isinstance(member_id, int) or member_id < 0:
            return jsonify({"error": "Invalid member ID"}), 400
        
        member = jackson_family.get_member(member_id)
        if not member:
            return jsonify({"error": "Member not found"}), 400
        return jsonify(member), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Endpoint para agregar un nuevo miembro
@app.route('/member', methods=['POST'])
def add_member():
    #validacion de miebros
    try:
        member_data = request.get_json()
        if not member_data or not all(key in member_data for key in ["first_name", "age", "lucky_numbers"]):
            return jsonify({"error": "Invalid request body"}), 400
        if not isinstance(member_data['age'], int) or member_data['age'] < 0:
            return jsonify({"error": "Age must be a positive integer"}), 400
        if not isinstance(member_data['lucky_numbers'], list) or not all(isinstance(num, int) for num in member_data['lucky_numbers']):
            return jsonify({"error": "Lucky numbers must be a list of integers"}), 400
        
        jackson_family.add_member(member_data)
        return jsonify({"message": "Member added successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    try:
        # Validar si el ID es válido
        if not isinstance(member_id, int) or member_id < 0:
            return jsonify({"error": "Invalid member ID"}), 400

        member = jackson_family.get_member(member_id)
        if not member:
            return jsonify({"error": "Member not found"}), 400
        jackson_family.delete_member(member_id)
        return jsonify({"done": True}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)