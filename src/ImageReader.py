from PIL import Image
from numpy import asarray


def read_image(img_path):
    img = Image.open(img_path)
    img_as_grayscale = img.convert("LA")
    img_as_matrix = asarray(img_as_grayscale)
    pixels = img_as_matrix[:, :, 0]  # each pixel contains two values, but only the first has the brightness value
    return pixels
