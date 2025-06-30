from abc import ABC, abstractmethod
from typing import Any, Dict, List


class IAgent(ABC):
    @abstractmethod
    async def execute(self, input_data: Any, context: Dict[str, Any]) -> Any:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass

    def set_tools(self, tools: List[Any]) -> None:
        """Définit les outils disponibles pour cet agent"""
        pass
