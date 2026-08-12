FROM golang:1.25.12-alpine3.24

LABEL "com.quatrolabs.watchman-bot"="quatroLABS Watchman"
LABEL "description"="Watchman helps to keep track of automating services; a tiny bot"

ENV GO111MODULE=on

RUN mkdir -p /opt
RUN mkdir -p /opt/watchman

WORKDIR /opt/watchman
COPY . /opt/watchman

RUN rm -rf cmd && mkdir -p cmd
RUN CGO_ENABLED=0 go build -o cmd/ ./...
RUN apk add --no-cache jq

ENV PATH="/opt/watchman/cmd:${PATH}"

ENTRYPOINT [ "cmd/watchman-bot" ]
CMD [ "help" ]
