FROM animcogn/face_recognition
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install opencv-python
COPY main.py .
CMD python3 main.py