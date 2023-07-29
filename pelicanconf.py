from pathlib import Path

from voltaire.pelican import *

SITENAME = "CodeSnipsPro"
PATH = "./CodeSnips"
PAGE_PATHS = [""]
ARTICLE_PATHS = ["articles"]
PAGE_EXCLUDES = ARTICLE_PATHS
FILENAME_METADATA = "(?P<title>.*)"

PLUGINS += ["voltaire.search"]
TEMPLATE_PAGES = {
    "search.html": "search/index.html",
}
INDEX_SAVE_AS = ""


STATIC_PATHS = [
    "../extra",
]
EXTRA_PATH_METADATA = {
    "../extra/CNAME": {"path": "CNAME"},
}

WEBASSETS_CONFIG = [
    ("SASS_LOAD_PATHS", [str(Path.cwd() / "node_modules")]),
    ("SASS_BIN", str(Path.cwd() / "node_modules" / ".bin" / "sass")),
    ("SASS_USE_SCSS", True),
]


MENUITEMS_START = (
    ("Home", "/"),
    ("Search", "/search/"),
)

MARKDOWN['extension_configs']['markdown.extensions.codehilite'] = {'css_class': 'highlight'}
