
# You can copy this Dockerfile.example to Dockerfile to add configuration
# or packages or anything else to your webimage
ARG BASE_IMAGE=drud/ddev-webserver
FROM $BASE_IMAGE

RUN apt-get install -y nodejs npm

# https://gist.github.com/LoganGray/8aa2de1a079222d9e2ba39ecd207684e
RUN apt-get update
RUN apt-get install libasound2 libnspr4 libnss3 libxss1 xdg-utils libgbm1 python3-pip -y
RUN sudo apt-get install -y libappindicator1 fonts-liberation libappindicator3-1 libatk-bridge2.0-0 libatspi2.0-0 libgtk-3-0
RUN apt-get -f install
RUN wget http://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN sudo dpkg -i google-chrome*.deb
RUN wget http://chromedriver.storage.googleapis.com/2.45/chromedriver_linux64.zip
RUN unzip chromedriver_linux64.zip
RUN sudo mv chromedriver /usr/bin/chromedriver
RUN sudo chown root:root /usr/bin/chromedriver
RUN sudo chmod +x /usr/bin/chromedriver
# install lighthouse
RUN npm i -g lighthouse
RUN pip3 install tabulate