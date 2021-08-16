from src.ImageReader import read_image
from src.LetterStore import LetterStore
from src.DifferenceCalculator import get_minimum_difference

class CaptchaSolver:

    def __init__(self, letter_store: LetterStore):
        self.letter_store: LetterStore = letter_store

    def parse_image(self, img_path: str):
        captcha_image = read_image(img_path)

        for letter in self.letter_store.get_letters():
            for letter_image in self.letter_store.get_images(letter):
                get_minimum_difference(captcha_image, letter_image)

