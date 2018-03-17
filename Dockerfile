FROM alpine:latest
LABEL maintainer="yuyang@uunus.com"

ENV PACKAGE ca-certificates openssl tzdata python3 py3-cffi
ENV BUILD_DEP gcc python3-dev musl-dev openssl-dev

COPY src/ /opt/src/

RUN apk add --no-cache --update ${PACKAGE} ${BUILD_DEP}

RUN ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && pip3 install -U pip \
    && pip3 install -r /opt/src/requirements.txt \
    && chmod +x /opt/src/run.py \
    && mkdir -p /opt/src/files \
    && apk del $BUILD_DEP \
    && rm -rf /var/cache/apk/* \
    && rm -rf /root/.cache/pip/*

EXPOSE 5000
WORKDIR /opt/src/

CMD ["./run.py"]