FROM python:3.9-slim
LABEL authors="andrey.zavodov"

ADD . /app/
WORKDIR /app

ENV STATIC_ROOT=/app/data/static
ENV MEDIA_ROOT=/app/data/media
ENV DJANGO_SETTINGS_MODULE=picloud.settings
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip &&\
    pip install -r requirements.txt --no-cache-dir

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
