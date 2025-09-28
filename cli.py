#!/usr/bin/env python3

import os
from ntpath import basename

import typer
from PIL import Image
from typing_extensions import Annotated

from plexartscaler import config, image, plex

pas = typer.Typer(name="plexartscaler", no_args_is_help=True, add_completion=False)


def _process(item, upload):
    ratio = config.get("image.width") / config.get("image.height")
    output_dir = config.get("output_dir")

    if not item.artUrl:
        print(f"Skipping {item.title}. No art URL found.")
        return

    original_file = plex.download_art(item)
    original_image = Image.open(original_file)

    if original_image.size[0] / original_image.size[1] != ratio:

        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        print(f"Processing {item.title}")
        background = image.scale_image(original_image)
        # background_file = os.path.join(output_dir, hash_item(item) + ".png")
        background_file = os.path.join(
            output_dir, basename(original_file).replace(".jpg", ".png")
        )
        background.save(background_file)

        if upload:
            item.uploadArt(filepath=background_file)
    else:
        print(f"Skipping {item.title}. Already correct ratio.")
        os.remove(original_file)


@pas.command(help="Scales a single item.")
def scale(
    title: Annotated[str, typer.Argument(help="The title to search.")],
    upload: bool = typer.Option(False, help="Upload the art."),
    library: str = typer.Option("", help="The library to search the item in."),
    verbose: bool = typer.Option(False),
):
    items = plex.search_library_item(title, library)
    if not items:
        print(f"No items found.")
        exit()

    total = len(items)
    processed = 0
    for item in items:
        processed += 1
        print(f"({processed}/{total})", end=" ")
        _process(item, upload)


@pas.command(help="Scales all items in a library.")
def scale_all(
    upload: bool = typer.Option(False, help="Upload the art."),
    library: str = typer.Option("", help="The library to search the item in."),
    verbose: bool = typer.Option(False),
):
    items = plex.get_library_items(library)
    if not items:
        print(f"No items found.")
        exit()

    total = len(items)
    processed = 0
    for item in items:
        processed += 1
        print(f"({processed}/{total})", end=" ")
        _process(item, upload)


if __name__ == "__main__":
    pas()
