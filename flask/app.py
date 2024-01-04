from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
import os

db_host = os.getenv('HYDRANT_DB_HOST')
db_name = os.getenv('HYDRANT_DB')
db_user = os.getenv('HYDRANT_DB_USER')
db_password = os.getenv('HYDRANT_DB_PASS')
db_port = os.getenv('HYDRANT_DB_PORT')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://'+db_user+':'+db_password+'@'+db_host+'/'+db_name
db = SQLAlchemy(app)

Bootstrap(app)

class hydrant_status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    status = db.Column(db.String(100))
    pressure = db.Column(db.Float)

    def to_dict(self):
        return {
            'id': self.id,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'status': self.status,  # assuming you have a status field
            'pressure': self.pressure  # assuming you have a pressure field
        }

@app.route('/')
def index():
    points = hydrant_status.query.all()
    points_data = [point.to_dict() for point in points]
    return render_template('map_view.html', points=points_data)


@app.route('/update_point/<int:point_id>', methods=['POST'])
def update_point(point_id):
    point = hydrant_status.query.get(point_id)
    if point:
        point.status = request.form['status']
        point.pressure = request.form['pressure']
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
