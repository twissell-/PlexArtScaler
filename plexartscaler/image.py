from PIL import ImageFilter

from plexartscaler import config


def resize_image(image, width=None, height=None):
    x, y = image.size

    if width is None and height is None:
        raise ValueError("At least one of width or height must be specified")

    if height and width:
        new_width = width
        new_height = height
    elif height:
        h_percent = height / float(y)
        new_width = int((float(x) * float(h_percent)))
        new_height = height
    elif width:
        w_percent = width / float(x)
        new_height = int((float(y) * float(w_percent)))
        new_width = width

    background = image.resize((new_width, new_height))

    return background


def scale_image(image):
    x, y = image.size
    fill_color = (0, 0, 0)  # Transparent background

    if image.mode == "P":
        image = image.convert("RGB")

    if x > y:
        # Adjust width to WIDTH for landscape image
        image = resize_image(image, width=config.get("image.width"))
    else:
        # Adjust height to HEIGHT for portrait image
        image = resize_image(image, height=config.get("image.height"))
    x, y = image.size

    # Create a blurred background from the original image
    if x > y:
        background = resize_image(image, height=config.get("image.height"))
    else:
        background = resize_image(image, width=config.get("image.width"))

    # Center crop to target dimensions
    bg_x, bg_y = background.size
    left = (bg_x - config.get("image.width")) // 2
    top = (bg_y - config.get("image.height")) // 2
    right = left + config.get("image.width")
    bottom = top + config.get("image.height")
    background = background.crop((left, top, right, bottom))

    background = background.filter(
        ImageFilter.GaussianBlur(radius=config.get("image.blur_radius"))
    )

    # Paste the original image on top of the blurred background
    background.paste(
        image,
        (
            int((config.get("image.width") - x) / 2),
            int((config.get("image.height") - y) / 2),
        ),
    )

    return background
