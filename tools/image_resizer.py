# image_resizer.py

import os
from PIL import Image


def resize_image(img, size):
    """Resize an image while maintaining aspect ratio and adding padding if necessary."""
    img.thumbnail(size, Image.LANCZOS)
    background = Image.new("RGBA", size, (255, 255, 255, 0))
    offset = ((size[0] - img.size[0]) // 2, (size[1] - img.size[1]) // 2)
    background.paste(img, offset, img if img.mode == "RGBA" else None)
    return background


def resize_images(directory, size=(64, 64)):
    """
    Resize all PNG images in the specified directory to the given size.

    :param directory: Path to the directory containing images
    :param size: Tuple of (width, height) for the target size
    """
    for filename in os.listdir(directory):
        if filename.lower().endswith(".png"):
            file_path = os.path.join(directory, filename)
            try:
                with Image.open(file_path) as img:
                    # Convert to RGBA if the image is not already in that mode
                    if img.mode != "RGBA":
                        img = img.convert("RGBA")

                    new_img = resize_image(img, size)
                    new_img.save(file_path, "PNG")

                print(f"Resized {filename}")
            except Exception as e:
                print(f"Error processing {filename}: {str(e)}")


def main():
    image_directory = "./images"  # Change this to your image directory path
    target_size = (64, 64)  # Change this if you want a different size

    resize_images(image_directory, target_size)
    print("Image resizing completed.")


if __name__ == "__main__":
    main()
