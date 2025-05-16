from app.models import Participant


def check_acc(code):
    acc = Participant.query.filter(Participant.participant_code == code).first()
    if acc:
        return True
    else:
        return  False