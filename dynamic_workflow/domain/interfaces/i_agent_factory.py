from abc import ABC, abstractmethod
from typing import Any, Dict

from .i_agent import IAgent


class IAgentFactory(ABC):
    @abstractmethod
    def create_agent(self, agent_config: Dict[str, Any]) -> IAgent:
        pass
