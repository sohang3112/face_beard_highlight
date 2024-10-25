FROM jupyter/scipy-notebook
USER root
RUN chown jovyan /home/jovyan
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install opencv-python face_recognition
COPY main.py .
ENTRYPOINT ["python3", "main.py"]