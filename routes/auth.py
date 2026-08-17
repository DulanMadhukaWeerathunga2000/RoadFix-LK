from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user

from models.models import db, User

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name", "").strip()
        email = request.form.get("email", "").strip().lower()
        phone = request.form.get("phone", "").strip()
        password = request.form.get("password", "")

        error = None
        if not full_name or not email or not password:
            error = "Name, email and password are required."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif User.query.filter_by(email=email).first():
            error = "An account with that email already exists."

        if error:
            flash(error, "danger")
            return render_template("register.html", form=request.form)

        new_user = User(
            full_name=full_name,
            email=email,
            password_hash=generate_password_hash(password),
            phone=phone,
            role="citizen"
        )
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash("Account created. Welcome to RoadFix LK!", "success")
        return redirect(url_for("reports.my_reports"))

    return render_template("register.html", form={})


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        if current_user.role in ("admin", "officer"):
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("reports.my_reports"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        if user is None or not check_password_hash(user.password_hash, password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        remember = True if request.form.get("remember") else False
        login_user(user, remember=remember)
        
        flash(f"Welcome back, {user.full_name}!", "success")

        next_page = request.args.get("next")
        if not next_page or not next_page.startswith('/'):
            if user.role in ("admin", "officer"):
                next_page = url_for("admin.dashboard")
            else:
                next_page = url_for("reports.my_reports")
                
        return redirect(next_page)

    return render_template("login.html")


@bp.route("/logout")
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
