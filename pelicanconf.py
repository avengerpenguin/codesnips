from pathlib import Path

from voltaire.pelican import *

SITENAME = "CodeSnips"
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
    "../extra/android-chrome-512x512.png": {"path": "android-chrome-512x512.png"},
    "../extra/android-chrome-192x192.png": {"path": "android-chrome-192x192.png"},
    "../extra/apple-touch-icon.png": {"path": "apple-touch-icon.png"},
    "../extra/favicon-16x16.png": {"path": "favicon-16x16.png"},
    "../extra/favicon-32x32.png": {"path": "favicon-32x32.png"},
    "../extra/favicon.ico": {"path": "favicon.ico"},
    "../extra/site.webmanifest": {"path": "site.webmanifest"},
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
