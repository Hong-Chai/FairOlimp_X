import datetime

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
from reportlab.lib.colors import black, HexColor

# Регистрируем шрифт с поддержкой кириллицы
pdfmetrics.registerFont(TTFont('DejaVuSans', 'app/funcs/fonts_for_pdf/DejaVuSans.ttf'))

def generate_certificate(full_name, olympiad, level, grade, filename="app/funcs/certificate.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    # Фон
    c.setFillColor(HexColor("#f9f9f9"))
    c.rect(0, 0, width, height, fill=1)

    c.setFont("DejaVuSans", 50)
    c.setFillColor(black)
    c.drawCentredString(width / 2, height - 4*cm, "СЕРТИФИКАТ")

    c.setFont("DejaVuSans", 16)
    c.drawCentredString(width / 2, height - 6*cm, "подтверждает, что")

    c.setFont("DejaVuSans", 20)
    c.drawCentredString(width / 2, height - 8*cm, full_name)

    c.setFont("DejaVuSans", 16)
    c.drawCentredString(width / 2, height - 10*cm, f"обучающий(ай)ся {grade} класса")

    c.setFont("DejaVuSans", 16)
    c.drawCentredString(width / 2, height - 12*cm, f"принял(а) участие в")

    c.setFont("DejaVuSans", 20)
    c.drawCentredString(width / 2, height - 14*cm, f"{level[:-2] + 'ом' if level.isalpha() else level} "
                                                   f"этапе олимпиады:")

    c.setFont("DejaVuSans", 20)
    c.drawCentredString(width / 2, height - 16*cm, f"«{olympiad}»")

    c.setFont("DejaVuSans", 12)
    c.drawRightString(10*cm, 3*cm, "Подпись организатора: ___________")

    c.setFont("DejaVuSans", 10)
    c.drawCentredString(width/2, 1*cm, f"{datetime.date.today().year}")

    c.save()