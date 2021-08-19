from numpy import ndarray, zeros, matmul, subtract, absolute, sum, identity, iinfo
import numpy as np
import bisect
from typing import List, Tuple


DifferencePositionList = List[Tuple[float, int]]

class DifferenceCalculator:

    def __init__(self,
                 margin_left: int = 0,
                 margin_top: int = 0,
                 margin_right: int = 0,
                 margin_bottom: int = 0):
        self.margin_left = margin_left
        self.margin_top = margin_top
        self.margin_right = margin_right
        self.margin_bottom = margin_bottom

    def get_differences(self, captcha_image: ndarray,  letter_image: ndarray) -> DifferencePositionList:
        """ Returns a sorted List containing all possible DifferencePositions where the letter could be placed inside the Image.
        Each DifferencePosition contains a float between 0 and 1 describing how much the image fits at the position
        and the x value at which the image was fitted.
        The List is sorted by the difference value."""

        if letter_image.shape > captcha_image.shape:
            raise ValueError("The letter image is bigger than the captcha image")
        if not captcha_image.dtype == letter_image.dtype:
            raise ValueError("The Matrices representing both images must be of the same data type")

        positions_to_return: DifferencePositionList = []
        data_type = captcha_image.dtype

        l_h, l_w = letter_image.shape[0], letter_image.shape[1]  # Letter height and width
        i_h, i_w = captcha_image.shape[0], captcha_image.shape[1]  # Image height and width
        height_difference = i_h - l_h
        width_difference = i_w - l_w

        width_normalisation_matrix = zeros((l_w, i_w), dtype=data_type)
        height_normalisation_matrix = zeros((i_h, l_h), dtype=data_type)
        width_mask = zeros((i_w, i_w), dtype=data_type)
        height_mask = zeros((i_h, i_h), dtype=data_type)

        for x_offset in range(self.margin_left, width_difference + 1 - self.margin_right):
            width_normalisation_matrix.fill(0)
            width_normalisation_matrix[0:l_w, x_offset:x_offset + l_w] = identity(l_w, dtype=data_type)

            width_mask.fill(0)
            width_mask[x_offset:x_offset + l_w, x_offset: x_offset + l_w] = identity(l_w, dtype=data_type)
            min_difference = 1.0
            for y_offset in range(self.margin_top, height_difference + 1 - self.margin_bottom):
                height_normalisation_matrix.fill(0)
                height_normalisation_matrix[y_offset:y_offset + l_h, 0:l_h] = identity(l_h, dtype=data_type)

                height_mask.fill(0)
                height_mask[y_offset: l_h + y_offset, y_offset: l_h + y_offset] = identity(l_h, dtype=data_type)

                width_normalized = matmul(letter_image, width_normalisation_matrix)
                normalized_letter = matmul(height_normalisation_matrix, width_normalized)

                width_masked_image = matmul(captcha_image, width_mask)
                masked_image = matmul(height_mask, width_masked_image)

                current_difference = self._calculate_difference(masked_image, normalized_letter, l_w, l_h, data_type)
                if current_difference < min_difference:
                    min_difference = current_difference
            bisect.insort(positions_to_return, (min_difference, x_offset))

        return positions_to_return

    def _calculate_difference(self, masked_captcha_image: ndarray, normalized_letter_image: ndarray, letter_width: int, letter_height: int, data_type):
        max_data_value = iinfo(data_type).max
        max_possible_difference = max_data_value * letter_width * letter_height

        max_pixel_values = np.maximum(masked_captcha_image, normalized_letter_image)
        min_pixel_values = np.minimum(masked_captcha_image, normalized_letter_image)
        actual_difference = sum(subtract(max_pixel_values, min_pixel_values))
        return actual_difference / max_possible_difference
