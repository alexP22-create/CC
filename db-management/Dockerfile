FROM phpmyadmin/phpmyadmin:latest

ENV PMA_ARBITRARY=1 \
    MYSQL_HOST=db-service \
    MYSQL_PORT=3306 \
    MYSQL_USER=Alex \
    MYSQL_PASSWORD=CloudComp10

EXPOSE 30080

CMD ["apache2-foreground"]

