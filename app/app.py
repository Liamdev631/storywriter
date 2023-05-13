from dataclasses import dataclass
from flask import Flask, jsonify, request, redirect, url_for, render_template
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = 'mysecretkey'

# flask-sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@dataclass
class User(UserMixin, db.Model):
    id = db.Column(db.String(80), primary_key=True)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

@login_manager.user_loader
def user_loader(username):
    return User.query.get(username)

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = User.query.get(username)
    if user is not None and user.check_password(password):
        login_user(user)
        return redirect(url_for('protected'))

    return 'Bad login'

@app.route('/protected')
@login_required
def protected():
    return render_template('protected.html', name=current_user.id)

@app.route('/logout', methods=['POST'])
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        user = User.query.get(current_user.get_id())
        if user is not None and user.check_password(current_password):
            user.set_password(new_password)
            db.session.commit()
            return redirect(url_for('protected'))
        else:
            return 'Current password is incorrect'
    return render_template('change_password.html')




if __name__ == "__main__":
    app.run(debug=True, port=5000)
