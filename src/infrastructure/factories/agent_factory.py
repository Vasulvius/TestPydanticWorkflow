from typing import Any, Dict

from ...domain.interfaces.i_agent import IAgent
from ...domain.interfaces.i_agent_factory import IAgentFactory
from ..agents.pydantic_agent import PydanticAgent


class AgentFactory(IAgentFactory):
    def create_agent(self, agent_config: Dict[str, Any]) -> IAgent:
        agent_type = agent_config.get("type", "pydantic")

        if agent_type == "pydantic":
            return PydanticAgent(agent_config)
        else:
            raise ValueError(f"Agent type {agent_type} not supported")
