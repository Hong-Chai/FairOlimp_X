import os

import email_validator
from email_validator import EmailNotValidError
from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash,
    request,
    session,
    abort,
    current_app,
)
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from . import db
from app.models import Olympiad, Participant, OlympiadStatus
from app.forms import (
    OrganizerRegistrationForm,
    OrganizerLoginForm,
    OlympiadSettingsForm,
    ParticipantRegistrationForm,
    ParticipantLoginForm,
    WorkUploadForm,
    EvaluationForm,
    AppealForm,
    OlympiadStatusForm,
)

bp = Blueprint("main", __name__)


def init_app(app):
    app.register_blueprint(bp)
    # Create upload directories if they don't exist
    os.makedirs(os.path.join(app.static_folder, "logos"), exist_ok=True)
    os.makedirs(os.path.join(app.static_folder, "works"), exist_ok=True)


@bp.route("/")
def index():
    return render_template("index.html")


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
            flash(
                "Логин или email уже заняты!", "danger"
            )  # при помощи bootstrap делаем предупреждение
            return render_template(
                "register_organizer.html", form=form
            )  # передаем уже существующую форму

        olympiad = Olympiad(
            organizer_username=form.username.data,
            organizer_email=form.email.data,
            name="Новая олимпиада",
            subject="Не указано",
            grades="0",
        )
        olympiad.set_password(form.password.data)
        db.session.add(olympiad)
        db.session.commit()

        session["user_type"] = "organizer"
        login_user(olympiad)
        return redirect(url_for("main.organizer_dashboard"))
    else:
        if form.email.data:
            try:
                email_validator.validate_email(
                    form.email.data
                )  # проверяем соответсвует ли email формату
            except EmailNotValidError:
                flash(
                    "Ваш email не соответсвует формату *@*.* ", "warning"
                )  # при помощи bootstrap делаем предупреждение

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
            session["user_type"] = "organizer"
            login_user(olympiad)
            return redirect(url_for("main.organizer_dashboard"))
        else:
            flash(
                "Неверные учетные данные!", "danger"
            )  # предупреждение при помощи bootstrap
    return render_template("login_organizer.html", form=form)


# Выход
@bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop("user_type", None)
    return redirect(url_for("main.login_organizer"))


@bp.route("/organizer_dashboard")
@login_required
def organizer_dashboard():
    if session.get("user_type") != "organizer":
        logout_user()
        return redirect(url_for("main.login_organizer"))

    participants = Participant.query.filter_by(olympiad_id=current_user.id).all()
    form = OlympiadSettingsForm(obj=current_user)
    status_form = OlympiadStatusForm(status=current_user.status)
    
    return render_template(
        "organizer_dashboard.html",
        participants=participants,
        custom_link=f"/customlg/{current_user.id}",
        form=form,
        status_form=status_form,
        fn=current_user.logo
    )


@bp.route("/olympiad_settings", methods=["POST"])
@login_required
def olympiad_settings():
    if session.get("user_type") != "organizer":
        logout_user()
        return redirect(url_for("main.login_organizer"))

    form = OlympiadSettingsForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.subject = form.subject.data
        current_user.level = form.level.data
        current_user.grades = form.grades.data
        
        # Handle logo deletion
        if form.delete_logo.data and current_user.logo:
            # Delete the logo file if it exists
            logo_path = os.path.join("app/static", current_user.logo)
            if os.path.exists(logo_path):
                os.remove(logo_path)
            current_user.logo = None
            flash("Логотип удален", "success")
        # Handle logo upload only if a new file is provided
        elif form.logo.data:
            logo = form.logo.data
            filename = secure_filename(logo.filename)
            path_in_uploads = str(current_user.id) + "." + filename.split(".")[1]
            
            # Delete old logo if exists
            if current_user.logo:
                old_logo_path = os.path.join("app/static", current_user.logo)
                if os.path.exists(old_logo_path):
                    os.remove(old_logo_path)
                    
            current_user.logo = "logos/" + path_in_uploads
            logo.save(os.path.join("app/static/logos", path_in_uploads))

        db.session.commit()
        flash("Настройки сохранены", "success")
    else:
        flash("Что-то пошло не так! Настройки не были сохранены!", "danger")
    return redirect(url_for("main.organizer_dashboard"))


