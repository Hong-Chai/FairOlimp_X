from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    SelectField,
    FileField,
    IntegerField,
    TextAreaField,
    FloatField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional


class OrganizerRegistrationForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()],
    )
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Зарегистрироваться")


class OrganizerLoginForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class OlympiadSettingsForm(FlaskForm):
    name = StringField("Название", validators=[DataRequired()])
    subject = StringField("Предмет", validators=[DataRequired()])
    level = StringField("Уровень")
    grades = StringField("Классы (через запятую)", validators=[DataRequired()])
    logo = FileField(
        "Логотип", validators=[FileAllowed(["jpg", "png"], "Только изображения!")]
    )
    delete_logo = SubmitField("Удалить логотип")
    submit = SubmitField("Сохранить")


class ParticipantRegistrationForm(FlaskForm):
    name = StringField("ФИО", validators=[DataRequired(), Length(min=2, max=150)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    grade = SelectField("Класс", validators=[DataRequired()])
    password = PasswordField("Пароль", validators=[DataRequired(), Length(min=6)])
    submit = SubmitField("Зарегистрироваться")


class ParticipantLoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Пароль", validators=[DataRequired()])
    submit = SubmitField("Войти")


class WorkUploadForm(FlaskForm):
    work_file = FileField(
        "Файл работы",
        validators=[
            FileRequired(),
            FileAllowed(["pdf", "jpg", "png"], "Только PDF или изображения!"),
        ],
    )
    submit = SubmitField("Загрузить")


class EvaluationForm(FlaskForm):
    score = IntegerField("Оценка", validators=[DataRequired(), NumberRange(min=0)])
    comments = TextAreaField("Комментарий", validators=[Optional()])
    submit = SubmitField("Сохранить оценку")


class AppealForm(FlaskForm):
    appeal_text = TextAreaField("Текст апелляции", validators=[DataRequired()])
    submit = SubmitField("Отправить апелляцию")


class OrganizerCommentForm(FlaskForm):
    comment = TextAreaField("Комментарий к апелляции", validators=[DataRequired()])
    submit = SubmitField("Отправить комментарий")


class OlympiadStatusForm(FlaskForm):
    status = SelectField(
        "Статус олимпиады",
        choices=[
            ("draft", "Черновик"),
            ("registration", "Регистрация"),
            ("registration ended", "Регистрация завершена"),
            ("checking", "Проверка"),
            ("appeal", "Апелляция"),
            ("completed", "Завершена"),
        ],
        validators=[DataRequired()],
    )
    submit = SubmitField("Изменить статус")


class RankingForm(FlaskForm):
    winners_percent = FloatField(
        "Процент победителей",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=100, message="Процент должен быть от 0 до 100"),
        ],
    )
    awardees_percent = FloatField(
        "Процент призеров",
        validators=[
            DataRequired(),
            NumberRange(min=0, max=100, message="Процент должен быть от 0 до 100"),
        ],
    )
    submit = SubmitField("Пересчитать рейтинги")
