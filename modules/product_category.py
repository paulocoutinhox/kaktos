import glob

import yaml


# -----------------------------------------------------------------------------
def by_token(token: str):
    from modules import config

    return next(
        (
            category
            for category in config.product_category_data
            if category["token"] == token
        ),
        None,
    )


# -----------------------------------------------------------------------------
def load_data():
    data = []

    files = glob.glob("extras/config/product/category/**/*.yml")

    for file in files:
        with open(file, "r") as f:
            data.extend(yaml.safe_load(f))

    return data
