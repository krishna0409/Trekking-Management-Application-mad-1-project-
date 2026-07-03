import os
from flask import Flask
from application.config import LocalDevelopmentConfig
from application.models import db, User, Role
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
def create_app():
    app = Flask(__name__, template_folder="templates")
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    print("Starting Local Development")
    app.config.from_object(LocalDevelopmentConfig)
    db_dir = app.config.get("SQLITE_DB_DIR")
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)
    db.init_app(app)
    user_datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, user_datastore)
    with app.app_context():
        db.create_all()
        from application import controllers  # noqa: registers routes
    return app
app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)