from flask import Flask
from utils.config import load_config
from utils.crypto import gen_secret_key
from models.database import db, db_init
from flask_wtf.csrf import CSRFProtect


config = load_config()
csrf = CSRFProtect()
app = Flask(__name__)
app.secret_key = config["app"]["secret_key"] or gen_secret_key()


@app.before_first_request
def _db_init():
    db_init()


@app.before_request
def _db_connect():
    db.connect()


@app.teardown_request
def _db_close(exc):
    if not db.is_closed():
        db.close()


if __name__ == "__main__":
    from api import api

    app.register_blueprint(api)
    
    csrf.init_app(app)

    app.run(host=config["app"]["host"], port=config["app"]["port"])
