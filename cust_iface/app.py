from app import app


app.jinja_env.line_statement_prefix = '#'
if __name__ == "__main__":
    app.run(ssl_context="adhoc")
