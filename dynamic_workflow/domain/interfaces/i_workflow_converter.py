from abc import ABC, abstractmethod
from typing import Any, Dict

from ..entities.workflow_definition import WorkflowDefinition


class IWorkflowConverter(ABC):
    @abstractmethod
    def json_to_workflow(self, json_data: Dict[str, Any]) -> WorkflowDefinition:
        pass

    @abstractmethod
    def workflow_to_pydantic_graph(self, workflow: WorkflowDefinition) -> Any:
        pass
