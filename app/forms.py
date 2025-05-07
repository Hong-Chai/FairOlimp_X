from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email


class OrganizerRegistrationForm(FlaskForm):
    username = StringField("Логин", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
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
