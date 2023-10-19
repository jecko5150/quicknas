from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import SQLAlchemyUserDatastore, Security, RoleMixin

app = Flask(__name__)
app.config['SECRET_KEY'] = 'super-secret'  # Change this to a secure secret key

# Replace with your desired file directory
UPLOAD_DIRECTORY = '/path/to/your/upload/directory'

# SQL Alchemy Config (Can be replaced with other database configurations)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///file_server.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

roles_users = db.Table(
    'roles_users',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id'))
)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users, backref=db.backref('users', lazy='dynamic'))

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    try:
        # Add authentication and permission checks here
        # Replace with your authentication and permission logic
        # Example: check if the user is authenticated before allowing the download
        if not current_user.is_authenticated:
            return "You are not authenticated!"
        return send_file(f"{UPLOAD_DIRECTORY}/{filename}", as_attachment=True)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
