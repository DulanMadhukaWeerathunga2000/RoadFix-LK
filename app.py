import os
from flask import Flask, redirect, url_for, session

from config import Config
from models.db import init_db


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    init_db(app)

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
        if session.get("user_id"):
            if session.get("role") in ("admin", "officer"):
                return redirect(url_for("admin.dashboard"))
            return redirect(url_for("reports.my_reports"))
        return redirect(url_for("map_view"))

    @app.route("/map")
    def map_view():
        from flask import render_template
        return render_template("map.html")

    @app.errorhandler(403)
    def forbidden(e):
        from flask import render_template
        return render_template("error.html", code=403, message="You don't have access to that page."), 403

    @app.errorhandler(404)
    def not_found(e):
        from flask import render_template
        return render_template("error.html", code=404, message="Page not found."), 404

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
