MAKEFLAGS += --silent

bash-hello-world-agent:
	@docker exec -it hello-world-agent bash -c "source ./local-env/bin/activate"
