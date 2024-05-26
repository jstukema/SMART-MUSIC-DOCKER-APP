# SMART-MUSIC-DOCKER-APP
 SMART-MUSIC-DOCKER-APP

# Running the code
- docker-compose up -d --build
- docker-compose up

# This is to see the containers that are running
- docker ps

# This command is to log into the DB
- docker exec -it imageName bash

# To log into the server that holds the codes and NOT the db
- alembic revision -m "create_main_tables"
- alembic upgrade head

- docker-compose exec databaseName
- psql -U postgres
- psql -h localhost -U postgres --dbname=postgres
- generate SECRET_KEY: openssl rand -hex 32


