FROM python:3.7.4-stretch

###
# Server
###
RUN adduser films
WORKDIR /home/films

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir uwsgi

COPY app app
COPY migrations migrations
COPY wsgi.py flask_moment_project.py config.py filling_db.py uwsgi_setting.ini start.sh ./

RUN chmod +x start.sh
RUN chown -R films:films ./

USER films

ENTRYPOINT ["./start.sh"]



