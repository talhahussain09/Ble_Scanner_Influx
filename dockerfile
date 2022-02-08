#Deriving the latest base image
FROM python:latest

#Labels as key value pair
LABEL Maintainer="talha.test"


#installing the required dependencies
RUN apt-get update && apt-get install -y \
    bluez \
    dbus

RUN apt-get install -y  python3-pip libglib2.0-dev

RUN pip3 install bluepy

RUN pip3 install paho-mqtt

# Any working direcrtory can be chosen as per choice like '/' or '/home' etc
# i have chosen /usr/app/src

WORKDIR /usr/app/src

#to COPY the remote file at working directory in container
COPY influx_Scanner.py ./

COPY test.sh ./
# Now the structure looks like this '/usr/app/src/test.py'

#CMD instruction should be used to run the software
#contained by your image, along with any arguments.

#test the bash script

CMD ./test.sh

#CMD ["service", "dbus", "start"]

#CMD [ "service", "bluetooth", "start"]
