FROM python:3.11.8-slim-bookworm
RUN useradd --create-home --shell /bin/bash app_user
WORKDIR /home/app_user
# RUN --mount=type=bind,source=requirements,target=requirements

COPY ./requirements requirements

RUN pip install --no-cache-dir uv && \
    uv pip compile requirements/in/production.in -o ./requirements/linux-py3.11-production.txt
