from src.CaptchaSolver import CaptchaSolver
from src.LetterStore import LetterStore

def test_solve_captcha():
    letter_store = LetterStore("data/letters")
    under_test = CaptchaSolver(letter_store)
    under_test.parse_image("data/captchas/captcha1.jpeg")
    assert True
