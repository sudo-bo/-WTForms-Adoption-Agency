"""Models for Adoption Agency."""

from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, BooleanField, SelectField
from wtforms.validators import InputRequired, DataRequired, Optional, URL, NumberRange

db = SQLAlchemy()
def connect_db(app):
    """Connect this database to provided Flask app."""
    db.app = app
    db.init_app(app)

class Pet(db.Model):
    """Users."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    species = db.Column(db.String(50), nullable=False)
    photo_url = db.Column(db.Text, default="https://lh5.googleusercontent.com/proxy/CvtZRFvsfQZQWK_hz-ia2jLi2K4sh2s8fkFkcPTKryuxaody6pC5Rz3-kGqHSw4pXipMgqEr5U5BWEMLoAVNcK5TyhJT-g6QlfU4pXcfB3l5h2--4lEka5oHwrdSHrx-tn82DwI_DV9G_I9dvw9x3vPnkwvlMZqq")
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)

    @classmethod
    def get_pets(cls):
        return cls.query.all()
    
    @classmethod
    def find_pet(cls, id):
        return cls.query.get_or_404(id)
    
class PetForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    species = SelectField('Species', choices=[('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine')], validators=[DataRequired()])
    photo_url = StringField('Pet Photo Link', validators=[Optional(), URL()])
    age = IntegerField('Age', validators=[Optional(), NumberRange(min=0, max=30)])
    notes = StringField('Notes')
    available = BooleanField('Available or Unavailable', validators=[InputRequired()])
    submit = SubmitField('Add Pet')
    