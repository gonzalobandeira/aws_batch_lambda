NAME=poc-batch-start
ECR_NAME=775255162681.dkr.ecr.eu-central-1.amazonaws.com/poc-batch-start

default: up

build:
	docker build -t $(NAME) .

tag:
	docker tag $(NAME) $(ECR_NAME):latest

push:
	aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 775255162681.dkr.ecr.eu-central-1.amazonaws.com/poc-batch-process
	docker push $(ECR_NAME):latest

up:
	docker build -t $(NAME) .
	docker tag $(NAME) $(ECR_NAME):latest
	docker tag $(NAME) $(ECR_NAME):latest
	aws ecr get-login-password --region eu-central-1 | docker login --username AWS --password-stdin 775255162681.dkr.ecr.eu-central-1.amazonaws.com/poc-batch-process
	docker push $(ECR_NAME):latest

all:
	@echo "Makefile needs your attention"