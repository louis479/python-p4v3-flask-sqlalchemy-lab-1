# server/app.py
#!/usr/bin/env python3

from flask import Flask, make_response
from flask_migrate import Migrate

from models import db, Earthquake

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)


@app.route('/')
def index():
    body = {'message': 'Flask SQLAlchemy Lab 1'}
    return make_response(body, 200)

# Add views here
@app.route('/earthquakes/<int:id>')
def get_earthquake(id):
    quake = Earthquake.query.get(id)
    if not quake:
        return make_response({'message': f"Earthquake {id} not found."}, 404)
    return make_response(quake.to_dict(), 200)

@app.route('/earthquakes/magnitude/<float:mag>')
def earthquakes_by_magnitude(mag):
    quakes = Earthquake.query.filter(Earthquake.magnitude >= mag).order_by(Earthquake.id).all()
    quakes_list = [q.to_dict() for q in quakes]
    return make_response({
        "count": len(quakes_list),
        "quakes": quakes_list
    }, 200)



if __name__ == '__main__':
    app.run(port=5555, debug=True)
