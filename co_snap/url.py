import re


def get_name(url):
    return re.search("/app/p/([a-z]{3}-[a-z]{3})", url).group(1)
