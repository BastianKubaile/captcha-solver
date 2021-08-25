import functools
from multiprocessing import Process, Array
from src.ImageReader import read_image
from src.LetterStore import LetterStore
from src.DifferenceCalculator import DifferenceCalculator, DifferencePositionList
from typing import List, Tuple, Dict
from ctypes import Structure, c_float, c_int, c_char
import yaml

config = yaml.safe_load(open("../config.yml"))

LetterFit = Tuple[float, int, str]


class LetterFitStructure(Structure):
    _fields_ = [("difference", c_float), ("x_offset", c_int), ("letter", c_char)]


class CaptchaSolver:

    def __init__(self,
                 letter_store: LetterStore,
                 letters_per_captcha: int = config['LettersPerCaptcha'],
                 possible_letter_duplicates_per_captcha: int = config['PossibleDuplicateLettersPerCaptcha'],
                 processes_to_use: int = config['ProcessesPerCaptchaSolver']):
        self.letter_store: LetterStore = letter_store
        self.difference_calculator = DifferenceCalculator()
        self.possible_duplicates: int = possible_letter_duplicates_per_captcha
        self.letters_per_captcha: int = letters_per_captcha
        self.processes_to_use: int = processes_to_use

    def parse_image(self, img_path: str) -> str:
        captcha_image = read_image(img_path)
        n_relevant_positions = len(self.letter_store.get_letters()) * self.possible_duplicates
        most_relevant_positions = Array(LetterFitStructure, n_relevant_positions)

        letters_for_each_process = [{} for _ in range(self.processes_to_use)]
        idx_process_to_use: int = 0
        for letter in self.letter_store.get_letters():
            letters_for_each_process[idx_process_to_use][letter] = self.letter_store.get_images(letter)
            idx_process_to_use = (idx_process_to_use + 1) % self.processes_to_use

        processes = [None for _ in range(self.processes_to_use)]
        idx_to_insert_solutions = 0
        for i in range(self.processes_to_use):
            processes[i] = Process(target=self._parse_image_for_letters,
                                   args=(letters_for_each_process[i], captcha_image, most_relevant_positions,
                                         idx_to_insert_solutions))
            idx_to_insert_solutions += len(letters_for_each_process[i]) * self.possible_duplicates

        for process in processes:
            process.start()
        for process in processes:
            process.join()

        sorted_by_difference = sorted(most_relevant_positions, key=lambda position: position.difference)
        useful_positions = sorted_by_difference[0: self.letters_per_captcha]
        sorted_by_x_offset = sorted(useful_positions, key=lambda position:  position.x_offset)
        captcha_string = functools.reduce(lambda reduced_value, position: reduced_value + position.letter.decode(),
                                          sorted_by_x_offset, "")
        return captcha_string

    def _parse_image_for_letters(self, letters: Dict[str, List], captcha_image, position_store, idx_to_start_inserting):
        curr_idx_to_insert = idx_to_start_inserting
        for letter in letters.keys():
            all_differences: DifferencePositionList = []

            for letter_image in letters[letter]:
                current_differences = self.difference_calculator.get_differences(captcha_image, letter_image)
                useful_differences = self._remove_covered_positions(current_differences, letter_image.shape[1],
                                                                    self.possible_duplicates)
                all_differences = sorted(useful_differences + all_differences)

            most_relevant_differences = all_differences[0: self.possible_duplicates]
            for difference in most_relevant_differences:
                position_store[curr_idx_to_insert].difference = difference[0]
                position_store[curr_idx_to_insert].x_offset = difference[1]
                position_store[curr_idx_to_insert].letter = letter.encode()
                curr_idx_to_insert += 1

    @staticmethod
    def _remove_covered_positions(raw_differences: DifferencePositionList, letter_width: int,
                                  n_positions_to_return: int):
        useful_positions: DifferencePositionList = []
        while len(useful_positions) < n_positions_to_return and raw_differences:
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
