"""Flask app for Cupcakes"""
from flask import Flask, request, render_template, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_cors import CORS 
from models import db, connect_db, Cupcake

app=Flask(__name__)

CORS(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"
toolbar = DebugToolbarExtension(app)


with app.app_context():
    
    connect_db(app)
    db.create_all()
    
    
@app.route('/', methods=['GET'])
def root_page():
    
    return render_template('homepage.html')
    
@app.route('/api/cupcakes', methods=['GET'])
def get_all_cupcakes():
    # GET /api/cupcakes : Get data about all cupcakes. Respond with JSON like: {cupcakes: [{id, flavor, size, rating, image}, ...]}. 
    # The values should come from each cupcake instance.

    cupcakes = [cupcake.serialize_cupcakes() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes) 


    
@app.route('/api/cupcakes/<int:cupcake_id>', methods=['GET'])
def get_cupcake(cupcake_id):
    
# GET /api/cupcakes/[cupcake-id] : Get data about a single cupcake. Respond with JSON like: {cupcake: {id, flavor, size, rating, image}}. 
# This should raise a 404 if the cupcake cannot be found.

    cupcake = [cupcate.serialize_cupcakes() for cupcake in Cupcake.query.get_or_404(cupcake_id)]
    
    return jsonify(cupcake=cupcake)

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    
# POST /api/cupcakes : Create a cupcake with flavor, size, rating and image data from the body of the request. 
# espond with JSON like: {cupcake: {id, flavor, size, rating, image}}.    

    data=request.json
    
    cupcake = Cupcake(
        flavor=data['flavor'],
        size=data['size'],
        rating=data['rating'],
        image=data['image'] or None
    )
    
    db.session.add(cupcake)
    db.session.commit()
    
    return (jsonify(cupcake=cupcake.serialize_cupcakes()),201)

    
@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake_data(cupcake_id):
    
# PATCH /api/cupcakes/[cupcake-id] : Update a cupcake with the id passed in the URL and 
# flavor, size, rating and image data from the body of the request. You can always assume that the entire 
# cupcake object will be passed to the backend. This should raise a 404 if the cupcake cannot be found. Respond with JSON of 
# the newly-updated cupcake, like this: {cupcake: {id, flavor, size, rating,image}}.
    data=request.json
    
    cupcake= Cupcake.query.get_or_404(cupcake_id)
    
    cupcake.flavor = data['flavor']
    cupcake.size=data['size']
    cupcake.rating=data['rating']
    cupcake.image=data['image']
    
    db.session.add(cupcake)
    db.session.commit()
    
    return jsonify(cupcake=cupcake.serialize_cupcakes())


@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):

# This should raise a 404 if the cupcake cannot be found.
# Delete cupcake with the id passed in the URL. Respond with JSON like `{message: "Deleted"}`.
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    
    db.session.delete(cupcake)
    db.session.commit()
    
    return jsonify(message='Deleted')

if __name__ == '__main__':
    app.run(debug=True)
