from typing import Any, Dict

from pydantic_ai import Agent

from ...domain.interfaces.i_agent import IAgent


class PydanticAgent(IAgent):
    def __init__(self, agent_config: Dict[str, Any]):
        self.config = agent_config
        self.agent = Agent(model=agent_config.get("model", "openai:gpt-4"), system_prompt=agent_config.get("system_prompt", ""))
        self.name = agent_config.get("name", "GenericAgent")

    async def execute(self, input_data: Any, context: Dict[str, Any]) -> Any:
        result = await self.agent.run(input_data)
        return result.output

    def get_name(self) -> str:
        return self.name
