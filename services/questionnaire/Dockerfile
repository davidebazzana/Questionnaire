FROM python:slim-buster

WORKDIR /usr/src/app
RUN addgroup --system app && adduser --system --group app
ENV APP_HOME=/usr/src/app
COPY ./requirements.txt ./
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt
COPY ./ ./
RUN chown -R app:app $APP_HOME
USER app
RUN flask init-db
RUN rm *.csv