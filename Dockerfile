FROM jhonatans01/python-dlib-opencv
RUN pip install face_recognition
COPY main.py .
CMD python3 main.py