from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.user import Admin, User, db
from utils.helper import clean_text, validate_email, validate_phone


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = clean_text(request.form.get("full_name"), 120)
        email = clean_text(request.form.get("email"), 120).lower()
        phone = clean_text(request.form.get("phone"), 20)
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not all([full_name, email, phone, password, confirm_password]):
            flash("All fields are required.", "danger")
        elif not validate_email(email):
            flash("Enter a valid email address.", "danger")
        elif not validate_phone(phone):
            flash("Enter a valid phone number.", "danger")
        elif len(password) < 8:
            flash("Password must be at least 8 characters.", "danger")
        elif password != confirm_password:
            flash("Passwords do not match.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "danger")
        else:
            user = User(full_name=full_name, email=email, phone=phone)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Registration successful. Please log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = clean_text(request.form.get("email"), 120).lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session.clear()
            session["role"] = "citizen"
            session["user_id"] = user.id
            session["user_name"] = user.full_name
            flash("Welcome back.", "success")
            return redirect(url_for("complaint.dashboard"))
        flash("Invalid email or password.", "danger")

    return render_template("login.html", mode="citizen")


@auth_bp.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        email = clean_text(request.form.get("email"), 120).lower()
        password = request.form.get("password", "")
        admin = Admin.query.filter_by(email=email).first()
        if admin and admin.check_password(password):
            session.clear()
            session["role"] = "admin"
            session["admin_id"] = admin.id
            session["user_name"] = admin.full_name
            flash("Administrator login successful.", "success")
            return redirect(url_for("admin.dashboard"))
        flash("Invalid administrator credentials.", "danger")

    return render_template("login.html", mode="admin")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("index"))
