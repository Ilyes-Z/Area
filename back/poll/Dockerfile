FROM golang:1.15.6
RUN mkdir /app
COPY . /app/
WORKDIR /app
RUN go build -o poll main.go
CMD ["/app/poll"]
