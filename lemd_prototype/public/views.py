# -*- coding: utf-8 -*-
"""Public section, including homepage and signup."""
from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    # Added section for matplotlib plotting
    send_file,
    make_response
)
from flask_login import login_required, login_user, logout_user

from lemd_prototype.extensions import login_manager
from lemd_prototype.public.forms import LoginForm
from lemd_prototype.user.forms import RegisterForm
from lemd_prototype.user.models import User
from lemd_prototype.utils import flash_errors
# Added section for plotting input systems
from lemd_prototype.plots import plot_dist
from lemd_prototype.input_phaser import *
from lemd_prototype.mat_database import DpField, get_file

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET", "POST"])
def home():
    """Home page."""
    form = LoginForm(request.form)
    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    if request.method == "POST":
        if form.validate_on_submit():
            login_user(form.user)
            flash("You are logged in.", "success")
            redirect_url = request.args.get("next") or url_for("user.members")
            return redirect(redirect_url)
        else:
            flash_errors(form)
    return render_template("public/home.html", form=form)

# Test
@blueprint.route("/plot/distributions", methods=['GET'])
def figure_plot():
    structure = get_struct_from_mp("mp-1201492")
    distribution = extract_descrpt(structure)
    dist_fig = plot_dist(distribution)
    return send_file(dist_fig, attachment_filename='plog.png', mimetype='image/png')
# Test!

@blueprint.route("/logout/")
@login_required
def logout():
    """Logout."""
    logout_user()
    flash("You are logged out.", "info")
    return redirect(url_for("public.home"))


@blueprint.route("/register/", methods=["GET", "POST"])
def register():
    """Register new user."""
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        User.create(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
            active=True,
        )
        flash("Thank you for registering. You can now log in.", "success")
        return redirect(url_for("public.home"))
    else:
        flash_errors(form)
    return render_template("public/register.html", form=form)


@blueprint.route("/about/")
def about():
    """About page."""
    form = LoginForm(request.form)
    return render_template("public/about.html", form=form)


@blueprint.route("/testfile/")
def testfile(file_id=None):
    """test MongoDB"""
    file = DpField('Si', 'v1')
    file_id = str(file.get_dist())

    return render_template("mongotest.html", file=file_id)
