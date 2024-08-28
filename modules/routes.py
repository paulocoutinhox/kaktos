from flask.templating import render_template

from modules import system
from modules.system import flask_app


# -----------------------------------------------------------------------------
@flask_app.route("/")
def index():
    kaktos = system.get_kaktos("index")
    return render_template(f"pages/index.html", kaktos=kaktos)


# -----------------------------------------------------------------------------
@flask_app.route("/<path:path>/")
def page(path=None):
    kaktos = system.get_kaktos(path)
    return render_template(f"pages/{path}.html", kaktos=kaktos)


# -----------------------------------------------------------------------------
@flask_app.route("/category/<string:token>/")
def category(token):
    kaktos = system.get_kaktos("category")
    return render_template(f"pages/category.html", kaktos=kaktos, token=token)


# -----------------------------------------------------------------------------
@flask_app.route("/product/<string:token>/")
def product(token):
    kaktos = system.get_kaktos("product")
    return render_template(f"pages/product.html", kaktos=kaktos, token=token)


# -----------------------------------------------------------------------------
@flask_app.before_request
def before_request():
    pass
