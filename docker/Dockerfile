FROM python:3

WORKDIR /usr/src/app

RUN git clone https://github.com/hemna/slackbot_bs.git

WORKDIR /usr/src/app/slackbot_bs
RUN pip install --no-cache-dir .

CMD [ "slackbot_bs", "bot", "-c", "/tmp/slackbot_bs.conf", "--loglevel", "DEBUG" ]
