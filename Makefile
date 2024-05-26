message="code changes from makefile"

build:
	docker-compose up -d --build

run:
	docker-compose up

build_run: build run

clean:
	docker rm -f $(docker ps -a -q)


push:
	git pull
	git commit -m "${message}"
	git push