from python:3.11.1-buster

WORKDIR /src

COPY . /src

RUN pip install --no-cache-dir --upgrade pip
RUN pip install runpod
RUN pip install --no-cache-dir -r requirements.txt


CMD [ "python", "-u", "handler.py" ]