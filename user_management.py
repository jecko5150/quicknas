from werkzeug.security import generate_password_hash, check_password_hash

# Simulated user database (replace with a secure database in production)
users = {'admin': {'password': generate_password_hash('adminpass')},
         'user': {'password': generate_password_hash('userpass')}
         }


def get_user(username):
    if username in users:
        return users[username]
    return None


def add_user(username, password):
    if username not in users:
        users[username] = {'password': generate_password_hash(password)}
        return True
    return False


def verify_password(stored_password, password):
    return check_password_hash(stored_password, password)
