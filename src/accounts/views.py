from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, session, url_for, jsonify
from flask_login import login_required, login_user, logout_user, current_user

# App package imports
from src.utils.decorators import logout_required, admin_required
from src.utils.email import send_email
from model import bcrypt, db, oauth

# Relative imports to avoid conflicts with Pypy packages
from .forms import LoginForm, RegisterForm
from .models import User
from .token import generate_token, confirm_token


accounts_bp = Blueprint("accounts", __name__, template_folder='../templates')


@accounts_bp.route("/register", methods=["GET", "POST"])
@logout_required
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(name=form.name.data, email=form.email.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()

        send_confirmation_email(user)

        return redirect(url_for("accounts.inactive"))

    return render_template("accounts/register.html", form=form)


@accounts_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, request.form["password"]):
            login_user(user)
            return redirect(url_for("core.index"))
        else:
            flash("Invalid email and/or password.", "danger")
            return render_template("accounts/login.html", form=form)
    return render_template("accounts/login.html", form=form)


@accounts_bp.route('/login/google')
def login_google():
    redirect_uri = url_for('accounts.auth_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)


@accounts_bp.route('/auth/google')
def auth_google():
    token = oauth.google.authorize_access_token()
    userinfo = token['userinfo']
    session['user'] = userinfo

    name = userinfo['name']
    email = userinfo['email']
    password = token['access_token']

    user = User.query.filter_by(email=email).first()
    if not user:
        user = User(name=name, email=email, password=password, is_confirmed=True, confirmed_on=datetime.now())
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for("core.index"))


@accounts_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You were logged out.", "success")
    return redirect(url_for("accounts.login"))


@accounts_bp.route("/confirm/<token>")
@login_required
def confirm_email(token):
    if current_user.is_confirmed:
        flash("Account already confirmed.", "success")
        return redirect(url_for("core.index"))
    email = confirm_token(token)
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if user.email == email:
        user.is_confirmed = True
        user.confirmed_on = datetime.now()
        db.session.add(user)
        db.session.commit()
        flash("You have confirmed your account. Thanks!", "success")
    else:
        flash("The confirmation link is invalid or has expired.", "danger")
    return redirect(url_for("core.index"))


@accounts_bp.route("/inactive")
@login_required
def inactive():
    if current_user.is_approved:
        return redirect(url_for("core.index"))
    elif current_user.is_confirmed:
        return render_template("accounts/unapproved.html")
    else:
        return render_template("accounts/inactive.html")


@accounts_bp.route("/resend")
@login_required
def resend_confirmation():
    """Route for sending confirmation email."""
    if current_user.is_confirmed:
        flash("Your account has already been confirmed.", "success")
        return redirect(url_for("core.index"))

    send_confirmation_email(current_user)

    return redirect(url_for("accounts.inactive"))


def send_confirmation_email(user):
    token = generate_token(user.email)
    confirm_url = url_for("accounts.confirm_email", token=token, _external=True)
    html = render_template("accounts/confirm_email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(user.email, subject, html)

    login_user(user)

    flash("A confirmation email has been sent via email.", "success")


@accounts_bp.route('/users')
@login_required
@admin_required
def users_list():
    # Načteme všechny uživatele z databáze
    users = User.query.all()
    return render_template("accounts/users.html", users=users)


@accounts_bp.route('/update_approval', methods=['POST'])
@login_required
@admin_required
def update_approval():
    data = request.get_json()
    user_id = data.get('user_id')
    is_approved = data.get('is_approved')

    # Najdi uživatele podle ID a aktualizuj jeho is_approved hodnotu
    user = User.query.get(user_id)
    if user:
        user.is_approved = is_approved
        db.session.commit()
        return jsonify({'message': 'Schválení aktualizováno.'}), 200
    else:
        return jsonify({'message': 'Uživatel nenalezen.'}), 404