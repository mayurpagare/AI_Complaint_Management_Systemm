from datetime import datetime

from models.user import db


class Complaint(db.Model):
    __tablename__ = "complaints"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    full_name = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    title = db.Column(db.String(160), nullable=False)
    description = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(180), nullable=False)
    category = db.Column(db.String(80), nullable=False, index=True)
    priority = db.Column(db.String(20), nullable=False, default="Low", index=True)
    status = db.Column(db.String(20), nullable=False, default="Pending", index=True)
    image_filename = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def to_csv_row(self):
        return [
            self.id,
            self.full_name,
            self.phone,
            self.email,
            self.title,
            self.location,
            self.category,
            self.priority,
            self.status,
            self.created_at.strftime("%Y-%m-%d %H:%M"),
        ]
