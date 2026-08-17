import os
from flask import Flask, redirect, url_for, session
from flask_login import LoginManager, current_user

from config import Config
from models.db import init_db
from utils.logger import setup_logger


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize Logger
    setup_logger(app)

    init_db(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    login_manager.init_app(app)

    from models.models import User, db
    
    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    from routes.auth import bp as auth_bp
    from routes.reports import bp as reports_bp
    from routes.admin import bp as admin_bp
    from routes.api import bp as api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(reports_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(api_bp)

    @app.route("/")
    def index():
        if current_user.is_authenticated:
            if current_user.role in ("admin", "officer"):
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("reports.my_reports"))
        return redirect(url_for("map_view"))

    @app.route("/map")
    def map_view():
        from flask import render_template
        return render_template("map.html")

    @app.errorhandler(400)
    def bad_request(e):
        app.logger.warning(f"400 Bad Request: {e}")
        from flask import render_template
        return render_template("error.html", code=400, message="Bad Request. The server could not understand the request."), 400

    @app.errorhandler(401)
    def unauthorized(e):
        app.logger.warning(f"401 Unauthorized: {e}")
        from flask import render_template
        return render_template("error.html", code=401, message="Unauthorized. Please log in to access this page."), 401

    @app.errorhandler(403)
    def forbidden(e):
        app.logger.warning(f"403 Forbidden: {e}")
        from flask import render_template
        return render_template("error.html", code=403, message="Forbidden. You don't have permission to access this page."), 403

    @app.errorhandler(404)
    def not_found(e):
        app.logger.info(f"404 Not Found: {e}")
        from flask import render_template
        return render_template("error.html", code=404, message="Page not found. The requested URL was not found on this server."), 404

    @app.errorhandler(500)
    def internal_error(e):
        app.logger.error(f"500 Internal Server Error: {e}")
        from flask import render_template
        return render_template("error.html", code=500, message="Internal Server Error. Something went wrong on our end."), 500

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
