ARG BASE_IMAGE=python:3.11-alpine@sha256:25df32b602118dab046b58f0fe920e3301da0727b5b07430c8bcd4b139627fdc

FROM golang:1.20.5@sha256:fd9306e1c664bd49a11d4a4a04e41303430e069e437d137876e9290a555e06fb as builder

RUN apt-get update && \
    apt-get install --no-install-recommends --yes clang && \
    rm -rf /var/lib/apt/lists/*

RUN `#TODO(beckerhe): Replace fork with upstream version once fixes are upstreamed` \
    git clone https://github.com/beckerhe/bigquery-emulator && \
    git -C bigquery-emulator/ checkout -b build_branch fdc1733

RUN make -C bigquery-emulator/ emulator/build

FROM $BASE_IMAGE
WORKDIR /root
COPY --from=builder /go/bigquery-emulator/bigquery-emulator /usr/local/bin/
RUN pip install pip==23.2

RUN adduser -D user && mkdir /work
USER user
WORKDIR /work

COPY devtools/db_import/requirements.txt /home/user/
ENV PATH="/home/user/.local/bin:${PATH}"
RUN pip install --user -r /home/user/requirements.txt && rm /home/user/requirements.txt
