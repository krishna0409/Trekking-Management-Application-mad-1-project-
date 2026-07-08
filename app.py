import os
from flask import Flask
from application.config import LocalDevelopmentConfig
from application.models import db, User, Role,Staff,Admin
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from flask import render_template

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
    app.security = Security(app, user_datastore, register_blueprint=False)
    login_manager = app.security.login_manager

    @login_manager.user_loader
    def load_user(compound_id):
        kind, _, real_id = compound_id.partition('-')
        if kind == 'user':
            return User.query.get(real_id)
        if kind == 'staff':
            return Staff.query.get(real_id)
        if kind == 'admin':
            return Admin.query.get(real_id)
        return None
    
    @login_manager.unauthorized_handler
    def unauthorized():
        return render_template("error.html")
    
    with app.app_context():
        db.create_all()
        from application import controllers
    return app

app = create_app()
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)