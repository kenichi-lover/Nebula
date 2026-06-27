import re


def generate_slug(text: str) -> str:

    slug = text.lower()

    slug = re.sub(
        r"[^a-z0-9]+",
        "-",
        slug
    )

    return slug.strip("-")