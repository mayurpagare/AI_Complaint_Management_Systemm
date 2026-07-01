import re
from functools import wraps
from pathlib import Path
from uuid import uuid4

from flask import current_app, flash, redirect, request, session, url_for
from markupsafe import escape
from werkzeug.utils import secure_filename


EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
PHONE_RE = re.compile(r"^[0-9+\-\s()]{7,20}$")


def clean_text(value, max_length=None):
    value = " ".join((value or "").strip().split())
    if max_length:
        value = value[:max_length]
    return str(escape(value))


def validate_email(email):
    return bool(EMAIL_RE.match(email or ""))


def validate_phone(phone):
    return bool(PHONE_RE.match(phone or ""))


def allowed_file(filename):
    suffix = Path(filename or "").suffix.lower().lstrip(".")
    return suffix in current_app.config["ALLOWED_EXTENSIONS"]


def save_upload(file_storage):
    if not file_storage or not file_storage.filename:
        return None
    if not allowed_file(file_storage.filename):
        raise ValueError("Only JPG, JPEG, and PNG uploads are allowed.")

    upload_folder = Path(current_app.config["UPLOAD_FOLDER"])
    upload_folder.mkdir(parents=True, exist_ok=True)
    original = secure_filename(file_storage.filename)
    suffix = Path(original).suffix.lower()
    filename = f"{uuid4().hex}{suffix}"
    file_storage.save(upload_folder / filename)
    return filename


def citizen_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("role") != "citizen" or not session.get("user_id"):
            flash("Please log in as a citizen to continue.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


def admin_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if session.get("role") != "admin" or not session.get("admin_id"):
            flash("Please log in as an administrator to continue.", "warning")
            return redirect(url_for("auth.admin_login"))
        return view(*args, **kwargs)

    return wrapped


def wants_json():
    return request.headers.get("X-Requested-With") == "XMLHttpRequest"
