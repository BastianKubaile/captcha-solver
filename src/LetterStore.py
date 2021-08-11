from os import listdir
from os.path import isdir, isfile
from src.ImageReader import read_image


class LetterStore:

    def __init__(self, letter_path):
        self.letter_pixels = {}

        letter_dirs_and_names = [(letter_path + "/" + directory_name, directory_name)
                                 for directory_name in listdir(letter_path)
                                 if isdir(letter_path + "/" + directory_name)]

        for (letter_dir, letter_name) in letter_dirs_and_names:
            letter_files = [letter_dir + "/" + letter_filename
                            for letter_filename in listdir(letter_dir)
                            if isfile(letter_dir + "/" + letter_filename)]

            for letter_file in letter_files:
                if letter_name in self.letter_pixels:
                    self.letter_pixels[letter_name].append(read_image(letter_file))
                else:
                    self.letter_pixels[letter_name] = [read_image(letter_file)]
