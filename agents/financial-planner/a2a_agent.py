from a2a.types import (
    AgentCapabilities,
    AgentCard,
    AgentSkill,
)
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from agent import root_agent

def get_a2a_starlette_app(fqdn: str):
    # A2A Agent Skill definition
    currency_retrieval_skill = AgentSkill(
        id="currency_retrieval",
        name="Currency retrieval tool",
        description="Retrieve the details of a currency",
        tags=["currency", "currency details"],
        examples=["Tell me about the USD"],
    )

    exchange_rate_retrieval_skill = AgentSkill(
        id="exchange_rate_retrieval",
        name="Exchange rate retrieval tool",
        description="Retrieve the exchange rate between two currencies",
        tags=["retrieve exchange rate", "calculate exchange rate"],
        examples=["Convert 100 USD to EUR", "Can you tell me the exchange rate of USD to EUR?"],
    )

    time_series_exchange_rate_retrieval_skill = AgentSkill(
        id="time_series_exchange_rate_retrieval",
        name="Time series exchange rate retrieval tool",
        description="Retrieve the historical exchange rate between two currencies, across multiple time periods",
        tags=["time series exchange rate", "time series exchange rate retrieval"],
        examples=["Tell me about the USD to EUR exchange rate from 2024-01-01 to 2025-01-01", "Retrieve the time series data from 12th December 2020 to 12th December 2021, for USD to EUR"],
    )

    # A2A Agent Card definition
    agent_card = AgentCard(
        name="Financial Planner Agent",
        description="Host a series of financial planning tools",
        url=fqdn,
        version="1.0.0",
        defaultInputModes=["text"],
        defaultOutputModes=["text"],
        capabilities=AgentCapabilities(streaming=True),
        skills=[
            currency_retrieval_skill,
            exchange_rate_retrieval_skill,
            time_series_exchange_rate_retrieval_skill,
        ],
    )

    return to_a2a(root_agent, agent_card=agent_card)
