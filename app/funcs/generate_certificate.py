from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def create_certificate_pdf(filename, participant_name, participant_code, olympiad_name, olympiad_id):
    # Используем шрифт с поддержкой кириллицы
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Рамка
    c.setLineWidth(4)
    c.setStrokeColorRGB(0.2, 0.4, 0.7)
    c.rect(20, 20, width-40, height-40)

    # Заголовок
    c.setFont("DejaVuSans", 38)
    c.setFillColorRGB(0.2, 0.2, 0.5)
    c.drawCentredString(width/2, height-90, "СЕРТИФИКАТ")

    # Текст сертификата
    c.setFont("DejaVuSans", 18)
    c.setFillColorRGB(0,0,0)
    c.drawCentredString(width/2, height-160, "подтверждает, что")
    c.setFont("DejaVuSans", 28)
    c.drawCentredString(width/2, height-200, participant_name)
    c.setFont("DejaVuSans", 18)
    c.drawCentredString(width/2, height-240, f"является участником олимпиады")
    c.setFont("DejaVuSans", 22)
    c.drawCentredString(width/2, height-275, f'"{olympiad_name}"')
    c.setFont("DejaVuSans", 16)

    # Место для подписи
    c.setFont("DejaVuSans", 14)
    c.drawString(width-300, 60, "__________________ (подпись)")

    # Код участника
    c.setFont("DejaVuSans", 10)
    c.drawString(30, 30, f"Код участника: {participant_code}")

    # id олимпиады
    c.setFont("DejaVuSans", 10)
    c.drawString(30, 60, f"ID олимпиады:{olympiad_id}")

    c.save()

# Пример использования
# create_certificate_pdf(
#     filename="certificate.pdf",
#     participant_name="Иванов Иван Иванович",
#     olympiad_name="Олимпиада по информатике",
# )
