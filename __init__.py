from flask import Flask
from flask.ext.mongoengine import MongoEngine
from flask.ext.cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config["MONGODB_SETTINGS"] = {'DB': "Moengage_task"}
app.config["SECRET_KEY"] = "KeepThisS3cr3t"

db = MongoEngine(app)

def register_blueprints(app):
    # Prevents circular imports
    from moengage.views import moe
    app.register_blueprint(moe)

register_blueprints(app)

if __name__ == '__main__':
    app.run()