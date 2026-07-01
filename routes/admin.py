import csv
from io import StringIO

from flask import Blueprint, Response, flash, redirect, render_template, request, url_for
from sqlalchemy import asc, desc, func, or_

from models.complaint import Complaint
from models.user import db
from utils.classifier import VALID_CATEGORIES, VALID_PRIORITIES, VALID_STATUSES
from utils.helper import admin_required, clean_text


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def filtered_complaints():
    query = Complaint.query
    search = clean_text(request.args.get("search"), 120)
    category = clean_text(request.args.get("category"), 80)
    status = clean_text(request.args.get("status"), 30)
    priority = clean_text(request.args.get("priority"), 30)
    sort = request.args.get("sort", "newest")

    if search:
        like = f"%{search}%"
        query = query.filter(
            or_(
                Complaint.full_name.ilike(like),
                Complaint.phone.ilike(like),
                Complaint.category.ilike(like),
                Complaint.status.ilike(like),
                Complaint.location.ilike(like),
            )
        )
    if category:
        query = query.filter_by(category=category)
    if status:
        query = query.filter_by(status=status)
    if priority:
        query = query.filter_by(priority=priority)

    sort_map = {
        "oldest": asc(Complaint.created_at),
        "priority": desc(Complaint.priority),
        "status": asc(Complaint.status),
        "category": asc(Complaint.category),
        "newest": desc(Complaint.created_at),
    }
    return query.order_by(sort_map.get(sort, desc(Complaint.created_at)))


def analytics_payload():
    total = Complaint.query.count()
    resolved = Complaint.query.filter_by(status="Resolved").count()
    pending = Complaint.query.filter_by(status="Pending").count()
    progress = Complaint.query.filter_by(status="In Progress").count()
    rejected = Complaint.query.filter_by(status="Rejected").count()

    categories = db.session.query(Complaint.category, func.count(Complaint.id)).group_by(Complaint.category).all()
    priorities = db.session.query(Complaint.priority, func.count(Complaint.id)).group_by(Complaint.priority).all()
    monthly = (
        db.session.query(func.strftime("%Y-%m", Complaint.created_at), func.count(Complaint.id))
        .group_by(func.strftime("%Y-%m", Complaint.created_at))
        .order_by(func.strftime("%Y-%m", Complaint.created_at))
        .all()
    )
    return {
        "totals": {"total": total, "resolved": resolved, "pending": pending, "progress": progress, "rejected": rejected},
        "categories": dict(categories),
        "priorities": dict(priorities),
        "monthly": dict(monthly),
    }


@admin_bp.route("/dashboard")
@admin_required
def dashboard():
    recent = Complaint.query.order_by(Complaint.created_at.desc()).limit(6).all()
    return render_template("admin_dashboard.html", analytics=analytics_payload(), recent=recent)


@admin_bp.route("/complaints")
@admin_required
def complaints():
    items = filtered_complaints().all()
    return render_template(
        "complaints.html",
        complaints=items,
        categories=VALID_CATEGORIES,
        statuses=VALID_STATUSES,
        priorities=VALID_PRIORITIES,
    )


@admin_bp.route("/complaints/<int:complaint_id>/status", methods=["POST"])
@admin_required
def update_status(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    status = clean_text(request.form.get("status"), 30)
    if status not in VALID_STATUSES:
        flash("Invalid status selected.", "danger")
    else:
        complaint.status = status
        db.session.commit()
        flash("Complaint status updated.", "success")
    return redirect(request.referrer or url_for("admin.complaints"))


@admin_bp.route("/complaints/<int:complaint_id>/delete", methods=["POST"])
@admin_required
def delete_complaint(complaint_id):
    complaint = Complaint.query.get_or_404(complaint_id)
    db.session.delete(complaint)
    db.session.commit()
    flash("Complaint deleted.", "info")
    return redirect(request.referrer or url_for("admin.complaints"))


@admin_bp.route("/analytics")
@admin_required
def analytics():
    return render_template("analytics.html", analytics=analytics_payload())


@admin_bp.route("/export.csv")
@admin_required
def export_csv():
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID", "Name", "Phone", "Email", "Title", "Location", "Category", "Priority", "Status", "Created"])
    for complaint in filtered_complaints().all():
        writer.writerow(complaint.to_csv_row())
    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=complaints.csv"},
    )
