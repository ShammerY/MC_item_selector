from flask import Blueprint, request, jsonify, render_template, redirect, g
from models import db, Item

routes = Blueprint('routes', __name__)

@routes.route('/')
def welcome():
    return render_template('index.html')

@routes.route('/item_category')
def item_category_selection():
    return render_template('item_category.html')

@routes.route('/very_easy_list',methods=['GET'])
def very_easy_list():
    items = Item.query.filter_by(category="very easy").all()
    return render_template('very_easy_list.html',items=items)

@routes.route('/easy_list',methods=['GET'])
def easy_list():
    items = Item.query.filter_by(category="easy").all()
    return render_template('very_easy_list.html',items=items)

@routes.route('/normal_list',methods=['GET'])
def normal_list():
    items = Item.query.filter_by(category="normal").all()
    return render_template('very_easy_list.html',items=items)

@routes.route('/hard_list',methods=['GET'])
def hard_list():
    items = Item.query.filter_by(category="hard").all()
    return render_template('very_easy_list.html',items=items)

@routes.route('/items',methods=['POST'])
def create_item():
    

    #Obtener datos enviados con formato Json
    # data = request.get_json()

    # name = data.get('name')
    # category = data.get('category')

    #Obtener datos cuando se envian por un formulario
    name = request.form.get('name')
    category = request.form.get('category')

    if not all([name, category]):
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    new_item = Item(name=name,category=category)

    db.session.add(new_item)
    db.session.commit()

    return redirect('/')

@routes.route('/register_item',methods=['GET'])
def register_item_open():
    return render_template('register_item.html')

@routes.route('/items',methods=['GET'])
def get_items():
    items = Item.query.all()
    items_list = [{'id': item.id, 'name': item.name, 'category':item.category} for item in items]
    return jsonify(items_list), 200


@routes.route('/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item no encontrado'}), 404
    
    return jsonify({'id': item.id, 'name': item.name}), 200

@routes.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item no encontrado'}), 404
    
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Se requiere un nombre'}), 400

    item.name = data['name']
    item.category = data['category']
    db.session.commit()
    
    return jsonify({'message': 'Item actualizado', 'item': {'id': item.id, 'name': item.name,'category': item.category}}), 200

@routes.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item no encontrado'}), 404
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': 'Item eliminado'}), 200