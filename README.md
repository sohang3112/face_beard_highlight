# face_beard_highlight
This project aims to help during beard trimming 
by highlighting beard problem areas that need to be trimmed.

**NOTE:** See how the algorithm works in [this Jupyter Notebook](prototype.ipynb).

## Install & Run

### Installation
Ensure Python 3 is installed, and then run these commands:
```console
$ git clone https://github.com/sohang3112/face_beard_highlight.git
$ cd face_beard_highlight
$ pip install -r requirements.txt   # NOTE: this can take 10-15 mins because of dependency face_recognition
```

### Running
Now start the program with command `python main.py`.

## Bugs
- 25th percentile of grayscale frame is steadily increasing in each frame,
so after a point, it increases so much that hear & beard stop being highlighted completely.
Don't know why, since I tested with my face in webcam, sitting stationary, 
with stable (medium) lighting conditions.

- Only beard should be highlighted, but other facial features (eg. hair, spectacles) are also highlighted.

- Modify threshold to account for lighting conditions. 
If it's very dark, almost everything is highlighted. If it's very bright, almost nothing is highlighted.

For example, in this image (medium lighting), 
some beard areas are highlighted while majority is not highlighted:

![Medium Dark Lighting](test_outputs/medium_lighting.png)

## Useful Tools & Resources
- Pick exact RGB color from any image pixel: https://www.imgcolorpicker.com/