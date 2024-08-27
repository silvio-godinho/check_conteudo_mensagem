FROM mysql:8.0

ENV MYSQL_DATABASE=empresa_dados \
    MYSQL_USER=my_user \
    MYSQL_PASSWORD=my_password \
    MYSQL_ROOT_PASSWORD=1234

COPY mysql/dados_empresa.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

CMD ["mysqld"]
