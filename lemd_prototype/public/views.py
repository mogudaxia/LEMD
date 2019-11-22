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
    # send_file,
    make_response
)
from flask_login import login_required, login_user, logout_user

from lemd_prototype.extensions import login_manager
from lemd_prototype.public.forms import LoginForm, InputForm
from lemd_prototype.user.forms import RegisterForm
from lemd_prototype.user.models import User
from lemd_prototype.utils import flash_errors
# Added section for plotting input systems
from lemd_prototype.createfigure import create_figure
from lemd_prototype.input_phaser import *
from lemd_prototype.mat_database import DpField, get_file

blueprint = Blueprint("public", __name__, static_folder="../static")


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID."""
    return User.get_by_id(int(user_id))


@blueprint.route("/", methods=["GET"])
def home():
    """Home page."""
    current_app.logger.info("Hello from the LEMD System")
    return render_template("public/home.html", form=LoginForm(), inputs=InputForm())


@blueprint.route("/login", methods=["POST"])
def login():
    """handle login"""
    form = LoginForm(request.form)
    # with open("POSCAR", "r") as samplefile:
    # sample_input = samplefile.read()
    # inputs = InputForm()

    current_app.logger.info("Hello from the home page!")
    # Handle logging in
    # if request.method == "POST":
    if form.validate_on_submit():
        login_user(form.user)
        flash("You are logged in.", "success")
        redirect_url = request.args.get("next") or url_for("user.members")
        return redirect(redirect_url)
    else:
        flash_errors(form)
    # structure = inputs.validate_data()
    # dist = extract_descrpt(structure)
    # script, div = create_figure(dist, 10)
    return render_template("public/home.html", form=form, inputs=InputForm())


@blueprint.route("/submitdata", methods=["POST"])
def submitdata():
    inputs = InputForm(request.form)
    flag, structure, title = inputs.validate_data()
    if flag == 1:
        flash_errors(inputs)
    elif flag == 2:
        flash_errors(inputs)
    dist = extract_descrpt(structure)
    script, div = create_figure(dist, title, 10)
    return render_template("public/home.html", form=LoginForm(request.form), inputs=inputs, script=script, div=div)


# Test
# @blueprint.route("/plot/distributions", methods=['GET'])
# def figure_plot():
#    structure = get_struct_from_mp("mp-1201492")
#    distribution = extract_descrpt(structure)
#    script, div = create_figure(distribution, 10)
#    return send_file(dist_fig, attachment_filename='plog.png', mimetype='image/png')
#    return render_template("public/home.html", )
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


@blueprint.route("/testfile/<file_id>")
@blueprint.route("/testfile/")
def testfile(file_id=None):
    """test MongoDB"""
    file = DpField('Si', 'v1')
    if file_id is not None:
        f = get_file(file_id)
        response = make_response(f.read())
        response.mimetype = 'application/octet-stream'
        return response
    with open("POSCAR", "r") as f:
        sf = f.read()

    return render_template("testfile.html", file=str(file.get_fileid()), sf=sf)
