FROM nginx:stable

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/
COPY films_server_nginx.conf /etc/nginx/conf.d/