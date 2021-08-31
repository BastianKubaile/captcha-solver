from flask import Flask, request
from flask_caching import Cache
from uuid import uuid1
from os import system
from src.Customizable import captcha_is_solvable, reformat_captcha
from src.ImageReader import read_image
from src.LetterStore import LetterStore
from src.CaptchaSolver import CaptchaSolver

image_field_name = "captcha"
upload_directory = "uploaded_captchas"
letter_dir_path = "testing/data/letters"

# Create a empty upload directory
system(f"rm -r {upload_directory}")
system(f"mkdir {upload_directory}")

app = Flask(__name__)

cache = Cache(config={
    "CACHE_TYPE": "SimpleCache",
    "CACHE_DEFAULT_TIMEOUT": 9999
})
cache.init_app(app)

@cache.cached(key_prefix= "captcha_solver")
def get_captcha_solver():
    letter_store = LetterStore(letter_dir_path)
    return CaptchaSolver(letter_store)

@app.route("/solve", methods=['POST'])
def solve():
    if image_field_name not in request.files:
        pass  # TODO: Give some error message
    received_file = request.files[image_field_name]
    if not received_file:  # TODO: Check if file is of image type
        pass  # TODO: Give some error message

    saved_path = f"{upload_directory}/{uuid1()}.jpeg"
    image_file = open(saved_path, 'wb')
    received_file.save(image_file)
    image_file.close()

    captcha_image = read_image(saved_path)
    if not captcha_is_solvable(captcha_image):
        pass  # TODO: Give some error message
    captcha_image = reformat_captcha(captcha_image)

    solved_text = get_captcha_solver().parse_image(captcha_image)
    return {
        "solution": solved_text
    }


