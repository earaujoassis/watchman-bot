FROM golang:1.19.12-alpine3.18

LABEL "com.quatrolabs.watchman"="quatroLABS Watchman"
LABEL "description"="Watchman helps to keep track of automating services; a tiny bot"

ENV GO111MODULE=on

RUN mkdir -p /opt
RUN mkdir -p /opt/watchman

WORKDIR /opt/watchman

COPY . /opt/watchman

RUN rm -rf cmd && mkdir -p cmd
RUN CGO_ENABLED=0 go build -o cmd/ ./...

ENTRYPOINT [ "cmd/watchman-bot" ]
CMD [ "help" ]
