MAKEFILE_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))

DOCKER_REPO := mikeydunn/stalker

.PHONY: build
build:
	docker build \
		-t $(DOCKER_REPO):local .

.PHONY: run
run:
	docker run --rm -it \
		-v $(MAKEFILE_DIR)/config.yml:/app/config.yml \
		$(DOCKER_REPO):local \
		stalker

.PHONY: shell
shell:
	docker run --rm -it \
		$(DOCKER_REPO):local \
		ash

.PHONY: test
test:
		docker run --rm -it \
		$(DOCKER_REPO):local \
		pytest
