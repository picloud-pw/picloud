FROM python:3.9-slim
LABEL authors="andrey.zavodov"

ADD . /app/
WORKDIR /app

ENV APPLICATION_SECRETS=/app/data/secrets/secrets.json
ENV STATIC_ROOT=/app/data/static
ENV MEDIA_ROOT=/app/data/media
ENV DJANGO_SETTINGS_MODULE=picloud.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

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
