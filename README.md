# SMART-MUSIC-DOCKER-APP
 SMART-MUSIC-DOCKER-APP

# Running the code
- docker-compose up -d --build
- docker-compose up
- docker ps #this is to see the containers that are running
- docker exec -it imageName bash
- docker-compose exec databaseName 
- psql -h localhost -U postgres --dbname=postgres
- generate SECRET_KEY: openssl rand -hex 32
- alembic revision -m "create_main_tables"
- alembic upgrade head
