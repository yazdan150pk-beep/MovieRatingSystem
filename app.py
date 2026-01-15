import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# This tells Flask where to save the database file
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Database Table for Movies (Movie Portal & Cinema Finder feature)
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Float)
    city = db.Column(db.String(50)) # For finding showtimes in their city

# Command to create the database file
with app.app_context():
    db.create_all()
    # Let's add 2 sample movies so the site isn't empty
    if Movie.query.count() == 0:
        sample1 = Movie(title="Inception", rating=8.8, city="Karachi")
        sample2 = Movie(title="The Dark Knight", rating=9.0, city="Lahore")
        db.session.add(sample1)
        db.session.add(sample2)
        db.session.commit()

@app.route('/')
def home():
    all_movies = Movie.query.all()
    return render_template('index.html', movies=all_movies)

if __name__ == '__main__':
    app.run(debug=True)