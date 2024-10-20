FROM python:3.10-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /var/www

COPY ./requirements.txt .

RUN apk add --no-cache --virtual .build-deps gcc musl-dev \
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.__main__:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]