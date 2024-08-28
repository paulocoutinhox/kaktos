from modules import config


# -----------------------------------------------------------------------------
def by_token(token: str):
    return next(
        (
            category
            for category in config.store_data["categories"]
            if category["token"] == token
        ),
        None,
    )
