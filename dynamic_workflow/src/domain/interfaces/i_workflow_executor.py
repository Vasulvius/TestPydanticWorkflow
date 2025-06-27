from abc import ABC, abstractmethod
from typing import Any, Dict

from ..entities.workflow_definition import WorkflowDefinition


class IWorkflowExecutor(ABC):
    @abstractmethod
    async def execute(self, workflow: WorkflowDefinition, initial_data: Any) -> Dict[str, Any]:
        pass
