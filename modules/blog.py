import glob
from datetime import datetime

import yaml

from modules import pagination


# -----------------------------------------------------------------------------
def by_token(token: str):
    from modules import config

    return next(
        (post for post in config.blog_data["posts"] if post["token"] == token),
        None,
    )


# -----------------------------------------------------------------------------
def load_data():
    blog_data = {
        "posts": [],
        "posts_pag": {},
    }

    # load post files
    posts_files = glob.glob("extras/config/posts/**/*.yml")

    for post_file in posts_files:
        with open(post_file, "r") as file:
            posts_data = yaml.safe_load(file)
            blog_data["posts"].extend(posts_data)

    # order by published_at desc
    if len(blog_data["posts"]):
        blog_data["posts"] = sorted(
            blog_data["posts"],
            key=lambda x: datetime.strptime(x["published_at"], "%Y-%m-%d %H:%M:%S"),
            reverse=True,
        )

    # pagination
    blog_data["posts_pag"] = pagination.paginate(blog_data["posts"], 6)

    return blog_data
