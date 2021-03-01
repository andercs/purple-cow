FROM python:3.7.10-alpine

WORKDIR /app

# set environment variables
ENV PYTHONUNBUFFERED 1

# install package dependencies
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

# install python dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY .docker/webapp/entrypoint.sh /

# copy the web application
COPY app/ .

EXPOSE 3000

ENTRYPOINT ["/entrypoint.sh"]
