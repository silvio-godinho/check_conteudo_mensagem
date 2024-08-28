FROM mysql:8.0

ENV MYSQL_DATABASE=empresa_dados \
    MYSQL_USER= \
    MYSQL_PASSWORD= \
    MYSQL_ROOT_PASSWORD=

COPY mysql/dados_empresa.sql /docker-entrypoint-initdb.d/

EXPOSE 3306

CMD ["mysqld"]
