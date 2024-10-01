from flask.templating import render_template

from modules import config, system
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
@flask_app.route("/product-category/<string:token>/")
def product_category(token):
    kaktos = system.get_kaktos("product-category")
    return render_template(f"pages/product-category.html", kaktos=kaktos, token=token)


# -----------------------------------------------------------------------------
@flask_app.route("/product/<string:token>/")
def product(token):
    kaktos = system.get_kaktos("product")
    return render_template(f"pages/product.html", kaktos=kaktos, token=token)


# -----------------------------------------------------------------------------
@flask_app.route("/blog/", defaults={"page": 1})
@flask_app.route("/blog/page/<int:page>/")
def blog(page):
    kaktos = system.get_kaktos("blog")

    pagination_data = config.blog_data["posts_pag"]["pages"]

    if page <= len(pagination_data):
        pagination_data = pagination_data[page - 1]
    else:
        pagination_data = {
            "total_items": 0,
            "total_pages": 0,
        }

    return render_template(
        "pages/blog.html",
        kaktos=kaktos,
        pagination_data=pagination_data,
        page_num=page,
    )


# -----------------------------------------------------------------------------
@flask_app.route("/blog/<int:year>/<int:month>/<int:day>/<string:token>/")
def blog_post(year, month, day, token):
    kaktos = system.get_kaktos("blog-post")

    blog_post = next(
        (post for post in config.blog_data["posts"] if post.get("token") == token), None
    )

    return render_template(
        "pages/blog-post.html",
        kaktos=kaktos,
        blog_post=blog_post,
    )


# -----------------------------------------------------------------------------
@flask_app.before_request
def before_request():
    pass
