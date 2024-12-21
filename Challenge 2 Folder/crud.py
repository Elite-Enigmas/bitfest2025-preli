from sqlalchemy.orm import Session
from models import Recipe, Ingredient

async def upload_recipes(file, db: Session):
    content = await file.read()
    recipes = content.decode("utf-8").split("\n\n")
    for recipe in recipes:
        lines = recipe.split("\n")
        recipe_data = {
            "name": lines[0].split(": ")[1],
            "ingredients": lines[1].split(": ")[1],
            "taste": lines[2].split(": ")[1],
            "cuisine": lines[3].split(": ")[1],
            "preparation_time": int(lines[4].split(": ")[1]),
            "instructions": "\n".join(lines[5:])
        }
        new_recipe = Recipe(**recipe_data)
        db.add(new_recipe)
    db.commit()
    return {"message": "Recipes uploaded and parsed successfully"}

def get_recipes(taste: str, db: Session):
    query = db.query(Recipe)
    if taste:
        query = query.filter(Recipe.taste == taste)
    return query.all()

def update_ingredient(name: str, quantity: float, db: Session):
    ingredient = db.query(Ingredient).filter(Ingredient.name == name).first()
    if ingredient:
        ingredient.quantity += quantity
    else:
        new_ingredient = Ingredient(name=name, quantity=quantity, unit="unit")
        db.add(new_ingredient)
    db.commit()
    return {"message": f"Ingredient {name} updated successfully"}
