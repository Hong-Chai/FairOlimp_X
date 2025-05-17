from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas


def create_blank_pdf(filename, participant_code, olympiad_id, date):

    pdfmetrics.registerFont(TTFont('DejaVuSans', 'app/funcs/DejaVuSans.ttf'))

    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Заголовок
    c.setFont("DejaVuSans", 20)
    c.drawCentredString(width / 2, height - 70, f"Бланк участника олимпиады")

    # Информация об олимпиаде
    c.setFont("DejaVuSans", 14)
    c.drawString(70, height - 120, f"id олимпиады: {olympiad_id}")
    c.drawString(70, height - 180, f"Дата проведения: {date}")

    # Данные участника
    c.drawString(70, height - 150, f"Код участника: {participant_code}")

    # Поле для подписи
    c.drawString(70, height - 240, "Подпись участника: ________________________")

    # Поле для работы
    c.drawString(70, height - 320, "Ответы:")

    # Линии для ответов
    y = height - 350
    for _ in range(20):  # 20 строк для ответов
        c.line(70, y, width - 70, y)
        y -= 25

    c.save()


# create_blank_pdf(
#     filename="olympiad_form.pdf",
#     olympiad_id="1",
#     date="16.05.2025",
#     participant_code="123"
# )