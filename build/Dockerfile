FROM ubuntu:20.04 as slackbot_bs
MAINTAINER Walter A. Boring IV <waboring@hemna.com>

ENV VERSION=1.0.0
ENV HOME=/home/slackbot
ENV BRANCH="master"

ENV INSTALL=$HOME/install
RUN apt-get -y update
RUN apt-get install -y wget gnupg
RUN wget -qO- https://repos.influxdata.com/influxdb.key | apt-key add -
RUN echo "deb https://repos.influxdata.com/debian stretch stable" | tee /etc/apt/sources.list.d/influxdb.list
RUN apt-get -y update
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y apt-utils pkg-config sudo git
RUN apt-get install -y telegraf python3 python3-pip

# Add the telegraf.conf
ADD conf/telegraf.conf /etc/telegraf

# Setup Timezone
ENV TZ=US/Eastern
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN apt-get install -y tzdata
RUN dpkg-reconfigure --frontend noninteractive tzdata

RUN addgroup --gid 1000 slackbot
RUN useradd -m -u 1000 -g 1000 -p slackbot slackbot
# Create directory to hold some of the install files.

#RUN cd $INSTALL && wget https://bootstrap.pypa.io/get-pip.py && python3 get-pip.py
RUN pip3 install -U pip setuptools wheel
USER slackbot
RUN pip3 install --user git+https://github.com/hemna/slackbot_bs.git

# add all confs and extras to the install
# based on CONF env, copy the dirs to the install using CMD cp

# override this to run another configuration
WORKDIR $HOME
ENV CONF default
ADD conf $HOME/
ADD bin/run.sh $HOME/
#RUN chmod 755 $HOME/run.sh

EXPOSE 6000
VOLUME [ "/home/slackbot/conf/slackbot.yaml" ]


CMD $HOME/run.sh

