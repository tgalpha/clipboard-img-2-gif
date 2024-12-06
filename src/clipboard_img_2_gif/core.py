import os
import tempfile
from PIL import ImageGrab, Image


def get_clipboard_image_or_path():
    """Retrieve image data or image path from the clipboard."""
    image = ImageGrab.grabclipboard()
    if isinstance(image, Image.Image):
        return image, None
    elif isinstance(image, list) and os.path.isfile(image[0]):
        # Process only first file in list
        return None, image[0]
    return None, None


def save_as_gif(image, path):
    """Save the provided image to the specified path in GIF format."""
    width, height = image.size
    width_height_size_limit = 500
    if max(width, height) > width_height_size_limit:
        scaling = width_height_size_limit / max(width, height)
        image = image.resize((int(width * scaling), int(height * scaling)))
    image = image.convert("RGB")
    image.save(path, format="GIF")


def copy_to_clipboard(filepath):
    """Copy the specified file as a file object to the clipboard."""
    command = f"powershell Set-Clipboard -LiteralPath {filepath}"
    os.system(command)


def main():
    image, path = get_clipboard_image_or_path()
    if not image and not path:
        print("No image or image file path found in clipboard.")
        return

    if path:
        image = Image.open(path)

    # Convert and save to temporary directory
    temp_dir = tempfile.gettempdir()
    gif_path = os.path.join(temp_dir, "converted.gif")
    save_as_gif(image, gif_path)

    # Copy GIF back to clipboard
    copy_to_clipboard(gif_path)
    print(f"GIF saved to {gif_path} and copied back to clipboard.")


if __name__ == "__main__":
    main()
