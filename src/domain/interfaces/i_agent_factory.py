from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from ..entities.workflow_node import WorkflowNode
from .i_agent import IAgent


class IAgentFactory(ABC):
    @abstractmethod
    def create_agent(self, agent_config: Dict[str, Any], node: Optional[WorkflowNode] = None) -> IAgent:
        pass
