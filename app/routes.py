from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import db
from app.models import Olympiad, Participant
from app.forms import (
    OrganizerRegistrationForm,
    OrganizerLoginForm,
    OlympiadSettingsForm,
)

bp = Blueprint("main", __name__)


def init_app(app):
    app.register_blueprint(bp)


# Регистрация организатора
@bp.route("/register_organizer", methods=["GET", "POST"])
def register_organizer():
    form = OrganizerRegistrationForm()
    if form.validate_on_submit():
        # Проверка уникальности логина и email
        existing_org = Olympiad.query.filter(
            (Olympiad.organizer_username == form.username.data)
            | (Olympiad.organizer_email == form.email.data)
        ).first()

        if existing_org:
            flash("Логин или email уже заняты!")
            return redirect(url_for("main.register_organizer"))

        olympiad = Olympiad(
            organizer_username=form.username.data,
            organizer_email=form.email.data,
            name="Новая олимпиада",
            subject="Не указано",
            grades="",
        )
        olympiad.set_password(form.password.data)
        db.session.add(olympiad)
        db.session.commit()

        login_user(olympiad)
        return redirect(url_for("main.organizer_dashboard"))

    return render_template("register_organizer.html", form=form)


# Логин организатора
@bp.route("/login_organizer", methods=["GET", "POST"])
def login_organizer():
    form = OrganizerLoginForm()
    if form.validate_on_submit():
        olympiad = Olympiad.query.filter_by(
            organizer_username=form.username.data
        ).first()
        if olympiad and olympiad.check_password(form.password.data):
            login_user(olympiad)
            return redirect(url_for("main.organizer_dashboard"))
        flash("Неверные учетные данные!")
    return render_template("login_organizer.html", form=form)


# Выход
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.login_organizer"))


@bp.route("/organizer_dashboard")
@login_required
def organizer_dashboard():
    participants = Participant.query.filter_by(olympiad_id=current_user.id).all()
    form = OlympiadSettingsForm(obj=current_user)
    return render_template(
        "organizer_dashboard.html",
        participants=participants,
        custom_link=f"/customlg/{current_user.id}",
        form=form,
    )


@bp.route("/olympiad_settings", methods=["POST"])
@login_required
def olympiad_settings():
    form = OlympiadSettingsForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.subject = form.subject.data
        current_user.level = form.level.data
        current_user.grades = form.grades.data
        db.session.commit()
        flash("Настройки сохранены")
    return redirect(url_for("main.organizer_dashboard"))
