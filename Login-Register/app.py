
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    flash,
    session
)

from auth.logic_login_register import (
    register_user,
    login_user
)

app = Flask(__name__)
app.secret_key = "login_register_secret_key"


@app.route("/")
def index():
    return redirect(url_for("login"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username", "")
        email = request.form.get("email", "")
        password = request.form.get("password", "")

        success, message = register_user(
            username, email, password
        )

        flash(message)

        if success:
            return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        identifier = request.form.get("identifier", "")
        password = request.form.get("password", "")

        success, message = login_user(
            identifier, password
        )

        flash(message)

        if success:
            session["user"] = identifier
            return redirect(url_for("dashboard"))

    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect(url_for("login"))

    return f"""
        <h1>Login Berhasil!</h1>
        <p>Selamat datang, {session['user']}</p>
        <a href="/logout">Logout</a>
    """


@app.route("/logout")
def logout():
    session.pop("user", None)
    flash("Berhasil logout")
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=True)
