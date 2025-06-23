MAKEFLAGS += --silent

bash-adk-web:
	@docker exec -it adk-web bash

bash-hello-world-agent:
	@docker exec -it hello-world-agent bash -c "source ./local-env/bin/activate"
