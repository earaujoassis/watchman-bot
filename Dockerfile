FROM golang:1.16.5-alpine3.13

LABEL "com.quatrolabs.watchman"="quatroLABS Watchman"
LABEL "description"="Watchman helps to keep track of automating services; a tiny bot"

ENV GO111MODULE=on

RUN mkdir -p /opt
RUN mkdir -p /opt/watchman

WORKDIR /opt/watchman

COPY . /opt/watchman

RUN go build -o watchman-bot main.go

ENTRYPOINT [ "./watchman-bot" ]
CMD [ "help" ]
