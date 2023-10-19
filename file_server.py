from flask import Flask, render_template, request, redirect, url_for, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'super-secret-key'

login_manager = LoginManager()
login_manager.init_app(app)

# Simulated user database (replace with a secure database in production)
users = {'admin': {'password': generate_password_hash('adminpass')}, 'user': {'password': generate_password_hash('userpass')}}

class User(UserMixin):
    def __init__(self, username, password):
        self.id = username
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id, users[user_id]['password'])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and check_password_hash(users[username]['password'], password):
            user = User(username, users[username]['password'])
            login_user(user)
            session['logged_in'] = True
            return redirect(url_for('index'))
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return 'Logged out'

@app.route('/')
@login_required
def index():
    return 'Logged in as: ' + current_user.id

if __name__ == '__main__':
    app.run(debug=True)
