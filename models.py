from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    making_time = db.Column(db.String(80), nullable=False)
    serves = db.Column(db.String(80), nullable=False)
    ingredients = db.Column(db.String(255), nullable=False)
    cost = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "making_time": self.making_time,
            "serves": self.serves,
            "ingredients": self.ingredients,
            "cost": self.cost,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
