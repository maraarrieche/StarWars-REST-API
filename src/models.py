from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship

db = SQLAlchemy()

class Usuario(db.Model):
    __tablename__ = 'usuario'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Planeta(db.Model):
    __tablename__ = 'planeta'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description
        }


class Character(db.Model):
    __tablename__ = 'character'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    description = db.Column(db.String(250), nullable=False)

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def serialize(self):
        return{
            "id": self.id,
            "name": self.name,
            "description": self.description
        }
    

class Favorite(db.Model):
    __tablename__ = 'favorite'

    id = db.Column(db.Integer, primary_key=True)
    character_id = db.Column(db.Integer, db.ForeignKey('character.id'), nullable=True)
    planeta_id = db.Column(db.Integer, db.ForeignKey('planeta.id'), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id'), nullable=False)
    character = db.relationship('Character')
    planeta = db.relationship('Planeta')
    usuario = db.relationship('Usuario')

    def __init__(self, character_id, planeta_id, usuario_id):
        self.character_id = character_id
        self.planeta_id = planeta_id
        self.usuario_id = usuario_id

    def serialize(self):
        return{
            "id": self.id,
            "character": self.character.serialize() if self.character != None else 'No character!',
            "planeta": self.planeta.serialize() if self.planeta != None else 'No planet!',
            "usuario": self.usuario.serialize() if self.usuario != None else 'No user!'
        }
