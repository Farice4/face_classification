FROM tensorflow/tensorflow:1.3.0

RUN apt-get -y update && apt-get install -y git python3-pip python3-dev python3-tk vim procps curl wget

#Face classificarion dependencies & web application
RUN pip3 install scipy==0.19.1 keras==2.0.8 tensorflow==1.3.0 pandas==0.19.1 numpy==1.12.1 h5py==2.7.0 statistics opencv-python==3.2.0.8 Flask==0.12.2 matplotlib==2.0.2 Pillow==4.2.1

ADD . /root/face_classification

WORKDIR /root/face_classification

ENV PYTHONPATH=$PYTHONPATH:src
ENV FACE_CLASSIFIER_PORT=8084
EXPOSE $FACE_CLASSIFIER_PORT
#
ENTRYPOINT ["python3"]
CMD ["src/web/faces.py"]
