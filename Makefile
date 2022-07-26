# env:
# 	conda deactivate && source venv/bin/activate
clock: 
	sudo hwclock -s
run: 
	uvicorn main:app --reload
create_docker_container:
	docker build -t live-trading-system:1 .
docker_run:
	docker run -p 8000:8000 --name live-instance live-trading-system:1
create_requirements:
	python -m pip freeze | grep -v "@ file" > requirements.txt / list --format=freeze > requirements.txt


############ BASIC Docker commands:
# docker ps: to see containers
# docker run -d redis: gets id as output and run container in detached mode
# docker stop {id}: stops the container
# docker start {id}: starts the container
# docker ps -a: gives all containers running, and not running.
# docker run -p6000:6379 redis: {host:container} specify port bindings
# docker images: see all images remove ones not being used.
# docker logs {id}: see logs of docker id. can also instead use name.
# docker exec -it {id} /bin/bash: root terminal access of container.
# docker run takes a images and creats container, docker starts takes a container that was of and turns on.
# docker network ls: see networks
# can also create a docker network...
##################################
# image is an artifact when run it is a container
# docker vs VMS's: docker smaller, faster. is application layer vm is application and os kernel.
# docker compose takes care of sharing a network