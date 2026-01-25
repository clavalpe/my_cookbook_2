FROM ghcr.io/astral-sh/uv:0.9.26@sha256:9a23023be68b2ed09750ae636228e903a54a05ea56ed03a934d00fe9fbeded4b AS uv
FROM python:3.14.2-slim-trixie@sha256:9b81fe9acff79e61affb44aaf3b6ff234392e8ca477cb86c9f7fd11732ce9b6a AS base

FROM base AS dev

ENV PYTHONUNBUFFERED=1
ENV PYTHONSAFEPATH=1
ENV PYTHONPATH=/app/src
ENV APPLICATION_NAME=my-cookbook
ENV PROMETHEUS_MULTIPROC_DIR=/var/run

WORKDIR /app/src

COPY --from=uv /uv /uvx /bin/
COPY ./requirements/base.txt /app/requirements/
RUN uv pip install --system --no-cache-dir --disable-pip-version-check \
    -r /app/requirements/base.txt

RUN export DEBIAN_FRONTEND=noninteractive \
    && apt-get update \
    && apt-get install --yes --no-install-recommends \
        wait-for-it \
    && rm -rf /var/lib/apt/lists/*

