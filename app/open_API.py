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
def create_certificate(olympiad_id):
    olympiad = Olympiad.query.get_or_404(olympiad_id)

    olymp_con = Olympiad.query.filter(Olympiad.id == olympiad_id).first()
    olymp_name = olymp_con.name

    if session.get("user_type") != "participant":
        pt_name = "ФИО участника"
        id_p = f"not_from_participant_with_olymp_id_{olympiad_id}"
        pt_code = "Здесь будет отображен код участника"
    else:
        pt_name = current_user.participant_name
        id_p = current_user.id
        pt_code = current_user.participant_code


    if os.path.exists(f"app/funcs/output/certificate_{id_p}.pdf"):
        os.remove(f"app/funcs/output/certificate_{id_p}.pdf")

    create_certificate_pdf(filename=f"app/funcs/output/certificate_{id_p}.pdf",
                       olympiad_name=olymp_name,
                       participant_name=pt_name,
                       olympiad_id=olympiad_id,
                       participant_code=pt_code
                       )
    path = f"funcs\\output\\certificate_{id_p}.pdf"
    return send_file(path, as_attachment=True)


@bp.route("/generate_diploma/<pt_code>", methods=["GET", "POST"])
def create_diploma(pt_code):
    if not check_acc(pt_code):
        return "Аккаунта не существует"

    status_raw = Participant.query.filter(Participant.participant_code == pt_code).first().status

    if status_raw not in ["completed-A", "completed-W", "completed-P"]:
        return "Олимпиада ещё не завершена!"

    if session.get("user_type") != "participant":
        pt_con = Participant.query.filter(Participant.participant_code == pt_code).first()
        name = pt_con.participant_name
        grade = pt_con.grade
        code = pt_code
        status = "Призёр" if status_raw == "completed-A" else ("Победитель" if status_raw == "completed-W" else
                                                               "Участник")
        ol_id = pt_con.olympiad_id
        olymp_con = Olympiad.query.filter(Olympiad.id == ol_id).first()
        olymp_name = olymp_con.name
        olymp_level = olymp_con.level
        id_p = f"not_from_participant_with_code_{code}"
    else:
        name = current_user.participant_name
        grade = current_user.grade
        code = current_user.participant_code
        status = "Призёр" if status_raw == "completed-A" else ("Победитель" if status_raw == "completed-W" else
                                                               "Участник")
        olymp_con = Olympiad.query.filter(Olympiad.id == current_user.olympiad_id).first()
        olymp_name = olymp_con.name
        olymp_level = olymp_con.level
        id_p = current_user.id

    if os.path.exists(f"app/funcs/output/diploma_{id_p}.pdf"):
        os.remove(f"app/funcs/output/diploma_{id_p}.pdf")

    create_diploma_pdf(filename=f"app/funcs/output/diploma_{id_p}.pdf",
                       name=name,
                       participant_code=code,
                       grade=grade,
                       olympiad_name=olymp_name,
                       olympiad_level=olymp_level,
                       date=datetime.date.today(),
                       status_by_res=status
                       )
    path = f"funcs\\output\\diploma_{id_p}.pdf"
    return send_file(path, as_attachment=True)

@bp.route("/generate_blank/<pt_code>", methods=["GET", "POST"])
def create_blank(pt_code):
    if not check_acc(pt_code):
        return "Аккаунта не существует"

    if session.get("user_type") != "participant":
        pt_con = Participant.query.filter(Participant.participant_code == pt_code).first()
        code = pt_code
        id = f"not_from_participant_with_code_{pt_code}"
        olympiad_id = pt_con.olympiad_id
    else:
        code = current_user.participant_code
        id = current_user.id
        olympiad_id = current_user.olympiad_id

    if os.path.exists(f"app/funcs/output/blank_{id}.pdf"):
        os.remove(f"app/funcs/output/blank_{id}.pdf")

    create_blank_pdf(
        filename=f"app/funcs/output/blank_{id}.pdf",
        olympiad_id=olympiad_id,
        date=datetime.date.today(),
        participant_code=code
    )
    path = f"funcs\\output\\blank_{id}.pdf"
    return send_file(path, as_attachment=True)
