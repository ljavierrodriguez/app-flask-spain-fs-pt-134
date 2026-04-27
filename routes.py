from datetime import timedelta
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import check_password_hash
from models import User

api = Blueprint('api', __name__)


@api.route('/register', methods=['POST'])
def register(): 
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
    
    user = User(name=name, email=email, active=active)
    user.hash_password(password)
    user.save()
    
    if user:
        return jsonify({ "status": "success", "msg": "User registed, please login!"}), 200
    else:
        return jsonify({ "status": "fail", "data": None, "msg": "Error, please try again"}), 500
    

@api.route('/login', methods=['POST'])
def login():
    
    email = request.json.get('email')
    password = request.json.get('password')
    
    if not email:
        return jsonify({ "msg": "Email is required!"}), 400
    if not password:
        return jsonify({ "msg": "Password is required!"}), 400
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        return jsonify({ "status": "fail", "msg": "Credenciales Inválidas"}), 401
    
    if not check_password_hash(user.password, password):
        return jsonify({ "status": "fail", "msg": "Credenciales Inválidas"}), 401
    
    expired_token = timedelta(days=1)
    
    access_token = create_access_token(identity=str(user.id), additional_claims={
        "role": "admin",
        "email": user.email
    }, expires_delta=expired_token)
    
    return jsonify({ "access_token": access_token }), 200
    
@api.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    
    id = get_jwt_identity()
    user = User.query.get(id)
    
    return jsonify({ "profile": user.to_dict() }), 200
     

# Listar Usuarios
@api.route('/users', methods=['GET'])
@jwt_required()
def list_users():
    users = User.query.all() # SELECT * FROM users; # [<User 1>, <User 2>] 
    users = [user.to_dict() for user in users]
    return jsonify({ "users": users }), 200
    
# Crear Usuario
@api.route('/users', methods=['POST'])
@jwt_required()
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
@jwt_required()
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
@jwt_required()
def delete_user(id):
    
    user = User.query.get(id)    
    
    if not user:
        return jsonify({ "msg": "User not found!"}), 404
    
    user.delete()
    
    return jsonify({ "status": "success", "data": None, "msg": "User deleted successfully"}), 200

"""
@api.route('/update', methods=['GET'])
def update_users():
    
    users = User.query.all()
    for user in users:
        user.hash_password(user.password)
        user.update()
        
    return jsonify({ "msg": "Users updated!"}), 200
"""