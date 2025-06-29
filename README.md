
# Principles

- In development, most if not all webservers containing agent(s), or adk-web, or adk web-server, will start numbering from port 8080, for ease of local debuggability
  - From docker-compose, we might expose it on a different port externally. Check `docker-compose.yml` for the latest updated value here

# Run Everything!

Run `docker-compose up` to run everything!

Here's a list of all of the available servers

| **Name**                                                                                                         | **Type**   | **Test URL (localhost)**                          | **Bash command**                      |
|------------------------------------------------------------------------------------------------------------------|------------|---------------------------------------------------|---------------------------------------|
| ADK Web Chat Tester                                                                                              | Dev tool   | [localhost:8080](http://localhost:8080)           | `make bash-adk-web`                   |
| ADK Server API (mocking remote deployment)                                                                       | Dev tool   | [localhost:8081](http://localhost:8081/list-apps) | `make bash-adk-apiserver`             |
| (Under construction) API Docs for agent API endpoints (Swagger)                                                  | Dev tool   | [localhost:8082](http://localhost:8082)           | -                                     |
| A2A master agent delegator (That also supports A2A itself!)                                                      | Agent      | [localhost:8083](http://localhost:8083)           | `make bash-agent-a2a-agent-master`    |
| Hello world greeter (agent that greets people, simple use case)                                                  | Agent      | [localhost:8084](http://localhost:8084)           | `make bash-agent-hello-world-greeter` |
| Google Search powered agent                                                                                      | Agent      | [localhost:8085](http://localhost:8085)           | `make bash-agent-google-search`       |
| Financial planner agent <br/>(Currently only currency functions - Currency conversion, Trend data retrieval etc) | Agent      | [localhost:8086](http://localhost:8086)           | `make bash-agent-financial-planner`   |
| Chart maker agent                                                                                                | Agent      | [localhost:8087](http://localhost:8087)           | `make bash-agent-chart-maker`         |
| MCP Server - Exchange rate API Wrapper                                                                           | MCP Server | [localhost:9000](http://localhost:9000)           | `make bash-mcp-server-exchange-rate`  |
| MCP Server - Quickchart image maker                                                                              | MCP Server | [localhost:9001](http://localhost:9001)           | `make bash-mcp-server-quickchart`     |

Use `ADK Web` to test the above agents (already integrated) easily. Here's how they are plugged together at the moment:

Here's how it looks like together:


# Development utilities

```
make util-create-agent name="YOUR_AGENT_NAME"
```


