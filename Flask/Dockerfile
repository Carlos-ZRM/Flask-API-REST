FROM python:3.6
RUN apt-get update -y
RUN apt-get install vim  net-tools telnet nmap traceroute -y
WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ./API-REST.py .

CMD [ "python", "./API-REST.py" ]
