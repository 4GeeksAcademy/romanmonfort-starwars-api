from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, )
    is_active = db.Column(db.Boolean(), unique=False, )

    def __repr__(self):
        return '<User %r>' % self.email

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }
    
    
class Planet(db.Model):
    __tablename__ = 'planets'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True)
    population = db.Column(db.Integer)
    characters = db.relationship('Character', back_populates='planet')

    def __repr__(self):
        return 'Planeta {} con id {}'.format(self.name,self.id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "population": self.population,
        }

class Character(db.Model):
    __tablename__ = 'characters'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=True)
    height = db.Column(db.Integer)
    mass = db.Column(db.Integer)
    planet_id = db.Column(db.Integer, db.ForeignKey('planets.id'))
    planet = db.relationship('Planet', back_populates='characters')

    def __repr__(self):
        return 'Personaje {} con id {}'.format(self.name,self.id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "height": self.height,
            "mass": self.mass,
            "planet": self.planet.serialize(),
        }
    
class Vehicle(db.Model):
    __tablename__ = 'vehicles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    type = db.Column(db.String(25))

    def __repr__(self):
        return 'Vehiculo {} con id {}'.format(self.name,self.id)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "type": self.type,
            "pilot": self.pilot.serialize(),
        }