"""Capture webcam and highlight beard areas needing shaving in realtime"""

import cv2
import numpy as np
import numpy.typing as npt

Cv2Image = npt.NDArray
BLUE, GREEN, RED = 0, 1, 2            # cv2 stores colors as BGR

def color_face_beard(original_image: Cv2Image) -> Cv2Image:
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)

    im = gray_image.copy()
    print('25th percentile:', np.percentile(gray_image, 25))
    upper_bound = 20   # np.percentile(gray_image, 25)
    im[im >= upper_bound] = 1
    im = im * 10    # (255 // upper_bound)      # enhance brightness

    # Convert the grayscale image to a 3-channel image
    gray_image_3c = cv2.merge([im, im, im])

    # Create a color image with the same dimensions as the grayscale image
    colored_hair_beard_image = np.zeros_like(gray_image_3c)
    colored_hair_beard_image[..., GREEN][im <= 80] = im[im <= 80]
    colored_hair_beard_image[..., BLUE][(80 <= im) & (im <= 160)] = im[(80 <= im) & (im <= 160)]
    colored_hair_beard_image[..., RED][(160 <= im) & (im <= 255)] = im[(160 <= im) & (im <= 255)]

    # overlay colored hair & beard on top of original image
    alpha = 0.5  # weight of the first image
    beta = 0.5   # weight of the second image
    gamma = 0    # scalar added to each sum
    blended_image = cv2.addWeighted(original_image, alpha, colored_hair_beard_image, beta, gamma)

    return blended_image

frame_delay = 1    # seconds
cap = cv2.VideoCapture(0)          # capture webcam video
while True:
    ret, frame = cap.read()
    transformed_frame = color_face_beard(frame)
    cv2.imshow('frame', transformed_frame)

    # Stop when close button of window is pressed
    if cv2.waitKey(frame_delay) and cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
