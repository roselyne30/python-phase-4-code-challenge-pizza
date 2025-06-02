from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    
    restaurant_pizzas = db.relationship(
        'RestaurantPizza', back_populates='restaurant', cascade='all, delete-orphan'
    )
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
        }
    
    def to_dict_with_pizzas(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'restaurant_pizzas': [rp.to_dict() for rp in self.restaurant_pizzas]
        }


class Pizza(db.Model):
    __tablename__ = 'pizzas'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)
    
    restaurant_pizzas = db.relationship('RestaurantPizza', back_populates='pizza')
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
        }


class RestaurantPizza(db.Model):
    __tablename__ = 'restaurant_pizzas'
    
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    
    pizza_id = db.Column(db.Integer, db.ForeignKey('pizzas.id'), nullable=False)
    restaurant_id = db.Column(db.Integer, db.ForeignKey('restaurants.id'), nullable=False)
    
    pizza = db.relationship('Pizza', back_populates='restaurant_pizzas')
    restaurant = db.relationship('Restaurant', back_populates='restaurant_pizzas')
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.validate()  # Validate right after creation to raise if invalid
    
    def to_dict(self):
        return {
            'id': self.id,
            'price': self.price,
            'pizza_id': self.pizza_id,
            'restaurant_id': self.restaurant_id,
            'pizza': self.pizza.to_dict(),
            'restaurant': self.restaurant.to_dict(),
        }
    
    def validate(self):
        if not (1 <= self.price <= 30):
            raise ValueError('Price must be between 1 and 30')
