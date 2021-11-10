import os
import pathlib
from glob import glob
from shutil import copyfile

import sass
from calmjs.parse import es5
from dukpy import babel_compile

from modules import system


# -----------------------------------------------------------------------------
def minify_js(code):
    print("minifying js...")

    if system.is_debug():
        result = str(babel_compile(str(code))["code"])
        print("skip minify")
        return result
    else:
        result = str(es5(babel_compile(str(code))["code"]))
        print("minified")
        return result


# -----------------------------------------------------------------------------
def build_js():
    print("building js...")

    if not os.path.exists("build/assets/js"):
        os.makedirs("build/assets/js")

    for js_file in glob("files/js/**/*.js", recursive=True):
        with open(js_file, "r") as og:
            js_file_dest = pathlib.Path(js_file)
            js_file_dest = pathlib.Path(*js_file_dest.parts[1:])

            base_dir = os.path.dirname(f"build/assets/{js_file_dest}")

            if not os.path.exists(base_dir):
                os.makedirs(base_dir)

            with open(f"./build/assets/{js_file_dest}", "w") as b:
                b.write(minify_js(og.read()))

    print("done")


# -----------------------------------------------------------------------------
def build_styles():
    print("building styles...")

    if not os.path.exists("build/assets/css"):
        os.makedirs("build/assets/css")

    sass.compile(
        dirname=("./files/css", "./build/assets/css"), output_style="compressed"
    )

    for css_file in glob("files/css/**/*.css", recursive=True):
        css_file_dest = pathlib.Path(css_file)
        css_file_dest = pathlib.Path(*css_file_dest.parts[1:])

        base_dir = os.path.dirname(f"build/assets/{css_file_dest}")

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        copyfile(css_file, f"build/assets/{css_file_dest}")

    print("done")


# -----------------------------------------------------------------------------
def copy_images():
    print("copying images...")

    if not os.path.exists("build/assets/images"):
        os.makedirs("build/assets/images")

    for img_file in glob("files/images/**/*.*", recursive=True):
        img_file_dest = pathlib.Path(img_file)
        img_file_dest = pathlib.Path(*img_file_dest.parts[1:])

        base_dir = os.path.dirname(f"build/assets/{img_file_dest}")

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        copyfile(img_file, f"build/assets/{img_file_dest}")

    print("done")


# -----------------------------------------------------------------------------
def copy_custom():
    print("copying custom...")

    for custom_file in glob("files/custom/**/*", recursive=True):
        if not os.path.isfile(custom_file):
            continue

        custom_file_dest = pathlib.Path(custom_file)
        custom_file_dest = pathlib.Path(*custom_file_dest.parts[2:])

        base_dir = os.path.dirname(f"build/{custom_file_dest}")

        if not os.path.exists(base_dir):
            os.makedirs(base_dir)

        copyfile(custom_file, f"build/{custom_file_dest}")

    print("done")
