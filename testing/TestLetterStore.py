from os import listdir
import pytest
from src.LetterStore import LetterStore

letter_directory = "testing/data/letters"


def test_gets_all_files():
    under_test = LetterStore(letter_directory)

    number_of_letter_directories = len(listdir(letter_directory))
    assert len(under_test.get_letters()) == number_of_letter_directories

    for letter in under_test.get_letters():
        number_of_images = len(listdir(f"{letter_directory}/{letter}"))
        assert len(under_test.get_images(letter)) == number_of_images


def test_raises_value_error_on_unknown_letter():
    under_test = LetterStore(letter_directory)

    with pytest.raises(ValueError):
        under_test.get_images("a")
