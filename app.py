from pathlib import Path

from flask import Flask, render_template

from config import Config
from models.complaint import Complaint
from models.user import Admin, db
from routes.admin import admin_bp
from routes.auth import auth_bp
from routes.complaint import complaint_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(complaint_bp)
    app.register_blueprint(admin_bp)

    @app.route("/")
    def index():
        total = Complaint.query.count()
        resolved = Complaint.query.filter_by(status="Resolved").count()
        pending = Complaint.query.filter_by(status="Pending").count()
        return render_template("index.html", total=total, resolved=resolved, pending=pending)

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template("404.html"), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return render_template("500.html"), 500

    with app.app_context():
        db.create_all()
        seed_admin()

    return app


def seed_admin():
    if Admin.query.filter_by(email=Config.ADMIN_EMAIL).first():
        return
    admin = Admin(full_name="System Administrator", email=Config.ADMIN_EMAIL)
    admin.set_password(Config.ADMIN_PASSWORD)
    db.session.add(admin)
    db.session.commit()


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
