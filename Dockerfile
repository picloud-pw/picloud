FROM python:3.9-slim
LABEL authors="andrey.zavodov"

ADD . /app/
WORKDIR /app

ENV APPLICATION_SECRETS=/app/picloud/secrets.json
ENV DJANGO_SETTINGS_MODULE=picloud.settings

RUN apt-get -y update &&\
    apt-get -y install git-core procps curl g++ tk &&\
    apt-get clean

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt --no-cache-dir

RUN groupadd -g 2000 user-group && useradd -m -u 2001 -g user-group picloud

RUN chown -R picloud .
USER 2001

ENTRYPOINT ["./start.sh"]
CMD [ \
    "gunicorn", \
    "--workers", "4", \
    "--threads", "4", \
    "--preload", \
    "--bind", ":8000", \
    "--access-logfile", "-", \
    "--enable-stdio-inheritance", \
    "picloud.wsgi" \
]
