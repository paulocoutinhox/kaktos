from flask.templating import render_template

from modules import blog as m_blog
from modules import config, pagination
from modules import product as m_product
from modules import product_category as m_product_category
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
@flask_app.route("/product-category/<string:token>/")
def product_category(token):
    kaktos = system.get_kaktos("product-category")

    product_category_data = m_product_category.by_token(token)

    return render_template(
        f"pages/product-category.html",
        kaktos=kaktos,
        product_category_data=product_category_data,
    )


# -----------------------------------------------------------------------------
@flask_app.route("/product/<string:token>/")
def product(token):
    kaktos = system.get_kaktos("product")

    product_data = m_product.by_token(token)

    return render_template(
        f"pages/product.html",
        kaktos=kaktos,
        product_data=product_data,
    )


# -----------------------------------------------------------------------------
@flask_app.route("/blog/", defaults={"page_num": 1})
@flask_app.route("/blog/page/<int:page_num>/")
def blog(page_num):
    kaktos = system.get_kaktos("blog")

    pagination_data = config.blog_data["posts_pag"]["pages"]

    if page_num <= len(pagination_data):
        pagination_data = pagination_data[page_num - 1]
    else:
        pagination_data = pagination.empty("blog")

    return render_template(
        "pages/blog.html",
        kaktos=kaktos,
        pagination_data=pagination_data,
        page_num=page_num,
    )


# -----------------------------------------------------------------------------
@flask_app.route("/blog/<int:year>/<int:month>/<int:day>/<string:token>/")
def blog_post(year, month, day, token):
    kaktos = system.get_kaktos("blog-post")

    blog_post_data = m_blog.by_token(token)

    return render_template(
        "pages/blog-post.html",
        kaktos=kaktos,
        blog_post_data=blog_post_data,
    )


# -----------------------------------------------------------------------------
@flask_app.before_request
def before_request():
    pass
