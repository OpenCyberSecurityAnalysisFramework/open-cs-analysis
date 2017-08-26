from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Employee(UserMixin, db.Model):
    """
    Create an Employee table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'employees'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.id'))
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    attacker_id = db.Column(db.Integer, db.ForeignKey('attackers.id'))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Employee: {}>'.format(self.username)


# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


class Department(db.Model):
    """
    Create a Department table
    """

    __tablename__ = 'departments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='department',
                                lazy='dynamic')

    def __repr__(self):
        return '<Department: {}>'.format(self.name)


class Role(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    employees = db.relationship('Employee', backref='role',
                                lazy='dynamic')

    def __repr__(self):
        return '<Role: {}>'.format(self.name)


class Analyse(db.Model):
    """
    Create a Role table
    """

    __tablename__ = 'analyses'

    id = db.Column(db.Integer, primary_key=True)
    #date = db.Column(db.Date)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    assets = db.relationship('Asset', backref='asset',
                                lazy='dynamic')

    def __repr__(self):
        return '<Analyse: {}>'.format(self.name)


class Asset(db.Model):

    """
    Create a Asset table
    """

    __tablename__ = 'assets'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    sensitivity = db.Column(db.Integer)
    criticality = db.Column(db.Integer)

    analyse_id = db.Column(db.Integer, db.ForeignKey('analyses.id'))

    assetattackers = db.relationship('AssetAttacker', backref="assetattacker", cascade="all, delete-orphan", lazy='dynamic')

    exposition = db.Column(db.Float)

    def __repr__(self):
        return '<Asset: {}>'.format(self.name)

class AssetAttacker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    asset_id = db.Column(db.Integer, db.ForeignKey('assets.id'))
    attacker_id = db.Column(db.Integer, db.ForeignKey('attackers.id'))
    wert = db.Column(db.Integer)
    description = db.Column(db.String(200))

class Attacker(db.Model):
    """
    Create a Attacker table
    """

    __tablename__ = 'attackers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), unique=True)
    description = db.Column(db.String(200))
    wert = db.Column(db.Integer)
    employees = db.relationship('Employee', backref='attacker',
                                lazy='dynamic')
    assetattackers2 = db.relationship('AssetAttacker', backref="assetattacker2", cascade="all, delete-orphan",
                                     lazy='dynamic')

    def __repr__(self):
        return '<Attacker: {}>'.format(self.name)