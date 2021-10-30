import os
import sys

root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
build_dir = os.path.join(root_dir, "build")
template_dir = os.path.join(root_dir, "templates")

title = "Kaktos"
rtl = False

base_url = "https://kaktos.netlify.app"

page_og_locale = "en_US"
page_og_type = "website"
page_og_site_name = title
page_og_image = f"{base_url}/assets/images/logo-og.png"
page_og_image_width = "1024"
page_og_image_height = "1024"

page_twitter_card = "summary_large_image"
page_twitter_site = "@thepsf"

page_apple_mobile_web_app_title = title
page_application_name = title

version_js_file = "1"
version_css_file = "1"
