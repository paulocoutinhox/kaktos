import glob
import os

import yaml

from modules import time

# general
root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
build_dir = os.path.join(root_dir, "build")
template_dir = os.path.join(root_dir, "templates")

title = "Kaktos"
rtl = False
base_url = "https://kaktos.netlify.app"

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

# store data
store_data = {
    "categories": [],
    "products": [],
}

# load categories
with open("extras/config/categories.yml", "r") as file:
    store_data["categories"] = yaml.safe_load(file)

# load products
product_files = glob.glob("extras/config/products/**/*.yml")
for product_file in product_files:
    with open(product_file, "r") as file:
        product_data = yaml.safe_load(file)
        store_data["products"].append(product_data)
