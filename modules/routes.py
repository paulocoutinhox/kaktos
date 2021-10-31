from flask.templating import render_template

from modules import system
from modules.system import flask_app


# -----------------------------------------------------------------------------
@flask_app.route("/")
def index(path=None):
    kaktos = system.get_kaktos("index")
    return render_template(f"pages/index.html", kaktos=kaktos)


# -----------------------------------------------------------------------------
@flask_app.route("/<path:path>/")
def page(path=None):
    kaktos = system.get_kaktos(path)
    return render_template(f"pages/{path}.html", kaktos=kaktos)


# -----------------------------------------------------------------------------
@flask_app.before_request
def before_request():
    pass
