#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
Kund gränssnitt
"""

from flask import Flask, render_template, request

app = Flask(__name__)
app.jinja_env.line_statement_prefix = '#'

@app.route("/")
def main():
    """
    Home route
    Shows a table of all accounts and their information.
    """
    return render_template("index.html", accounts=bank.accounts, customers=bank.customers)


@app.route("/history", methods=["GET"])
def history():
    """
    Route for showing travel history with payments
    """
    message = None

    return render_template(
        "history.html",
        accounts=bank.accounts,
        message=message
    )


@app.route("/account", methods=["POST", "GET"])
def account():
    """
    Route to manage customer account
    """
    message = None
    if request.method == "POST":
        if bank.connect(request.form):
            bank.save_data()
            message = "Connected account #{account} to customer '{customer}'".format(
                account=request.form["account"],
                customer=request.form["person"],
            )
        else:
            message = "Account #{account} is already connected to the customer '{customer}'".format(
                account=request.form["account"],
                customer=request.form["person"],
            )

    return render_template(
        "account.html",
        accounts=bank.accounts,
        persons=bank.customers,
        message=message
    )
