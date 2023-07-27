from pathlib import Path

from voltaire.pelican import *

SITENAME = "Code Snippets"
PATH = "./CodeSnips"
PAGE_PATHS = [""]
ARTICLE_PATHS = ["articles"]
PAGE_EXCLUDES = ARTICLE_PATHS
FILENAME_METADATA = "(?P<title>.*)"

PLUGINS += ["voltaire.search"]
TEMPLATE_PAGES = {
    "search.html": "search/index.html",
}

STATIC_PATHS = ["../extra"]
EXTRA_PATH_METADATA = {
    "../extra/CNAME": {"path": "CNAME"},
}

MENUITEMS_START = (
    ("Home", "/"),
    ("Search", "/search/"),
)

MARKDOWN['extension_configs']['markdown.extensions.codehilite'] = {'css_class': 'highlight'}