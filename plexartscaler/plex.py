import hashlib
import os
import time

import requests
from plexapi.server import PlexServer

from plexartscaler import config

_plex_server = PlexServer(config.get("plex.url"), config.get("plex.token"))


def hash_item(item):
    return hashlib.md5(f"{item.year}-{item.title}".encode("utf-8")).hexdigest()


def download_art(item, download_dir=config.get("backup_dir")):

    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    filename = os.path.join(download_dir, f"{hash_item(item)}-{int(time.time())}.jpg")
    response = requests.get(item.artUrl)
    with open(filename, "wb") as file:
        file.write(response.content)

    return filename


def get_library_items(library=None):
    if not library:
        libraries = config.get("plex.libraries")
    else:
        libraries = [library]

    rtn = []
    for library_name in libraries:
        rtn += _plex_server.library.section(library_name).all()
    return rtn


def search_library_item(title, library=None):
    if not library:
        libraries = config.get("plex.libraries")
    else:
        libraries = [library]

    for library_name in libraries:
        items = _plex_server.library.section(library_name).search(title)
        if items:
            return items

    raise ValueError(f"Item {title} not found.")
