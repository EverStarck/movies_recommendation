from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

from routes import *

app.register_blueprint(routes)


if __name__ == "__main__":
    app.run(debug=True)