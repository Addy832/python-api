from flask import Flask, request, jsonify, abort
from models import db, Recipe

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///recipes.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    required_fields = ['title', 'making_time', 'serves', 'ingredients', 'cost']
    if not all(field in data for field in required_fields):
        return jsonify({"message": "Recipe creation failed!", "required": "title, making_time, serves, ingredients, cost"}), 200  # Changed to 200
    new_recipe = Recipe(
        title=data['title'],
        making_time=data['making_time'],
        serves=data['serves'],
        ingredients=data['ingredients'],
        cost=data['cost']
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify({"message": "Recipe successfully created!", "recipe": new_recipe.to_dict()}), 200  # Changed to 200

@app.route('/recipes', methods=['GET'])
def get_recipes():
    recipes = Recipe.query.all()
    return jsonify({"recipes": [recipe.to_dict() for recipe in recipes]}), 200

@app.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    return jsonify([recipe.to_dict()]), 200  # Return as list

@app.route('/recipes/<int:id>', methods=['PATCH'])
def update_recipe(id):
    data = request.get_json()
    recipe = Recipe.query.get_or_404(id)
    if 'title' in data:
        recipe.title = data['title']
    if 'making_time' in data:
        recipe.making_time = data['making_time']
    if 'serves' in data:
        recipe.serves = data['serves']
    if 'ingredients' in data:
        recipe.ingredients = data['ingredients']
    if 'cost' in data:
        recipe.cost = data['cost']
    db.session.commit()
    return jsonify({"message": "Recipe successfully updated!", "recipe": recipe.to_dict()}), 200

@app.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    db.session.delete(recipe)
    db.session.commit()
    return jsonify({"message": "Recipe successfully removed!"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=8080)
