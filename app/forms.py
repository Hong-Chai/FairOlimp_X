from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, SelectField, FileField
from wtforms.validators import DataRequired, Email, Length


class OrganizerRegistrationForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()],)
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
    logo = FileField('Логотип', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Только изображения!')
    ])
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