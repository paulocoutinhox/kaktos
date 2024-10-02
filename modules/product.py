import glob

import yaml


# -----------------------------------------------------------------------------
def by_token(token: str):
    from modules import config

    return next(
        (product for product in config.product_data if product["token"] == token),
        None,
    )


# -----------------------------------------------------------------------------
def load_data():
    data = []

    files = glob.glob("extras/config/product/items/**/*.yml")

    for file in files:
        with open(file, "r") as f:
            data.append(yaml.safe_load(f))

    return data
