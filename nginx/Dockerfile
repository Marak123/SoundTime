FROM nginx:alpine

USER root

COPY ./nginx-setup.conf /etc/nginx/conf.d/default.conf
# COPY ./run.sh /run.sh

RUN chown nginx:nginx /etc/nginx/conf.d/default.conf
    # chmod +x /run.sh

# USER nginx

CMD ["nginx", "-g", "daemon off;"]
# CMD ["/run.sh"]