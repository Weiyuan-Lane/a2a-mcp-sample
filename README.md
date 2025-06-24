
# Principles

- In development, most if not all webservers containing agent(s), or adk-web, or adk web-server, will start numbering from port 8080, for ease of local debuggability
  - From docker-compose, we might expose it on a different port externally. Check `docker-compose.yml` for the latest updated value here

# Concepts

### Concept 1 - ADK is crazy awesome

By using ADK, you can
- Run `adk web` to host a local web server to test your agents directly
- Run `adk run` to test your agents directly, but with your terminal this time
- Run `adk api_server` to have local api server that emulates how it looks like when you deploy to cloud run and more
- Run `adk create` to create an agent template
- Using ADK and integrating with ADK web for development purpose

### Concept 2 - A2A

- `execute` and `cancel`

# Run Everything!

Run `docker-compose up` to run everything!

Here's a list of all of the running servers

| **Name**                                   | **Type** | **Test URL (localhost)**                          | **Bash command**          |
|--------------------------------------------|----------|---------------------------------------------------|---------------------------|
| ADK Web Chat Tester                        | Dev tool | [localhost:8080](http://localhost:8080)           | `make bash-adk-web`       |
| ADK Server API (mocking remote deployment) | Dev tool | [localhost:8081](http://localhost:8081/list-apps) | `make bash-adk-apiserver` |
|                                            | Agent    | [localhost:8082](http://localhost:8082)           |                           |

# Development utilities

```
make util-create-agent name="YOUR_AGENT_NAME"
```

# Planned scenarios (To change to table later)

Simple
- ADK - tool and schema use case
- ADK Agent - ADK tool
- ADK Agent - Custom tool
- ADK Agent - MCP tool
- ADK Agent - ADK Agent (sub agent)
- A2A Server Agent (Hello World!)
- A2A Client Agent - A2A Server Agent (All tools above!)


## Update requirements.txt
```
python3 -m  pipreqs.pipreqs . --force
```
OR
```
pip freeze >requirements.txt
```
