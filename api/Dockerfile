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

# build the container image
FROM hypermodeinc/modus:v0.17-latest

# # install db migration tool
# USER root
# RUN apt-get update \
#     && apt-get install -y --no-install-recommends gnupg2 lsb-release \
#     && curl -fsSL https://packagecloud.io/golang-migrate/migrate/gpgkey | gpg --dearmor -o /etc/apt/keyrings/migrate.gpg \
#     && echo "deb [signed-by=/etc/apt/keyrings/migrate.gpg] https://packagecloud.io/golang-migrate/migrate/ubuntu/ $(lsb_release -sc) main" > /etc/apt/sources.list.d/migrate.list \
#     && apt-get update \
#     && apt-get install -y --no-install-recommends migrate \
#     && rm -rf /var/lib/apt/lists/*
# USER modus

# copy app from the build phase
COPY --from=builder /src/build /home/modus/app/

# set environment variables
ARG PORT MODUS_ENV
ENV PORT=${PORT:-8686}
ENV MODUS_ENV=${MODUS_ENV:-prod}

# set the default entrypoint
# this will apply db migrations before starting the application
# ENTRYPOINT ["/bin/bash", "-c", "migrate -source github://hypermodeinc/modus/runtime/db/migrations -database $MODUS_DB up && modus_runtime -appPath /home/modus/app -port $PORT -jsonlogs"]

ENTRYPOINT ["/bin/bash", "-c", "modus_runtime -appPath /home/modus/app -port $PORT -jsonlogs"]
