FROM python:alpine3.15

WORKDIR /usr/src/app
COPY ./requirements.txt ./
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./ ./
RUN flask init-db
RUN rm *.csv
