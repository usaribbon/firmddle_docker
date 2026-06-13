FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ARG BINWALK_VERSION=v2.1.1
ARG SASQUATCH_COMMIT=bd864a1b037bf57ca7d64a292a60ba0d6459611f

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        binutils \
        binutils-multiarch \
        build-essential \
        ca-certificates \
        file \
        git \
        liblzo2-dev \
        liblzma-dev \
        patch \
        p7zip-full \
        python3 \
        python3-pip \
        python3-setuptools \
        squashfs-tools \
        unzip \
        wget \
        xz-utils \
        zlib1g-dev \
    && rm -rf /var/lib/apt/lists/*

RUN python3 -m pip install --no-cache-dir "git+https://github.com/ReFirmLabs/binwalk.git@${BINWALK_VERSION}"

RUN git init /tmp/sasquatch \
    && git -C /tmp/sasquatch fetch --depth 1 https://github.com/devttys0/sasquatch.git "${SASQUATCH_COMMIT}" \
    && git -C /tmp/sasquatch checkout FETCH_HEAD \
    && sed -i "s/-Werror//g" /tmp/sasquatch/patches/patch0.txt \
    && wget -q -O /tmp/sasquatch/squashfs4.3.tar.gz https://downloads.sourceforge.net/project/squashfs/squashfs/squashfs4.3/squashfs4.3.tar.gz \
    && tar -xzf /tmp/sasquatch/squashfs4.3.tar.gz -C /tmp/sasquatch \
    && patch -d /tmp/sasquatch/squashfs4.3 -p0 < /tmp/sasquatch/patches/patch0.txt \
    && make -C /tmp/sasquatch/squashfs4.3/squashfs-tools EXTRA_CFLAGS="-fcommon" sasquatch \
    && install -m 0755 /tmp/sasquatch/squashfs4.3/squashfs-tools/sasquatch /usr/local/bin/sasquatch \
    && rm -rf /tmp/sasquatch

WORKDIR /opt/firmddle
COPY . /opt/firmddle

RUN python3 -m pip install --no-cache-dir .

WORKDIR /workspace
ENTRYPOINT ["firmddle"]
CMD ["doctor"]