@bp.route("/change_olympiad_status", methods=["POST"])
@login_required
def change_olympiad_status():
    if session.get("user_type") != "organizer":
        logout_user()
        return redirect(url_for("main.login_organizer"))
        
    form = OlympiadStatusForm()
    if form.validate_on_submit():
        new_status = form.status.data
        
        # Check if the status can be changed (only forward movement allowed)
        if current_user.can_change_status_to(new_status):
            current_user.status = new_status
            db.session.commit()
            flash(f"Статус олимпиады изменен на {new_status}", "success")
        else:
            flash("Статус олимпиады можно изменять только вперед", "danger")
            
    return redirect(url_for("main.organizer_dashboard"))


@bp.route("/upload_work/<int:participant_id>", methods=["GET", "POST"])
@login_required
def upload_work(participant_id):
    if session.get("user_type") != "organizer":
        logout_user()
        return redirect(url_for("main.login_organizer"))
        
    participant = Participant.query.get_or_404(participant_id)
    
    # Check if the participant belongs to the current olympiad
    if participant.olympiad_id != current_user.id:
        flash("У вас нет доступа к этому участнику", "danger")
        return redirect(url_for("main.organizer_dashboard"))
        
    # Check if the olympiad is in the checking status
    if current_user.status != "checking":
        flash("Загрузка работ доступна только на этапе проверки", "danger")
        return redirect(url_for("main.organizer_dashboard"))
        
    form = WorkUploadForm()
    
    if form.validate_on_submit():
        work_file = form.work_file.data
        filename = secure_filename(work_file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower()
        new_filename = f"{participant.participant_code}.{file_ext}"
        
        # Save the file
        work_file.save(os.path.join("app/static/works", new_filename))
        
        # Update participant record
        participant.work_scan = f"works/{new_filename}"
        db.session.commit()
        
        flash("Работа успешно загружена", "success")
        # Redirect to evaluation form
        return redirect(url_for("main.evaluate_participant", participant_id=participant_id))
        
    return render_template("upload_work.html", form=form, participant=participant)


@bp.route("/evaluate_participant/<int:participant_id>", methods=["GET", "POST"])
@login_required
def evaluate_participant(participant_id):
    if session.get("user_type") != "organizer":
        logout_user()
        return redirect(url_for("main.login_organizer"))
        
    participant = Participant.query.get_or_404(participant_id)
    
    # Check if the participant belongs to the current olympiad
    if participant.olympiad_id != current_user.id:
        flash("У вас нет доступа к этому участнику", "danger")
        return redirect(url_for("main.organizer_dashboard"))
    
    form = EvaluationForm()
    
    if request.method == "GET":
        # Pre-populate form if evaluation exists
        if participant.score is not None:
            form.score.data = participant.score
        if participant.comments:
            form.comments.data = participant.comments
    
    if form.validate_on_submit():
        participant.score = form.score.data
        participant.comments = form.comments.data
        participant.status = "checked"
        db.session.commit()
        
        flash("Оценка сохранена", "success")
        return redirect(url_for("main.organizer_dashboard"))
        
    return render_template("evaluate_participant.html", form=form, participant=participant)


# Регистрация участника
@bp.route("/customlg/<int:olympiad_id>", methods=["GET", "POST"])
def participant_register(olympiad_id):
    olympiad = Olympiad.query.get_or_404(olympiad_id)

    # Создаем список классов из строки с классами олимпиады
    grades = [grade.strip() for grade in olympiad.grades.split(",") if grade.strip()]

    form = ParticipantRegistrationForm()
    form.grade.choices = [(grade, grade) for grade in grades]

    if form.validate_on_submit():
        # Проверяем, не зарегистрирован ли уже участник с таким email на эту олимпиаду
        existing_participant = Participant.query.filter_by(
            olympiad_id=olympiad_id, participant_email=form.email.data
        ).first()

        if existing_participant:
            flash(
                "Участник с таким email уже зарегистрирован на эту олимпиаду", "danger"
            )  # показываем предупреждение при помощи bootstrap
            return render_template(
                "participant_register.html", form=form, olympiad=olympiad,
            fn=olympiad.logo)  # возвращаем форму с уже заполненными даннами

        participant = Participant(
            olympiad_id=olympiad_id,
            participant_name=form.name.data,
            participant_email=form.email.data,
            grade=form.grade.data,
        )
        participant.set_password(form.password.data)

        db.session.add(participant)
        db.session.commit()

        flash("Регистрация успешна! Теперь вы можете войти в систему.", "success")
        return redirect(url_for("main.participant_login", olympiad_id=olympiad_id))
    else:
        if form.email.data:
            try:
                email_validator.validate_email(
                    form.email.data
                )  # проверяем соответсвует ли email формату
            except EmailNotValidError:
                flash(
                    "Ваш email не соответсвует формату *@*.* ", "warning"
                )  # при помощи bootstrap делаем предупреждение
    return render_template("participant_register.html", form=form, olympiad=olympiad,
                           fn=olympiad.logo)


# Логин участника
@bp.route("/customlg/<int:olympiad_id>/login", methods=["GET", "POST"])
def participant_login(olympiad_id):
    olympiad = Olympiad.query.get_or_404(olympiad_id)

    form = ParticipantLoginForm()

    if form.validate_on_submit():
        participant = Participant.query.filter_by(
            olympiad_id=olympiad_id, participant_email=form.email.data
        ).first()

        if participant and participant.check_password(form.password.data):
            session["user_type"] = "participant"
            login_user(participant)
            return redirect(
                url_for("main.participant_dashboard", olympiad_id=olympiad_id)
            )

        flash("Неверный email или пароль", "danger")

    else:
        if form.email.data:
            try:
                email_validator.validate_email(form.email.data)
            except EmailNotValidError:
                flash(
                    "Ваш email не соответсвует формату *@*.* ", "warning"
                )  # при помощи bootstrap делаем предупреждение

    return render_template("participant_login.html", form=form, olympiad=olympiad, fn=olympiad.logo)


# Личный кабинет участника
@bp.route("/customlg/<int:olympiad_id>/dashboard")
@login_required
def participant_dashboard(olympiad_id):
    if session.get("user_type") != "participant":
        logout_user()
        return redirect(url_for("main.participant_login", olympiad_id=olympiad_id))

    olympiad = Olympiad.query.get_or_404(olympiad_id)

    # Проверяем, что текущий пользователь - участник этой олимпиады
    if current_user.olympiad_id != olympiad_id:
        logout_user()
        flash("У вас нет доступа к этой олимпиаде", "error")
        return redirect(url_for("main.participant_login", olympiad_id=olympiad_id))

    # Create appeal form if olympiad is in appeal status
    appeal_form = None
    if olympiad.status == "appeal":
        appeal_form = AppealForm()
        if current_user.appeal_text:
            appeal_form.appeal_text.data = current_user.appeal_text

    return render_template(
        "participant_dashboard.html", 
        participant=current_user, 
        olympiad=olympiad, 
        appeal_form=appeal_form,
        fn=olympiad.logo
    )


@bp.route("/customlg/<int:olympiad_id>/submit_appeal", methods=["POST"])
@login_required
def submit_appeal(olympiad_id):
    if session.get("user_type") != "participant":
        logout_user()
        return redirect(url_for("main.participant_login", olympiad_id=olympiad_id))
        
    olympiad = Olympiad.query.get_or_404(olympiad_id)
    
    # Check if the olympiad is in appeal status
    if olympiad.status != "appeal":
        flash("Подача апелляций в данный момент недоступна", "danger")
        return redirect(url_for("main.participant_dashboard", olympiad_id=olympiad_id))
        
    form = AppealForm()
    if form.validate_on_submit():
        current_user.appeal_text = form.appeal_text.data
        current_user.status = "appealed"
        db.session.commit()
        
        flash("Апелляция отправлена", "success")
        
    return redirect(url_for("main.participant_dashboard", olympiad_id=olympiad_id))


# Выход участника
@bp.route("/customlg/<int:olympiad_id>/logout")
@login_required
def participant_logout(olympiad_id):
    logout_user()
    session.pop("user_type", None)
    return redirect(url_for("main.participant_login", olympiad_id=olympiad_id))