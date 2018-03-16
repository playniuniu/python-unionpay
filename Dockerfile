FROM alpine:latest
LABEL maintainer="yuyang@uunus.com"

ENV BUILD_DEP gcc python3-dev musl-dev

COPY src/ /opt/src/

RUN apk add --no-cache --update python3 $BUILD_DEP \
    && pip3 install -U pip \
    && pip3 install -r /opt/src/requirments.txt \
    && chmod +x /opt/src/run.py \
    && apk del $BUILD_DEP \
    && rm -rf /var/cache/apk/* \
    && rm -rf /root/.cache/pip/*

EXPOSE 5000
WORKDIR /opt/src/

CMD ["./run.py"]