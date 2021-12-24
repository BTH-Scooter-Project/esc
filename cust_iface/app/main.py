# main.py

from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)


@main.route('/')
def index():
    """Route index.

    Returns:
        html-string: rendered template page.
    """
    return render_template('index.html')


@main.route('/profile')
@login_required
def profile():
    """Route profile.

    Returns:
        [type]: [description]
    """
    return render_template('profile.html')


@main.route('/profile')
@login_required
def login_post():
    """/profile route (PUT).

    Returns:
        [type]: [description]
    """

    response = current_user.update(
        balance=escape(request.form.get('balance')),
        payment=escape(request.form.get('payment')),
        password=escape(request.form.get('password'))
        )

    # check if customer actually exists
    if response['status_code'] != 200:
        flash(response['message'])
        flash(response['detail'])
        return redirect(url_for('main.profile'))

    print(response)
    # if the above check passes, then we know the customer has the right credentials
    return redirect(url_for('main.profile'))



@main.route('/travels')
@login_required
def travels():
    """Route travels.

    Returns:
        [type]: [description]
    """
    return render_template('travels.html')
