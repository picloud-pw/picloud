#!/bin/bash

ARCHIVE_DIR="/app/data/"
TS=$(date '+%Y-%m-%dT%H-%M-%S')
FILENAME="$TS-$DUMP_SCRIPT_FILENAME.tar"
FILEDIR="/app/archive"
FILEPATH="$FILEDIR/$FILENAME"

# Простая функция для парсинга свойств из JSON
function parse_json()
{
    local output
    regex="(\"$1\":[\"]?)([^\",\}]+)([\"]?)"
    [[ $2 =~ $regex ]] && output=${BASH_REMATCH[2]}
    echo $output
}

# Функция для отправки файла
function save_to_yandex_drive
{
    echo "Start sending a file: $1"

    # Получаем URL для загрузки файла
    sendUrlResponse=`curl -s -H "Authorization: OAuth $DUMP_SCRIPT_YANDEX_DRIVE_TOKEN" https://cloud-api.yandex.net:443/v1/disk/resources/upload/?path=app:/$FILENAME&overwrite=true`
    sendUrl=$(parse_json 'href' $sendUrlResponse)

    # Отправляем файл
    sendFileResponse=`curl -s -T $FILEPATH -H "Authorization: OAuth $DUMP_SCRIPT_YANDEX_DRIVE_TOKEN" $sendUrl`

    echo "Completing a file upload: $1"
}

mkdir -p $FILEDIR
tar -cf $FILEPATH $ARCHIVE_DIR
save_to_yandex_drive $FILEPATH
rm $FILEPATH
