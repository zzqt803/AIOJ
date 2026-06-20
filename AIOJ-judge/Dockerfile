FROM ubuntu:22.04 AS build

RUN apt-get update && apt-get install -y \
    g++ cmake make \
    libhiredis-dev nlohmann-json3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build
COPY CMakeLists.txt .
COPY src/ src/
COPY include/ include/

RUN mkdir -p build && cd build \
    && cmake .. \
    && make -j$(nproc)

# Runtime
FROM ubuntu:22.04

RUN apt-get update && apt-get install -y \
    libhiredis0.14 \
    libconfig-dev \
    gcc g++ make \
    && rm -rf /var/lib/apt/lists/*

# Install isolate
RUN apt-get update && apt-get install -y \
    libcap-dev libseccomp-dev libsystemd-dev \
    pkg-config git \
    && rm -rf /var/lib/apt/lists/*

RUN git clone https://github.com/ioi/isolate.git /tmp/isolate \
    && cd /tmp/isolate \
    && make isolate \
    && cp isolate /usr/local/bin/isolate \
    && mkdir -p /var/local/lib/isolate \
    && rm -rf /tmp/isolate

# Setup isolate user and permissions
RUN useradd -r -s /bin/false isolate || true \
    && echo "isolate:0:65536" >> /etc/subuid \
    && echo "isolate:0:65536" >> /etc/subgid \
    && chmod u+s /usr/local/bin/isolate \
    && mkdir -p /usr/local/etc/isolate \
    && /usr/local/bin/isolate --init

RUN mkdir -p /opt/aioj/test_cases

COPY --from=build /build/build/aioj-judge /usr/local/bin/aioj-judge
COPY judge.conf /opt/aioj/judge.conf

WORKDIR /opt/aioj

CMD ["aioj-judge", "judge.conf"]
