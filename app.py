"""Pet Adoption Agency - Web application."""

from flask import Flask, render_template, redirect, request
# from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_db, Pet, PetForm


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///pet_adoption'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.debug = False # can change when needed

app.config['SECRET_KEY'] = 'development key'  # Needed for Flask sessions and debug toolbar
# toolbar = DebugToolbarExtension(app)

connect_db(app)
with app.app_context():
    db.create_all()

@app.route("/")
def root():
    pets = Pet.get_pets()
    return render_template("pets.html", pets=pets)

@app.route("/add", methods=['GET', 'POST'])
def add_pet():
    form = PetForm()

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        available = form.available.data
        
        new_pet = Pet(name=name, 
                      species=species, 
                      photo_url=photo_url if photo_url else None, 
                      age=age, 
                      notes=notes, 
                      available=available)
        db.session.add(new_pet)
        db.session.commit()

        return redirect('/')
    else:
        return render_template("add-pet.html", form=form)


@app.route("/<int:id>", methods= ['GET', 'POST'])
def pet_info(id):
    pet = Pet.find_pet(id) # returns a 404 error if not found
    form = PetForm(obj=pet)

    if form.validate_on_submit():
        form.populate_obj(pet) # updates pet with info taken from user-form. 
                               # should really be form.update_obj(pet)
        db.session.commit()
        return redirect(f'/{pet.id}')
    
    return render_template("pet-detail.html", pet=pet, form=form)