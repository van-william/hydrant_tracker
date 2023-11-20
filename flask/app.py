# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hydrant.db'
db = SQLAlchemy(app)

class Point(db.Model):
    index = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(255))

@app.route('/')
def index():
    points = Point.query.all()
    return render_template('index.html', points=points)

@app.route('/update_metadata/<int:point_id>', methods=['GET', 'POST'])
def update_metadata(point_id):
    point = Point.query.get(point_id)
    if request.method == 'POST':
        point.metadata = request.form['metadata']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('update_metadata.html', point=point)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
