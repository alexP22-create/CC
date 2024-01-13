FROM phpmyadmin/phpmyadmin:latest

# Set environment variables for phpMyAdmin configuration
ENV PMA_ARBITRARY=1 \
    MYSQL_HOST=db-service \
    MYSQL_PORT=3306 \
    MYSQL_USER=Alex \
    MYSQL_PASSWORD=CloudComp10

# Expose the port on which phpMyAdmin will run
EXPOSE 30080

# Start phpMyAdmin
CMD ["apache2-foreground"]

