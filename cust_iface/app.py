"""ESC-main python file."""

from project import app


app.jinja_env.line_statement_prefix = '#'
if __name__ == "__main__":
    app.run(debug=True)
    # app.run(ssl_context="adhoc")
