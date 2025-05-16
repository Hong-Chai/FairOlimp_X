from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas


def create_diploma_pdf(filename, name, participant_code, grade, olympiad_name, olympiad_level, date, status_by_res):
    # Регистрируем шрифт с поддержкой кириллицы
    pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

    # Используем альбомную ориентацию
    c = canvas.Canvas(filename, pagesize=landscape(A4))
    width, height = landscape(A4)

    # Рамка диплома
    c.setLineWidth(6)
    c.setStrokeColorRGB(0.3, 0.3, 0.7)
    c.rect(20, 20, width - 40, height - 40)

    # Заголовок "Диплом"
    c.setFont("DejaVuSans", 40)
    c.setFillColorRGB(0.1, 0.1, 0.5)
    c.drawCentredString(width / 2, height - 100, "ДИПЛОМ")

    # Тип диплома: Победитель/Призёр
    c.setFont("DejaVuSans", 30)
    c.setFillColorRGB(0.8, 0.2, 0.2)
    c.drawCentredString(width / 2, height - 160, status_by_res)

    # ФИО участника
    c.setFont("DejaVuSans", 24)
    c.setFillColorRGB(0, 0, 0)
    c.drawCentredString(width / 2, height - 260, name)

    # Школа, класс
    c.setFont("DejaVuSans", 18)
    c.drawCentredString(width / 2, height - 295, f"Ученику(це) {grade} класса")

    # Пишем за что диплом
    if olympiad_level is not None:
        text = f"За достижения в {olympiad_level[:-2] if olympiad_level.isalpha() else olympiad_level} этапе"
        c.setFont("DejaVuSans", 16)
        c.drawCentredString(width / 2, height - 335, text)
        c.setFont("DejaVuSans", 20)
        c.drawCentredString(width / 2, height - 370, f'Олимпиады: "{olympiad_name}"')
    else:
        text = f"За достижения в Олимпиаде: {olympiad_name}"
        c.setFont("DejaVuSans", 20)
        c.drawCentredString(width / 2, height - 335, text)

    # Дата и подпись
    c.setFont("DejaVuSans", 14)
    c.drawString(60, 60, f"Дата: {date}")
    c.drawRightString(width - 60, 60, "__________________ (подпись)")

    # Код участника
    c.setFont("DejaVuSans", 10)
    c.drawString(30, 30, f"Код участника: {participant_code}")

    c.save()


# create_diploma_pdf(filename="output/diploma.pdf",
#                    name="иван",
#                    participant_code="123",
#                    grade="7",
#                    olympiad_name="ама",
#                    olympiad_level="1",
#                    date="15",
#                    status_by_res="PObeditel"
#                    )