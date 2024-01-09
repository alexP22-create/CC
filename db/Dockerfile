FROM mysql:latest

ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=restaurant
ENV MYSQL_USER=Alex
ENV MYSQL_PASSWORD=CloudComp10!

COPY restaurant.sql /docker-entrypoint-initdb.d/

EXPOSE 3306