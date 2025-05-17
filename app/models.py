from . import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Enum, UniqueConstraint
import datetime
import uuid

OlympiadStatus = Enum(
    "draft",
    "registration",
    "registration ended",
    "checking",
    "appeal",
    "completed",
    name="olympiad_status",
)

ParticipantStatus = Enum(
    "registered",
    "nullified",
    "checked",
    "appealed",
    "completed-P",
    "completed-A",
    "completed-W",
    name="participant_status",
)


class Olympiad(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    level = db.Column(db.String(50))
    logo = db.Column(db.String(255))  # Путь к логотипу
    grades = db.Column(db.String(100), default="0")  # Классы через запятую: "0,5,6,7"
    status = db.Column(OlympiadStatus, default="draft")
    participants = db.relationship("Participant", backref="olympiad")
    # Данные организатора
    organizer_username = db.Column(db.String(80), unique=True, nullable=False)
    organizer_email = db.Column(db.String(120), unique=True, nullable=False)
    organizer_password_hash = db.Column(db.String(128))
    winners_percent = db.Column(db.Float, default=0)
    awardees_percent = db.Column(db.Float, default=0)

    def set_password(self, password):
        self.organizer_password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.organizer_password_hash, password)

    def can_change_status_to(self, new_status):
        """Check if the olympiad status can be changed to the new status"""
        status_order = [
            "draft",
            "registration",
            "registration ended",
            "checking",
            "appeal",
            "completed",
        ]
        current_index = status_order.index(self.status)
        new_index = status_order.index(new_status)
        return new_index == current_index + 1  # Only allow moving to the next status


class Participant(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    olympiad_id = db.Column(db.Integer, db.ForeignKey("olympiad.id"), nullable=False)
    participant_code = db.Column(
        db.String(36), default=lambda: str(uuid.uuid4()), unique=True
    )
    grade = db.Column(db.String(10), nullable=False)
    encrypted_data = db.Column(db.Text)
    status = db.Column(ParticipantStatus, default="registered")
    work_scan = db.Column(db.String(255))
    score = db.Column(db.Integer)
    comments = db.Column(db.Text)
    appeal_text = db.Column(db.Text)
    participant_email = db.Column(db.String(120), nullable=False)
    participant_password_hash = db.Column(db.String(128))
    participant_name = db.Column(db.String(150))
    organizer_comment = db.Column(db.Text)
    temp_status = db.Column(db.String(20))

    __table_args__ = (
        UniqueConstraint(
            "olympiad_id", "participant_email", name="unique_participant_per_olympiad"
        ),
    )

    def set_password(self, password):
        self.participant_password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.participant_password_hash, password)
