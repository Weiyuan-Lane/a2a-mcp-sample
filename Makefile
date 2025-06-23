MAKEFLAGS += --silent

bash-adk-apiserver:
	@docker exec -it adk-apiserver bash

bash-adk-web:
	@docker exec -it adk-web bash

bash-hello-world-agent:
	@docker exec -it hello-world-agent bash -c "source ./local-env/bin/activate"
