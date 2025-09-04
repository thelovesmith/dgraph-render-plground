# set up the image to build the Modus app
FROM --platform=$BUILDPLATFORM node:22-alpine AS builder
ENV NPM_CONFIG_UPDATE_NOTIFIER=false NPM_CONFIG_FUND=false
WORKDIR /src

# install the Modus CLI
RUN npm i -g @hypermode/modus-cli

# copy the application source code
COPY . /src/

# build the application
RUN modus build

# build the db migrations tool
FROM --platform=$BUILDPLATFORM golang:1.25 AS migrate-builder
RUN go install github.com/hypermodeinc/modus/tools/modus-dbmigrate@latest

# build the container image
FROM hypermodeinc/modus:v0.17-latest

# copy the migrations tool
COPY --from=migrate-builder /go/bin/modus-dbmigrate /usr/bin/

# copy app from the build phase
COPY --from=builder /src/build /home/modus/app/

# set environment variables
ARG PORT MODUS_ENV
ENV PORT=${PORT:-8686}
ENV MODUS_ENV=${MODUS_ENV:-prod}

# set the default entrypoint
# this will apply db migrations before starting the application
ENTRYPOINT ["/bin/bash", "-c", "modus-dbmigrate && modus_runtime -appPath /home/modus/app -port $PORT -jsonlogs"]
