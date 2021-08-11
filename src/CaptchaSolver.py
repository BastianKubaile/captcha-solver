from src.ImageReader import read_image

class CaptchaSolver:

    def __init__(self, letter_store):
        self.letter_store = letter_store

    def parse_image(self, img_path):
        pixels = read_image(img_path)
        print(pixels)


