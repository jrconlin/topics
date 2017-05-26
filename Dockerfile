FROM frolvlad/alpine-python2

EXPOSE 8200

RUN apk update && apk upgrade 
RUN apk add python make gcc libffi-dev linux-headers musl-dev git python-dev py-pip build-base openssl-dev

COPY . /app
WORKDIR /app

RUN pip install virtualenv && \
    virtualenv .

RUN source bin/activate && \
    cat requirements.txt | xargs pip install && \
    python setup.py develop 

RUN rm -rf /var/cache/apk/* && apk del py-pip

CMD bin/topic_server 
