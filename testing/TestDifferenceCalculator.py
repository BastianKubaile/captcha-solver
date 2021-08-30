from src.DifferenceCalculator import DifferenceCalculator
from src.ImageReader import read_image

captcha_path = "data/captchas/captcha1.jpeg"
letter_paths = [
    "data/letters/P/noSerif.jpeg",
    "data/letters/6/noSerif.jpeg",
    "data/letters/Z/withSerif.jpeg",
    "data/letters/N/noSerif.jpeg",
    "data/letters/E/noSerif.jpeg",
    "data/letters/K/withSerif.jpeg"
]
expected_offsets_for_letters = [18, 57, 92, 137, 166, 209]
maximum_expected_difference = 0.1


def test_finds_correct_offsets_for_first_captcha():
    under_test = DifferenceCalculator(0, 0, 0, 0)
    captcha = read_image(captcha_path)
    letters = list(map(lambda letter_path: read_image(letter_path), letter_paths))
    for i in range(len(letters)):
        letter = letters[i]
        expected_offset = expected_offsets_for_letters[i]
        smallest_difference = under_test.get_differences(captcha, letter)[0]
        actual_difference, actual_offset = smallest_difference[0], smallest_difference[1]
        assert expected_offset == actual_offset
        assert actual_difference < maximum_expected_difference
