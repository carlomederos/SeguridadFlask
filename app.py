from flask import (
    Flask,
    render_template,
    redirect,
    url_for,
    flash,
    abort
)

from flask_wtf.csrf import CSRFProtect, CSRFError

from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    current_user,
    login_required
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config["SECRET_KEY"] = "clave_super_secreta"

app.config["SESSION_COOKIE_SECURE"] = True
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["REMEMBER_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

csrf = CSRFProtect(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."
login_manager.login_message_category = "warning"

class User(UserMixin):

    def __init__(self, id, username, password_hash):

        self.id = str(id)
        self.username = username
        self.password_hash = password_hash
users = {}

@login_manager.user_loader
def load_user(user_id):

    return users.get(user_id)

@app.route("/")
def index():

    return render_template(
        "index.html"
    )

@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegistrationForm()

    if form.validate_on_submit():
        for usuario in users.values():
            if usuario.username == form.username.data:
                flash(
                    "El nombre de usuario ya está registrado.",
                    "danger"
                )
                return render_template(
                    "register.html",
                    form=form
                )
            
        nuevo_id = str(len(users) + 1)

        password_hash = generate_password_hash(
            form.password.data
        )
        nuevo_usuario = User(
            id=nuevo_id,
            username=form.username.data,
            password_hash=password_hash
        )
        users[nuevo_id] = nuevo_usuario

        flash(
            "Registro exitoso.",
            "success"
        )

        return redirect(
            url_for("login")
        )

    return render_template(
        "register.html",
        form=form
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():

        usuario_encontrado = None

        for usuario in users.values():

            if usuario.username == form.username.data:
                usuario_encontrado = usuario
                break

        if usuario_encontrado and check_password_hash(
            usuario_encontrado.password_hash,
            form.password.data
        ):

            login_user(usuario_encontrado)

            flash(
                "Inicio de sesión correcto.",
                "success"
            )

            return redirect(
                url_for("index")
            )

        flash(
            "Credenciales inválidas.",
            "danger"
        )

    return render_template(
        "login.html",
        form=form
    )

@app.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "Sesión cerrada correctamente.",
        "success"
    )

    return redirect(
        url_for("login")
    )

@app.route("/profile")
@login_required
def profile():

    return render_template(
        "profile.html"
    )

@app.route("/test401")
def test401():

    abort(401)

@app.route("/test403")
def test403():

    abort(403)

@app.errorhandler(CSRFError)
def handle_csrf_error(error):

    return render_template(
        "csrf_error.html",
        reason=error.description
    ), 400

@app.errorhandler(401)
def error_401(error):

    return render_template(
        "401.html"
    ), 401

@app.errorhandler(403)
def error_403(error):

    return render_template(
        "403.html"
    ), 403

if __name__ == "__main__":
    app.run(
        debug=True,
        ssl_context="adhoc"
    )