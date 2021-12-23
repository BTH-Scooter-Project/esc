# auth.py

from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from .models import Customer
from markupsafe import escape

auth = Blueprint('auth', __name__)


@auth.route('/login')
def login():
    """Login route.

    Returns:
        [type]: [description]
    """
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    """/login route (POST).

    Returns:
        [type]: [description]
    """
    credentials = dict(
        email=escape(request.form.get('email')),
        password=escape(request.form.get('password'))
    )

    response = Customer.login(
        email=credentials['email'],
        password=credentials['password']
        )

    # check if customer actually exists
    if response['status_code'] != 200:
        flash(response['message'])
        flash(response['detail'])
        return redirect(url_for('auth.login'))

    print(response)
    customer = Customer(response['id'], response['token'], response['user'])
    login_user(customer)
    # if the above check passes, then we know the customer has the right credentials
    return redirect(url_for('main.profile'))


@auth.route('/signup')
def signup():
    """Route signup (render template).

    Returns:
        [type]: [description]
    """
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    """Route signup (POST).

    Returns:
        [type]: [description]
    """
    customer = dict(
        email=request.form.get('email'),
        firstname=request.form.get('firstname'),
        lastname=request.form.get('lastname'),
    )

    # if this returns a customer, then the email already exists in database
    response = Customer.register(
        email=escape(request.form.get('email')),
        password=escape(request.form.get('password')),
        firstname=escape(request.form.get('firstname')),
        lastname=escape(request.form.get('lastname')),
        city_id=2
        )

    # if a customer is found, we want to redirect back to signup page so customer can try again
    if response['status_code'] != 200:
        flash(response['message'])
        flash(response['detail'])
        return redirect(url_for('auth.signup', customer=customer))

    return redirect(url_for('auth.login', customer=customer))


@auth.route('/logout')
@login_required
def logout():
    """Logout route.

    Returns:
        [type]: [description]
    """
    logout_user()
    Customer.customers = []
    return redirect(url_for('main.index'))
