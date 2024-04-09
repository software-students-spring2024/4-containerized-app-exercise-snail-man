IMAGE_NAME = your_image_name

.PHONY: dev

dev:
    docker build -t $(IMAGE_NAME) .
    docker run -p 5000:5000 --env-file .env $(IMAGE_NAME)

