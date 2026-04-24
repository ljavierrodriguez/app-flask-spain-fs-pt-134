from flask import Blueprint, jsonify, request
from models import User

api = Blueprint('api', __name__)

# Listar Usuarios
@api.route('/users', methods=['GET'])
def list_users():
    users = User.query.all() # SELECT * FROM users; # [<User 1>, <User 2>] 
    users = [user.to_dict() for user in users]
    return jsonify({ "users": users }), 200
    
# Crear Usuario
@api.route('/users', methods=['POST'])
def add_user():
    
    name = request.json.get('name', "")
    email = request.json.get('email')
    password = request.json.get('password')
    active = request.json.get('active', True)
    
    if not email:
        return jsonify({ "msg": "Email is required!"}), 400
    if not password:
        return jsonify({ "msg": "Password is required!"}), 400
    
    found = User.query.filter_by(email=email).first()
    
    if found:
        return jsonify({ "msg": "Email is already in use"}), 400
    
    """
    user = User()
    user.name = name
    user.email = email
    user.password = password
    """
    user = User(name=name, email=email, password=password, active=active)
    user.save()
    
    if user:
        return jsonify({ "status": "success", "data": user.to_dict(), "msg": "User created successfully"}), 200
    else:
        return jsonify({ "status": "fail", "data": None, "msg": "Error, please try again"}), 500
    
    

# Actualizar Usuario
@api.route('/users/<int:id>', methods=['PUT'])
def edit_user(id):
    name = request.json.get('name', "")
    email = request.json.get('email')
    password = request.json.get('password')
    active = request.json.get('active', True)
    
    if not email:
        return jsonify({ "msg": "Email is required!"}), 400
    if not password:
        return jsonify({ "msg": "Password is required!"}), 400
    
    found = User.query.filter(User.email==email, User.id!=id).first()
    
    if found:
        return jsonify({ "msg": "Email is already in use"}), 400
    
    user = User.query.get(id)    
    
    if not user:
        return jsonify({ "msg": "User not found!"}), 404
    
    user.name = name
    user.email = email
    user.password = password
    user.active = active
    
    user.update()
    
    if user:
        return jsonify({ "status": "success", "data": user.to_dict(), "msg": "User updated successfully"}), 200
    else:
        return jsonify({ "status": "fail", "data": None, "msg": "Error, please try again"}), 500

# Eliminar Usuario
@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    
    user = User.query.get(id)    
    
    if not user:
        return jsonify({ "msg": "User not found!"}), 404
    
    user.delete()
    
    return jsonify({ "status": "success", "data": None, "msg": "User deleted successfully"}), 200