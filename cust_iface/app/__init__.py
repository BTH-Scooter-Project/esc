# init.py

from flask import Flask
from flask_login import LoginManager
from .models import Customer
from .auth import auth as auth_blueprint  # blueprint for auth routes in our app
from .main import main as main_blueprint  # blueprint for non-auth parts of app

app = Flask(__name__)

app.config['SECRET_KEY'] = '3cd9b4db035a5eea10ebc75ea8f701891dfaf8a129f7790aa9ba1523adc1aaaf'


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.unauthorized_handler
def unauthorized():
    return "You must be logged in to access this content.", 403


@login_manager.user_loader
def load_user(user_id):
    """Check whether customer exists.
    Returns:
        Customer: Customer-object
    """
    # since the customer_id is just the primary key of our customer table,
    # use it in the query for the customer
    return Customer.get_customer_by_id(user_id)


app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)
