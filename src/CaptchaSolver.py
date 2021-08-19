import functools
from src.ImageReader import read_image
from src.LetterStore import LetterStore
from src.DifferenceCalculator import get_differences, DifferencePositionList
from typing import List, Tuple

LetterFits = Tuple[float, int, str]


class CaptchaSolver:

    def __init__(self,
                 letter_store: LetterStore,
                 letters_per_captcha: int = 6,
                 possible_letter_duplicates_per_captcha: int = 2):
        self.letter_store: LetterStore = letter_store
        self.possible_duplicates: int = possible_letter_duplicates_per_captcha
        self.letters_per_captcha: int = letters_per_captcha

    def parse_image(self, img_path: str) -> str:
        captcha_image = read_image(img_path)
        all_positions: List[LetterFits] = []

        for letter in self.letter_store.get_letters():

            all_differences: DifferencePositionList = []
            for letter_image in self.letter_store.get_images(letter):
                all_differences = sorted(get_differences(captcha_image, letter_image) + all_differences)

            useful_positions = self._find_useful_differences_positions(all_differences, letter_image.shape[1])
            to_append: List[LetterFits] = list(map(lambda x: (x[0], x[1], letter), useful_positions))
            all_positions = sorted(to_append + all_positions)
        most_relevant_positions = all_positions[0: self.letters_per_captcha]
        sorted_by_x_offset = sorted(most_relevant_positions, key=lambda x:  x[1])
        captcha_string = functools.reduce(lambda reduced_value, position: reduced_value + position[2],
                                          sorted_by_x_offset, "")
        return captcha_string

    def _find_useful_differences_positions(self, raw_differences: DifferencePositionList, letter_width: int):
        useful_positions: DifferencePositionList = []
        while len(useful_positions) < self.possible_duplicates and raw_differences:
            curr_difference_position = raw_differences.pop(0)
            is_covered = False
            for i in range(0, len(useful_positions)):
                x_offset = useful_positions[i][1]
                if x_offset - letter_width <= curr_difference_position[1] <= x_offset + letter_width:
                    is_covered = True
                    break
            if not is_covered:
                useful_positions.append(curr_difference_position)
        return useful_positions
