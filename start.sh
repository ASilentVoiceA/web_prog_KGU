#!/bin/bash

while true; do
    flask db upgrade
    if [[ "$?" == "0" ]]; then
        break
    fi
    echo Wait
    sleep 5
done

python filling_db.py

uwsgi uwsgi_setting.ini
