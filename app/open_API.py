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

    if os.path.exists(f"app/funcs/output/certificate_{current_user.id}.pdf"):
        os.remove(f"app/funcs/output/certificate_{current_user.id}.pdf")

    create_certificate_pdf(filename=f"app/funcs/output/certificate_{current_user.id}.pdf",
                       olympiad_name=olymp_name,
                       participant_name=current_user.participant_name,
                       olympiad_id=olympiad_id,
                       participant_code=current_user.participant_code
                       )
    path = f"funcs\\output\\certificate_{current_user.id}.pdf"
    return send_file(path, as_attachment=True)


@bp.route("/generate_diploma/<int:olympiad_id>", methods=["GET", "POST"])
@login_required
def create_diploma(olympiad_id):
    olympiad = Olympiad.query.get_or_404(olympiad_id)

    if session.get("user_type") != "participant" or not check_acc(current_user.participant_code):
        logout_user()
        return redirect(url_for("main.register_organizer"))

    status_raw = current_user.status

    if status_raw not in ["completed-A", "completed-W"]:
        return "Вы не являетесь победителем или призёром, поэтому диплом получить не можете..."

    name = current_user.participant_name
    grade = current_user.grade
    code = current_user.participant_code
    status = "Призёр" if status_raw == "completed-A" else "Победитель"

    olymp_con = Olympiad.query.filter(Olympiad.id == olympiad_id).first()
    olymp_name = olymp_con.name
    olymp_level = olymp_con.level

    if os.path.exists(f"app/funcs/output/diploma_{current_user.id}.pdf"):
        os.remove(f"app/funcs/output/diploma_{current_user.id}.pdf")

    create_diploma_pdf(filename=f"app/funcs/output/diploma_{current_user.id}.pdf",
                       name=name,
                       participant_code=code,
                       grade=grade,
                       olympiad_name=olymp_name,
                       olympiad_level=olymp_level,
                       date=datetime.date.today(),
                       status_by_res=status
                       )
    path = f"funcs\\output\\diploma_{current_user.id}.pdf"
    return send_file(path, as_attachment=True)

@bp.route("/generate_blank/<int:olympiad_id>", methods=["GET", "POST"])
@login_required
def create_blank(olympiad_id):
    olympiad = Olympiad.query.get_or_404(olympiad_id)

    if session.get("user_type") != "organizer":
        code = current_user.participant_code
        id = current_user.id
    else:
        code = "Здесь будет отображен код участника"
        id = "from_organizer" + str(current_user.id)

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
