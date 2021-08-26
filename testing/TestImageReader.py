from src.ImageReader import read_image

test_image_path = "data/50x50_white_with_black_pixel_at_6_10.jpeg"
test_image_shape = (50, 50)
test_image_background_color = 255
test_image_pixel_color = 0
test_image_pixel_coordinates = (6, 10)


def test_reads_right_dimensions_and_colors():
    under_test = read_image(test_image_path)
    assert under_test.shape == test_image_shape
    for i in range(test_image_shape[0]):
        for j in range(test_image_shape[1]):
            if i == test_image_pixel_coordinates[0] and j == test_image_pixel_coordinates[1]:
                assert _values_are_close_enough(under_test[i][j], test_image_pixel_color)
            else:
                assert _values_are_close_enough(under_test[i][j], test_image_background_color)


def _values_are_close_enough(val1, val2, maximum_allowed_difference=2):
    return val1 - val2 <= maximum_allowed_difference if val1 >= val2 else val2 - val1 <= maximum_allowed_difference
