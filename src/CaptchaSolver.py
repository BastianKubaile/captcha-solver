from ImageReader import read_image

class CaptchaSolver:

    def parse_image(self, img_path):
        pixels = read_image(img_path)
        print(pixels)


