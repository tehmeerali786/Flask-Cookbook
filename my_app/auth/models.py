from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf import FlaskForm
from wtforms import TextField, PasswordField
from wtforms.validators import InputRequired, EqualTo
from my_app import db

roles = db.Table('role_users', db.Column('user_id', db.Integer, db.ForeignKey('user.id')), db.Column('role_id', db.Integer, db.ForeignKey('role.id')))

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    pwdhash = db.Column(db.String())
    roles = db.relationship('Role', secondary=roles, backref=db.backref('users', lazy='dynamic'))


    def __init__(self, username, password):
        default = Role.query.filter_by(name='default').one()
        self.roles.append(default)
        self.username = username
        self.pwdhash = generate_password_hash(password)

    def has_role(self, name):
        for role in self.roles:
            if role.name == name:
                return True
            return False

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role {}>'.format(self.name)



class RegistrationForm(FlaskForm):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Passwords must mach')])
    confirm = PasswordField('Confirm Password', [InputRequired()])


class LoginForm(FlaskForm):
    username = TextField('Username', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
