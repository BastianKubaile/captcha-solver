from src.CaptchaSolver import CaptchaSolver
from src.LetterStore import LetterStore
from src.ImageReader import read_image

letter_store_path = "data/letters"
captcha_path = "data/captchas/captcha1.jpeg"
captcha_solution = "P6ZNEK"


def test_solves_first_captcha():
    letter_store = LetterStore(letter_store_path)
    under_test = CaptchaSolver(letter_store)
    solved_text = under_test.parse_image(read_image(captcha_path))
    assert solved_text == captcha_solution
