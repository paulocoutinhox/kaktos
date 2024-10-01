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
    product_category_data = []

    with open("extras/config/product-categories.yml", "r") as file:
        product_category_data = yaml.safe_load(file)

    return product_category_data
