from flask import Blueprint, request, jsonify, render_template, redirect, current_app
from models import db, Item
import os
from werkzeug.utils import secure_filename
import random

routes = Blueprint('routes', __name__)
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

@routes.route('/')
def welcome():
    return render_template('index.html')

@routes.route('/item_category')
def item_category_selection():
    return render_template('item_category.html')

@routes.route('/very_easy_list',methods=['GET'])
def very_easy_list():
    items = Item.query.filter_by(category="very easy").all()
    return render_template('item_list.html',items=items)

@routes.route('/easy_list',methods=['GET'])
def easy_list():
    items = Item.query.filter_by(category="easy").all()
    return render_template('item_list.html',items=items)

@routes.route('/normal_list',methods=['GET'])
def normal_list():
    items = Item.query.filter_by(category="normal").all()
    return render_template('item_list.html',items=items)

@routes.route('/hard_list',methods=['GET'])
def hard_list():
    items = Item.query.filter_by(category="hard").all()
    return render_template('item_list.html',items=items)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route('/items',methods=['POST'])
def create_item():
    #Obtener datos enviados con formato Json
    # data = request.get_json()

    # name = data.get('name')
    # category = data.get('category')

    #Obtener datos cuando se envian por un formulario
    name = request.form.get('name')
    category = request.form.get('category')
    # is_active = request.form.get('is_active') == "on"
    image = request.files["image"]

    if not all([name, category]):
        return jsonify({'error': 'Todos los campos son obligatorios'}), 400

    if image and allowed_file(image.filename):
        filename = secure_filename(image.filename)  # Asegura el nombre
        image_path = os.path.join(current_app.config["UPLOAD_FOLDER"], filename)
        image.save(image_path)  # Guarda la imagen en la carpeta de subida

        # Guarda la ruta relativa en la base de datos
        image_url = f'static/uploads/{filename}'
    else:
        return jsonify({'error': 'Imagen es obligatoria'}), 400

    
    new_item = Item(name=name, category=category, image_url=image_url, is_active=True)

    db.session.add(new_item)
    db.session.commit()

    return redirect('/item_category')

@routes.route('/register_item',methods=['GET'])
def register_item_open():
    return render_template('register_item.html')

@routes.route('/items',methods=['GET'])
def get_items():
    items = Item.query.all()
    items_list = [{'id': item.id, 'name': item.name, 'category':item.category, 'is_active':item.is_active, 'image_url':item.image_url} for item in items]
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

@routes.route("/select_item/<int:item_id>", methods=["POST"])
def toggle_selected(item_id):
    item = Item.query.get_or_404(item_id)  # Busca el item en la base de datos
    active = item.is_active

    if active:
        item.is_active = False
    else:
        item.is_active = True

    db.session.commit()

    cat = item.category

    if cat == 'very easy':
        return redirect('/very_easy_list')
    elif cat == 'easy':
        return redirect('/easy_list')
    elif cat == 'normal':
        return redirect('/normal_list')
    elif cat == 'hard':
        return redirect('/hard_list')
    else:
        return jsonify({'message':'PERO QUE HA PASAO!!??'})
    

@routes.route('/start_game/')
def start_game():
    items = Item.query.filter_by(is_active=True).all()

    selected_items = random.sample(items, min(len(items), 9))
    
    return render_template('game.html',items=selected_items)
    