from os import listdir
from os.path import isdir, isfile
from src.ImageReader import read_image


class LetterStore:

    def __init__(self, letter_path):
        self.letter_matrices = {}

        letter_dirs_and_names = [(letter_path + "/" + directory_name, directory_name)
                                 for directory_name in listdir(letter_path)
                                 if isdir(letter_path + "/" + directory_name)]

        for (letter_dir, letter_name) in letter_dirs_and_names:
            letter_files = [letter_dir + "/" + letter_filename
                            for letter_filename in listdir(letter_dir)
                            if isfile(letter_dir + "/" + letter_filename)]

            for letter_file in letter_files:
                if letter_name in self.letter_matrices:
                    self.letter_matrices[letter_name].append(read_image(letter_file))
                else:
                    self.letter_matrices[letter_name] = [read_image(letter_file)]

    def get_letters(self):
        return list(self.letter_matrices.keys())

    def get_images(self, letter: str):
        if letter not in self.letter_matrices:
            raise ValueError(f"There are no image matrix for the letter {letter}")
        return self.letter_matrices[letter]
