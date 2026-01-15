import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Movie, User

app = Flask(__name__)

# --- Configuration ---
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = 'ssuet-bcis-2025f-project-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'movies.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- Initialize Extensions ---
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login' # Redirects guests to login if they try to access protected pages

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Database Initialization (The 10 Listings) ---
with app.app_context():
    db.create_all()
    
    if Movie.query.count() == 0:
        movies_list = [
            Movie(title="Inception", rating=8.8, city="Karachi", poster_image="inception.jpg"),
            Movie(title="Interstellar", rating=8.7, city="Lahore", poster_image="interstellar.jpg"),
            Movie(title="The Dark Knight", rating=9.0, city="Karachi", poster_image="dark_knight.jpg"),
            Movie(title="Gladiator II", rating=7.5, city="Karachi", poster_image="gladiator.jpg"),
            Movie(title="Dune: Part Two", rating=8.9, city="Islamabad", poster_image="dune2.jpg"),
            Movie(title="Avengers: Endgame", rating=8.4, city="Lahore", poster_image="avengers.jpg"),
            Movie(title="Joker", rating=8.4, city="Karachi", poster_image="joker.jpg"),
            Movie(title="Oppenheimer", rating=8.5, city="Islamabad", poster_image="oppenheimer.jfif"),
            Movie(title="Avatar", rating=7.9, city="Karachi", poster_image="avatar.jfif"),
            Movie(title="Spider-Man", rating=8.2, city="Lahore", poster_image="spiderman.jfif")
        ]
        db.session.add_all(movies_list)
        db.session.commit()
        print("Database successfully initialized!")

# --- Routes ---

@app.route('/')
def index():
    city_search = request.args.get('city')
    if city_search:
        movies = Movie.query.filter(Movie.city.contains(city_search)).all()
    else:
        movies = Movie.query.all()
    return render_template('index.html', movies=movies)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists!')
            return redirect(url_for('signup'))
        
        new_user = User(username=username, email=email, 
                        password=generate_password_hash(password, method='pbkdf2:sha256'))
        
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Invalid email or password.')
            return redirect(url_for('login'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# --- Execution ---
if __name__ == '__main__':
    app.run(debug=True)