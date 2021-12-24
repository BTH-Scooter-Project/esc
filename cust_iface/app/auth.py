# auth.py

import os
import requests
from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from .models import Customer
from markupsafe import escape
from oauthlib.oauth2 import WebApplicationClient

auth = Blueprint('auth', __name__)

# Configuration
GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

# OAuth2 client setup
client = WebApplicationClient(GOOGLE_CLIENT_ID)


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
    if response['status_code'] != 201:
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


@auth.route("/login/callback")
def callback():
    """Google OAuth2 callback.

    Returns:
        [type]: [description]
    """

    # Get authorization code Google sent back to you
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send request to get tokens! Yay tokens!
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code,
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(GOOGLE_CLIENT_ID, GOOGLE_CLIENT_SECRET),
    )

    # Parse the tokens!
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Now that we have tokens (yay) let's find and hit URL
    # from Google that gives you user's profile information,
    # including their Google Profile Image and Email
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # We want to make sure their email is verified.
    # The user authenticated with Google, authorized our
    # app, and now we've verified their email through Google!
    if userinfo_response.json().get("email_verified"):
        unique_id = userinfo_response.json()["sub"]
        users_email = userinfo_response.json()["email"]
        users_name = userinfo_response.json()["given_name"]
    else:
        return "User email not available or not verified by Google.", 400

    # Create a user in our db with the information provided
    # by Google
    customer = Customer(
        id_=unique_id, name=users_name, email=users_email
    )

    # Doesn't exist? Add to database
    if not Customer.get(unique_id):
        Customer.create(unique_id, users_name, users_email)

    # Begin user session by logging the user in
    login_user(customer)

    # Send user back to homepage
    return redirect(url_for("main.profile"))


def get_google_provider_cfg():
    return requests.get(GOOGLE_DISCOVERY_URL).json()
