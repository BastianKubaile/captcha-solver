1. Read in Captcha Image
2. Read in Letter Images
3. Reform Letter Image to size of Captcha Image
3.1. Move Letter Image on x and y axis
3.2. Rotate Letter Image by n Pixels clock- and counterclockwise
3.3. Calculate a Mask of moved and rotated captcha image
4. Calculate Difference between reformed Letter Image on the masked pixels
5. Get the lowest Difference of all possible rotations
6. Find the lowest possible Difference out of all the letters
7. Return those letters 