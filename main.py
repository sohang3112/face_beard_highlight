"""Capture webcam and highlight beard areas needing shaving in realtime"""
from typing import Any
from argparse import ArgumentParser
import os
import sys

import cv2
import numpy as np
import numpy.typing as npt
import face_recognition as fc

try:
    Cv2Image = npt.NDArray[np.int_]
except AttributeError:
    Cv2Image = Any

BLUE, GREEN, RED = 0, 1, 2            # cv2 stores colors as BGR

def extract_faces(original_image: Cv2Image) -> Cv2Image:
    """Extract faces in image, and turn the remaining background into white"""
    rgb_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    face_locations = fc.face_locations(rgb_image)
    ans_image = 255 * np.ones_like(original_image)         # full white image
    for top, right, bottom, left in face_locations:
        ans_image[top:bottom, left:right] = original_image[top:bottom, left:right]  # draw face
    return ans_image

def color_face_beard(original_image: Cv2Image) -> Cv2Image:
    face_image = extract_faces(original_image)
    gray_image = cv2.cvtColor(face_image, cv2.COLOR_BGR2GRAY)

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


parser = ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument('--video-url', type=str, help='The url of the video to process')
group.add_argument('--webcam', type=int, default=0, help='Device ID of webcam')
args = parser.parse_args()

if args.video_url is not None:
    name = f'video {args.video_url}'
    cap = cv2.VideoCapture(args.video_url)
else:
    name = f'webcam (device id {args.webcam})'
    cap = cv2.VideoCapture(args.webcam)

if not cap.isOpened():
    print(f'Failed to capture {name}. Exiting.')
    sys.exit(1)

frame_delay = 1    # seconds
while True:
    ret, frame = cap.read()
    transformed_frame = color_face_beard(frame)
    cv2.imshow('frame', transformed_frame)

    # Stop when close button of window is pressed
    if cv2.waitKey(frame_delay) and cv2.getWindowProperty('frame', cv2.WND_PROP_VISIBLE) < 1:
        break

cap.release()
cv2.destroyAllWindows()
