from flask import Flask, request
from uuid import uuid1
from os import system
from src.Customizable import captcha_is_solvable, reformat_captcha
from src.ImageReader import read_image

app = Flask(__name__)

image_field_name = "captcha"
upload_directory = "uploaded_captchas"

# Create a empty upload directory
system(f"rm -r {upload_directory}")
system(f"mkdir {upload_directory}")


@app.route("/solve", methods=['POST'])
def solve():
    if image_field_name not in request.files:
        pass  # TODO: Give some error message
    received_file = request.files[image_field_name]
    if received_file:  # TODO: Check if file is of image type
        saved_path = f"{upload_directory}/{uuid1()}.jpeg"
        image_file = open(saved_path, 'wb')
        received_file.save(image_file)
        image_file.close()

        captcha_image = read_image(saved_path)
        if not captcha_is_solvable(captcha_image):
            pass  # TODO: Give some error message
        captcha_image = reformat_captcha(captcha_image)

    return {
        "solution": "foobar"
    }


