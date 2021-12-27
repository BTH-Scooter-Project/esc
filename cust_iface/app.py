"""ESC-main python file."""

from project import app


app.jinja_env.line_statement_prefix = '#'
if __name__ == "__main__":
    app.run(debug=True, ssl_context="adhoc")
    # app.run(ssl_context="adhoc")
