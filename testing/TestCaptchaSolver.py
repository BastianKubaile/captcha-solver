from src.CaptchaSolver import CaptchaSolver


def test_solve_captcha():
    under_test = CaptchaSolver(None)
    under_test.parse_image("data/captchas/captcha1.jpeg")
    assert True
