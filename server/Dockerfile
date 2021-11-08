# syntax=docker/dockerfile:1

FROM navikey/raspbian-buster

ENV FLASK_APP=flaskr
ENV FLASK_ENV=development
WORKDIR /server
RUN sudo apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-pip
RUN python3 -m venv venv
RUN . venv/bin/activate

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .


ENTRYPOINT [ "bash", "commands.sh" ]
