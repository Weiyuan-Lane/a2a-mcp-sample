MAKEFLAGS += --silent

# BASH Aliases

bash-adk-web:
	@docker exec -it adk-web bash

bash-adk-apiserver:
	@docker exec -it adk-apiserver bash

bash-hello-world-agent:
	@docker exec -it hello-world-agent bash -c "source ./local-env/bin/activate"

# UTIL utilities

util-create-agent:
ifndef name
	$(error "name" is not set)
else
	@docker exec -it adk-apiserver sh -c "adk create agents/${name}"
endif

