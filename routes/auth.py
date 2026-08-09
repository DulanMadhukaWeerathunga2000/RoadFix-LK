from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash

from models.db import query, execute

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
        elif query("SELECT id FROM users WHERE email = ?", (email,), one=True):
            error = "An account with that email already exists."

        if error:
            flash(error, "danger")
            return render_template("register.html", form=request.form)

        user_id = execute(
            "INSERT INTO users (full_name, email, password_hash, phone, role) VALUES (?, ?, ?, ?, ?)",
            (full_name, email, generate_password_hash(password), phone, "citizen"),
        )
        session.clear()
        session["user_id"] = user_id
        session["full_name"] = full_name
        session["role"] = "citizen"
        flash("Account created. Welcome to RoadFix LK!", "success")
        return redirect(url_for("reports.my_reports"))

    return render_template("register.html", form={})


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = query("SELECT * FROM users WHERE email = ?", (email,), one=True)
        if user is None or not check_password_hash(user["password_hash"], password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        session.clear()
        session["user_id"] = user["id"]
        session["full_name"] = user["full_name"]
        session["role"] = user["role"]
        flash(f"Welcome back, {user['full_name']}!", "success")

        if user["role"] in ("admin", "officer"):
            return redirect(url_for("admin.dashboard"))
        return redirect(url_for("reports.my_reports"))

    return render_template("login.html")


@bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
