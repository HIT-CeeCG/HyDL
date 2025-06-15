FROM golang:1.17 as builder
WORKDIR /go/src/Kooperator

COPY go.mod go.mod
COPY go.sum go.sum

RUN go mod download

COPY apis/ apis/
COPY cmd/ cmd/
COPY pkg/ pkg/

RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -a -o koord-scheduler cmd/koord-scheduler/main.go

FROM gcr.io/distroless/static:latest
WORKDIR /
COPY --from=builder /go/src/Kooperator/koord-scheduler .
ENTRYPOINT ["/koord-scheduler"]
