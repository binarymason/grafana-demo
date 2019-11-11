FROM python:3.7

RUN apt-get update && apt-get install vim -y

RUN pip install pipenv
COPY Pipfile* /tmp/
RUN cd /tmp && pipenv lock --requirements > /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt


WORKDIR /app/src
COPY . /app/src/

ENV PYTHONPATH /app

CMD ["python", "-c", "print('hello from docker')"]

