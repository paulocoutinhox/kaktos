from modules import config


# -----------------------------------------------------------------------------
def by_token(token: str):
    return next(
        (
            product
            for product in config.store_data["products"]
            if product["token"] == token
        ),
        None,
    )
