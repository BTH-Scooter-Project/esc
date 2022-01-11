"""Main routes."""

from flask import Blueprint, render_template, request, url_for, redirect, flash
from flask_login import login_required, current_user
from markupsafe import escape

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Route index.

    Returns
    -------
        html-string: rendered template page.
    """
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    """Route profile.

    Returns
    -------
        [type]: [description]
    """
    return render_template('profile.html')


@main.route('/profile', methods=['POST'])
@login_required
def profile_post():
    """/profile route (POST).

    Returns
    -------
        [type]: [description]
    """
    response = current_user.update(
        email=escape(request.form.get('email')),
        balance=escape(request.form.get('balance')),
        payment=escape(request.form.get('payment')),
        password=escape(request.form.get('password'))
    )

    print(response)

    flash(response['message'])
    if response['status_code'] != 200:
        flash(response['detail'])
    return redirect(url_for('main.profile'))


@main.route('/travels')
@login_required
def travels():
    """Route showing travels.

    Returns
    -------
        [type]: [description]
    """
    travel_info = current_user.get_travel_info()
    return render_template('travels.html', travels=travel_info)
