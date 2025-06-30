from typing import Any, Dict

from ...domain.entities.workflow_node import WorkflowNode
from ...domain.interfaces.i_agent import IAgent
from ...domain.interfaces.i_agent_factory import IAgentFactory
from ..agents.pydantic_agent import PydanticAgent
from ..tools import tool_registry


class AgentFactory(IAgentFactory):
    def create_agent(self, agent_config: Dict[str, Any], node: WorkflowNode = None) -> IAgent:
        agent_type = agent_config.get("type", "pydantic")

        if agent_type == "pydantic":
            # Récupérer les outils si spécifiés dans le nœud
            tools = None
            if node and node.tools:
                tools = tool_registry.get_tools(node.tools)

            return PydanticAgent(agent_config, tools=tools)
        else:
            raise ValueError(f"Agent type {agent_type} not supported")
