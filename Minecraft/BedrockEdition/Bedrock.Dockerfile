FROM ubuntu:24.04

EXPOSE 19132 19133

RUN apt-get update && \
    apt-get install -y \
    wget \
    build-essential libbz2-dev libdb-dev \
    libreadline-dev libffi-dev libgdbm-dev liblzma-dev \
    libncursesw5-dev libsqlite3-dev libssl-dev \
    zlib1g-dev uuid-dev tk-dev \
    libcurl4

# =====================================
# Setup python
# =====================================
RUN wget https://www.python.org/ftp/python/3.12.9/Python-3.12.9.tar.xz && tar xvf Python-3.12.9.tar.xz
WORKDIR /Python-3.12.9
RUN ./configure --enable-optimizations && make && make install

WORKDIR /app
COPY ./src/requirements.txt .
COPY ./src/downloader.py .

# =====================================
# Setup server
# =====================================
ENV LD_LIBRARY_PATH="."
COPY ./scripts .

CMD ["bash", "/app/entrypoint.bash"]
