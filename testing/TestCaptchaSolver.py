from src.CaptchaSolver import CaptchaSolver

def test_solve_captcha():
    underTest = CaptchaSolver()
    underTest.parse_image("data/captcha1.jpeg")
    assert True
