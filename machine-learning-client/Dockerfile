FROM python:3

WORKDIR /

ADD . /

COPY requirements.txt ./
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt


EXPOSE 80

CMD [ "python3", "face_detection.py" ]