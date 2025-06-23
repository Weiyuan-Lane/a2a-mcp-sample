
# Principles

- In development, most if not all webservers containing agent(s), or adk-web, or adk web-server, will run on port 8080, for ease of local debuggability
  - From docker-compose, we might expose it on a different port externally. Check `docker-compose.yml` for the latest updated value here

# Concepts

Concept 1
- Using ADK and integrating with ADK web for development purpose


# Maintenance instructions

## Update requirements.txt
```
python3 -m  pipreqs.pipreqs . --force
```
OR
```
pip freeze >requirements.txt
```
