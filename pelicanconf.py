from collections import defaultdict
from pathlib import Path
from typing import Any, Dict

from voltaire.pelican import *  # isort: skip

SITENAME = "CodeSnips"
PATH = "./CodeSnips"
PAGE_PATHS = [""]
ARTICLE_PATHS = ["articles"]
PAGE_EXCLUDES = ARTICLE_PATHS
FILENAME_METADATA = "(?P<title>.*)"

if "PLUGINS" not in globals():
    PLUGINS = []
PLUGINS += ["voltaire.search"]
TEMPLATE_PAGES = {
    "search.html": "search/index.html",
}
INDEX_SAVE_AS = ""
ARCHIVES_SAVE_AS = AUTHORS_SAVE_AS = CATEGORIES_SAVE_AS = TAGS_SAVE_AS = ""

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

if "MARKDOWN" not in globals():
    MARKDOWN: Dict[str, Dict[str, Any]] = defaultdict(dict)

MARKDOWN["extension_configs"]["markdown.extensions.codehilite"] = {
    "css_class": "highlight"
}
MARKDOWN["extension_configs"]["markdown.extensions.meta"] = {}
