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
    product_data = []

    product_files = glob.glob("extras/config/products/**/*.yml")

    for product_file in product_files:
        with open(product_file, "r") as file:
            product_data.append(yaml.safe_load(file))

    return product_data
