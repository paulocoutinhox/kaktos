import os

from modules import blog, product, product_category, time

# general
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
build_dir = os.path.join(root_dir, "build")
template_dir = os.path.join(root_dir, "templates")

title = "Kaktos"
rtl = False
base_url = "https://kaktos.pages.dev"

page_description = "Kaktos is a python static site generator"
page_keywords = "python, html, javascript, css, seo, site, static, generator, jamstack"
page_author = "Paulo Coutinho"
page_language = "en"

page_og_locale = "en_US"
page_og_type = "website"
page_og_site_name = title
page_og_image = f"{base_url}/assets/images/logo-og.png"
page_og_image_width = "1024"
page_og_image_height = "1024"

page_twitter_card = "summary_large_image"
page_twitter_site = "@paulocoutinhox"

page_apple_mobile_web_app_title = title
page_application_name = title

version_js_file = time.current_time()
version_css_file = time.current_time()

# product data
product_data = product.load_data()

# product category data
product_category_data = product_category.load_data()

# blog data
blog_data = blog.load_data()
