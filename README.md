# face_beard_highlight
This project aims to help during beard trimming 
by highlighting beard problem areas that need to be trimmed.

**NOTE:** See how the algorithm works in [this Jupyter Notebook](prototype.ipynb).

## Bugs
- 25th percentile of grayscale frame is steadily increasing in each frame,
so after a point, it increases so much that hear & beard stop being highlighted completely.
Don't know why, since I tested with my face in webcam, sitting stationary, 
with stable (medium) lighting conditions.

- Only beard should be highlighted, but other things like clothes are also being highlighted.
Try to limit to face only (and even better - to beard only).

- Modify threshold to account for lighting conditions. 
If it's very dark, almost everything is highlighted. If it's very bright, almost nothing is highlighted.

For example, in this image (medium lighting), 
some beard areas are highlighted while majority is not highlighted:

![Medium Dark Lighting](test_outputs/medium_lighting.png)

## Useful Tools & Resources
- Pick exact RGB color from any image pixel: https://www.imgcolorpicker.com/