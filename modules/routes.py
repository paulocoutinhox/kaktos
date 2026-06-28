import glob
import os
from datetime import datetime, timezone
from pathlib import Path

import yaml
from flask import Response
from flask.templating import render_template

from modules import blog as m_blog
from modules import config, pagination
from modules import product as m_product
from modules import product_category as m_product_category
from modules import system, time
from modules.system import flask_app

SITEMAP_EXCLUDED_PATHS = {"index", "product", "product-category", "blog-post"}


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
def file_lastmod(path):
    return datetime.fromtimestamp(Path(path).stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d")


# -----------------------------------------------------------------------------
def token_lastmods(pattern):
    # map each item token to the modification date of its source yml file
    lastmods = {}

    for file_path in glob.glob(pattern):
        last = file_lastmod(file_path)

        with open(file_path, "r") as f_in:
            data = yaml.safe_load(f_in)

        items = data if isinstance(data, list) else [data]

        for item in items:
            lastmods[item["token"]] = last

    return lastmods


# -----------------------------------------------------------------------------
@flask_app.route("/sitemap.xml")
def sitemap():
    pages_dir = Path(config.template_dir) / "pages"
    base = config.base_url.rstrip("/")

    # home reflects the index template change time
    urls = [{"loc": f"{base}/", "lastmod": file_lastmod(pages_dir / "index.html")}]

    # static pages use their template modification date
    for p in sorted(pages_dir.rglob("*.html")):
        rel = p.relative_to(pages_dir).with_suffix("")
        path = str(rel).replace(os.sep, "/")
        if path in SITEMAP_EXCLUDED_PATHS:
            continue
        urls.append({"loc": f"{base}/{path}/", "lastmod": file_lastmod(p)})

    # blog posts use their published date
    for post in config.blog_data["posts"]:
        published_at = post["published_at"]
        urls.append(
            {
                "loc": f"{base}/blog/{time.format_datetime(published_at, '%Y')}/{int(time.format_datetime(published_at, '%m'))}/{int(time.format_datetime(published_at, '%d'))}/{post['token']}/",
                "lastmod": time.format_datetime(published_at, "%Y-%m-%d"),
            }
        )

    # categories and products use their source yml modification date
    category_lastmods = token_lastmods("extras/config/product/category/**/*.yml")
    product_lastmods = token_lastmods("extras/config/product/items/**/*.yml")
    category_fallback = file_lastmod(pages_dir / "product-category.html")
    product_fallback = file_lastmod(pages_dir / "product.html")

    for category in config.product_category_data:
        token = category["token"]
        urls.append({"loc": f"{base}/product-category/{token}/", "lastmod": category_lastmods.get(token, category_fallback)})

    for prod in config.product_data:
        token = prod["token"]
        urls.append({"loc": f"{base}/product/{token}/", "lastmod": product_lastmods.get(token, product_fallback)})

    xml = render_template("sitemap.xml", urls=urls)
    return Response(xml, mimetype="application/xml")


# -----------------------------------------------------------------------------
@flask_app.route("/robots.txt")
def robots():
    base = config.base_url.rstrip("/")
    body = f"User-agent: *\nAllow: /\n\nSitemap: {base}/sitemap.xml\n"
    return Response(body, mimetype="text/plain")


# -----------------------------------------------------------------------------
@flask_app.before_request
def before_request():
    pass
