from sqlalchemy import func
from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.complaint import Complaint
from models.user import User, db
from utils.classifier import VALID_CATEGORIES, classify_complaint
from utils.helper import citizen_required, clean_text, save_upload, validate_email, validate_phone


complaint_bp = Blueprint("complaint", __name__)


@complaint_bp.route("/dashboard")
@citizen_required
def dashboard():
    user = User.query.get_or_404(session["user_id"])
    complaints = Complaint.query.filter_by(user_id=user.id).order_by(Complaint.created_at.desc()).all()
    stats = {
        "total": len(complaints),
        "pending": sum(1 for item in complaints if item.status == "Pending"),
        "progress": sum(1 for item in complaints if item.status == "In Progress"),
        "resolved": sum(1 for item in complaints if item.status == "Resolved"),
    }
    return render_template("dashboard.html", user=user, complaints=complaints, stats=stats)


@complaint_bp.route("/complaint", methods=["GET", "POST"])
@citizen_required
def report_complaint():
    user = User.query.get_or_404(session["user_id"])
    if request.method == "POST":
        try:
            full_name = clean_text(request.form.get("full_name"), 120)
            phone = clean_text(request.form.get("phone"), 20)
            email = clean_text(request.form.get("email"), 120).lower()
            title = clean_text(request.form.get("title"), 160)
            description = clean_text(request.form.get("description"), 3000)
            location = clean_text(request.form.get("location"), 180)
            category_input = clean_text(request.form.get("category"), 80)

            if not all([full_name, phone, email, title, description, location]):
                flash("Please complete every required field.", "danger")
            elif not validate_email(email):
                flash("Enter a valid email address.", "danger")
            elif not validate_phone(phone):
                flash("Enter a valid phone number.", "danger")
            else:
                image_filename = save_upload(request.files.get("photo"))
                classification = classify_complaint(title, description, category_input)
                category = classification["category"]
                priority = classification["priority"]
                complaint = Complaint(
                    user_id=user.id,
                    full_name=full_name,
                    phone=phone,
                    email=email,
                    title=title,
                    description=description,
                    location=location,
                    category=category,
                    priority=priority,
                    image_filename=image_filename,
                )
                db.session.add(complaint)
                db.session.commit()
                flash(f"Complaint submitted. Category: {category}, Priority: {priority}.", "success")
                return redirect(url_for("complaint.dashboard"))
        except ValueError as exc:
            flash(str(exc), "danger")

    return render_template("complaint.html", user=user, categories=VALID_CATEGORIES)


@complaint_bp.route("/profile", methods=["GET", "POST"])
@citizen_required
def profile():
    user = User.query.get_or_404(session["user_id"])
    if request.method == "POST":
        full_name = clean_text(request.form.get("full_name"), 120)
        phone = clean_text(request.form.get("phone"), 20)
        email = clean_text(request.form.get("email"), 120).lower()

        if not all([full_name, phone, email]):
            flash("All profile fields are required.", "danger")
        elif not validate_email(email):
            flash("Enter a valid email address.", "danger")
        elif not validate_phone(phone):
            flash("Enter a valid phone number.", "danger")
        else:
            existing = User.query.filter(User.email == email, User.id != user.id).first()
            if existing:
                flash("Another account already uses this email.", "danger")
            else:
                user.full_name = full_name
                user.phone = phone
                user.email = email
                db.session.commit()
                session["user_name"] = user.full_name
                flash("Profile updated.", "success")
                return redirect(url_for("complaint.profile"))

    history = (
        db.session.query(Complaint.status, func.count(Complaint.id))
        .filter_by(user_id=user.id)
        .group_by(Complaint.status)
        .all()
    )
    return render_template("profile.html", user=user, history=dict(history))
