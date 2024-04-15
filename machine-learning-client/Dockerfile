FROM python:3

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=face_detection.py \
    FLASK_RUN_HOST=0.0.0.0 \
    FLASK_RUN_PORT=80

WORKDIR /

ADD . /

COPY requirements.txt ./
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt


EXPOSE 80

CMD [ "python3", "face_detection.py" ]