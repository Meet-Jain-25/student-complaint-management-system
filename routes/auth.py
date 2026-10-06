from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash
)

from flask_login import (
    login_user,
    logout_user,
    login_required,
    current_user
)

from extensions import db, login_manager
from models.user import User


auth_bp = Blueprint(
    "auth",
    __name__,
    url_prefix="/auth"
)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


@auth_bp.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if not name or not email or not password:
            flash(
                "Please fill in all fields.",
                "error"
            )
            return render_template("register.html")

        existing_user = db.session.scalar(
            db.select(User).where(User.email == email)
        )

        if existing_user:
            flash(
                "An account with this email already exists.",
                "error"
            )
            return render_template("register.html")

        user = User(
            name=name,
            email=email,
            role="student"
        )

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash(
            "Registration successful. Please log in.",
            "success"
        )

        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for("home"))

    if request.method == "POST":

        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = db.session.scalar(
            db.select(User).where(User.email == email)
        )

        if user and user.check_password(password):

            login_user(user)

            next_page = request.args.get("next")

            if next_page:
                return redirect(next_page)

            return redirect(url_for("home"))

        flash(
            "Invalid email or password.",
            "error"
        )

    return render_template("login.html")


@auth_bp.route("/logout")
@login_required
def logout():

    logout_user()

    flash(
        "You have been logged out.",
        "success"
    )

    return redirect(url_for("home"))