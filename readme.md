```angular2html
docker run --name postgres-sql \
-e POSTGRES_USER=tawhid \
-e POSTGRES_PASSWORD=password \
-e POSTGRES_DB=mypython \
-p 5432:5432 \
-d \
postgres
```

````
docker exec -it postgres-sql psql -U tawhid -d mypython
````

```angular2html
SELECT current_user;
```

```angular2html
\list
```

```angular2html
GRANT ALL PRIVILEGES ON DATABASE mypython TO tawhid;
```