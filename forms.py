from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class RegistrationForm(FlaskForm):
    username = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired(),
            Length(
                min=3,
                max=30,
                message="El nombre debe tener entre 3 y 30 caracteres."
            )
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired(),
            Length(
                min=6,
                message="La contraseña debe tener al menos 6 caracteres."
            )
        ]
    )

    confirm_password = PasswordField(
        "Confirmar contraseña",
        validators=[
            DataRequired(),
            EqualTo(
                "password",
                message="Las contraseñas deben coincidir."
            )
        ]
    )

    submit = SubmitField("Registrarse")

class LoginForm(FlaskForm):
    username = StringField(
        "Nombre de usuario",
        validators=[
            DataRequired()
        ]
    )

    password = PasswordField(
        "Contraseña",
        validators=[
            DataRequired()
        ]
    )

    submit = SubmitField("Iniciar sesión")