# ONLY FOR DEV

FROM ubuntu:16.04


RUN apt-get update -y && \
    apt-get install -y python3-pip 

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY . /app


# Run server
EXPOSE 5000
CMD ["python3", "wdrAPI.py"]

