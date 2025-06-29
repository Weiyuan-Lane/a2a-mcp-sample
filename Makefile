MAKEFLAGS += --silent

# BASH Aliases

bash-adk-web:
	@docker exec -it adk-web bash

bash-adk-apiserver:
	@docker exec -it adk-apiserver bash

bash-agent-a2a-agent-master:
	@docker exec -it agent-a2a-agent-master bash -c "source ./local-env/bin/activate && bash"

bash-agent-hello-world-greeter:
	@docker exec -it agent-hello-world-greeter bash -c "source ./local-env/bin/activate && bash"

bash-agent-google-search:
	@docker exec -it agent-google-search bash -c "source ./local-env/bin/activate && bash"

bash-mcp-server-exchange-rate:
	@docker exec -it mcp-server-exchange-rate bash -c "source ./local-env/bin/activate && bash"

# UTIL utilities

util-create-agent:
ifndef name
	$(error "name" is not set)
else
	@docker exec -it adk-apiserver sh -c "adk create agents/${name}"
endif

