from flask import Flask
from flask_babelex import Babel

app = Flask(__name__)
babel = Babel(app)

@babel.localeselector
def get_locale():
    return 'en'  # Replace with your desired language code

if __name__ == '__main__':
    app.run(debug=True)
