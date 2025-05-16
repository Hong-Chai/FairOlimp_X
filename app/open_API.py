import datetime
import os

from flask import (
    Blueprint,
    redirect,
    url_for,
    session,
    send_file
)
from flask_login import logout_user, login_required, current_user

from app.models import Olympiad, Participant

from app.funcs.generate_diploma import create_diploma_pdf
from app.funcs.generate_blank import create_blank_pdf
from app.funcs.generate_certificate import create_certificate_pdf

from app.funcs.check_account_in_ORM import check_acc

bp = Blueprint("API", __name__)


def init_app(app):
    app.register_blueprint(bp)

    os.makedirs('app/funcs/output', exist_ok=True)

@bp.route("/generate_certificate/<int:olympiad_id>", methods=["GET", "POST"])
@login_required
def create_certificate(olympiad_id):
    olympiad = Olympiad.query.get_or_404(olympiad_id)

    if session.get("user_type") != "participant" or not check_acc(current_user.participant_code):
        logout_user()
        return redirect(url_for("main.register_organizer"))


    olymp_con = Olympiad.query.filter(Olympiad.id == olympiad_id).first()
    olymp_name = olymp_con.name

    create_certificate_pdf(filename="app/funcs/output/certificate.pdf",
                       olympiad_name=olymp_name,
                       participant_name=current_user.participant_name,
                       olympiad_id=olympiad_id,
                       participant_code=current_user.participant_code
                       )
    path = "funcs\\output\\certificate.pdf"
    return send_file(path, as_attachment=True)


@bp.route("/generate_diploma/<int:olympiad_id>", methods=["GET", "POST"])
@login_required
def create_diploma(olympiad_id):
    olympiad = Olympiad.query.get_or_404(olympiad_id)

    if session.get("user_type") != "participant" or not check_acc(current_user.participant_code):
        logout_user()
        return redirect(url_for("main.register_organizer"))

    name = current_user.participant_name
    grade = current_user.grade
    code = current_user.participant_code

    olymp_con = Olympiad.query.filter(Olympiad.id == olympiad_id).first()
    olymp_name = olymp_con.name
    olymp_level = olymp_con.level

    create_diploma_pdf(filename="app/funcs/output/diploma.pdf",
                       name=name,
                       participant_code=code,
                       grade=grade,
                       olympiad_name=olymp_name,
                       olympiad_level=olymp_level,
                       date=datetime.date.today(),
                       status_by_res="POKA_NET"
                       )
    path = "funcs\\output\\diploma.pdf"
    return send_file(path, as_attachment=True)

@bp.route("/generate_blank/<int:olympiad_id>", methods=["GET", "POST"])
@login_required
def create_blank(olympiad_id):
    olympiad = Olympiad.query.get_or_404(olympiad_id)

    if session.get("user_type") != "organizer":
        code = current_user.participant_code
    else:
        code = "Здесь будет отображен код участника"
    create_blank_pdf(
        filename="app/funcs/output/blank.pdf",
        olympiad_id=olympiad_id,
        date=datetime.date.today(),
        participant_code=code
    )
    path = "funcs\\output\\blank.pdf"
    return send_file(path, as_attachment=True)
