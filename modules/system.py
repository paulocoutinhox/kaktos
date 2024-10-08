import importlib
import os
import sys
from importlib import reload

from dotenv import find_dotenv, load_dotenv
from flask import Flask
from flask_frozen import Freezer
from livereload import Server
from pygemstones.io import file
from pygemstones.util import log

from modules import assets, blog, config, product, product_category, time

flask_app = None
freezer_app = None
force_debug = False


# -----------------------------------------------------------------------------
def is_debug():
    global force_debug

    if os.getenv("KAKTOS_DEBUG", False):
        return True
    else:
        return force_debug


# -----------------------------------------------------------------------------
def get_kaktos(path):
    class KaktosConfig(object):
        pass

    kc = KaktosConfig()

    kc.is_debug = is_debug()
    kc.config = reload(config)
    kc.path = path

    return kc


# -----------------------------------------------------------------------------
def setup():
    # load .env file
    load_dotenv(find_dotenv())

    # root
    if is_debug():
        print(f"environment mode: development")
    else:
        print(f"environment mode: production")

    print(f"root dir: {config.root_dir}")
    print(f"build dir: {config.build_dir}")
    print(f"template dir: {config.template_dir}")

    # load flask
    global flask_app

    flask_app = Flask(__name__, template_folder=config.template_dir)
    flask_app.url_map.strict_slashes = False

    flask_app.config["DEBUG"] = is_debug()
    flask_app.config["TEMPLATES_AUTO_RELOAD"] = is_debug()
    flask_app.config["FREEZER_BASE_URL"] = config.base_url
    flask_app.config["FREEZER_DESTINATION"] = config.build_dir

    flask_app.jinja_env.globals.update(product=product)
    flask_app.jinja_env.globals.update(product_category=product_category)
    flask_app.jinja_env.globals.update(blog=blog)

    flask_app.jinja_env.globals.update(file=file)
    flask_app.jinja_env.globals.update(time=time)
    flask_app.jinja_env.globals.update(path=os.path)
    flask_app.jinja_env.globals.update(is_debug=is_debug())
    flask_app.jinja_env.auto_reload = is_debug()

    # load freezer
    global freezer_app
    freezer_app = Freezer(flask_app)


# -----------------------------------------------------------------------------
def build_pages():
    print("building site...")

    freezer_app.freeze()

    assets.build_js()
    assets.build_styles()
    assets.copy_images()
    assets.copy_custom()

    print("building done")


# -----------------------------------------------------------------------------
def start_live_reload():
    print("starting dev...")

    server = Server()

    server.watch(os.path.join(config.root_dir, "templates"), build_pages)
    server.watch(os.path.join(config.root_dir, "files", "css"), assets.build_styles)
    server.watch(os.path.join(config.root_dir, "files", "js"), assets.build_js)
    server.watch(os.path.join(config.root_dir, "files", "images"), assets.copy_images)
    server.watch(os.path.join(config.root_dir, "files", "custom"), assets.copy_custom)
    server.watch(os.path.join(config.root_dir, "modules", "config.py"), build_pages)

    server.serve(root="build", port=5555)


# -----------------------------------------------------------------------------
def process_command():
    command_name = ""

    if len(sys.argv) > 1:
        command_name = sys.argv[1]

    command_params = {}

    if command_name == "":
        # use the default command
        from modules.commands.default import run

        run(command_params)
    else:
        try:
            # dynamically load the command module
            command_module = importlib.import_module(f"modules.commands.{command_name}")
            command_module.run(command_params)
        except ModuleNotFoundError:
            log.e(f"Command '{command_name}' not found.")


# -----------------------------------------------------------------------------
def initialize():
    # setup
    setup()

    # routes
    from modules.routes import before_request, index, page
