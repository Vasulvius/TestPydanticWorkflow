from typing import Any, Dict

from ...infrastructure.converters.workflow_converter import WorkflowConverter
from ...infrastructure.executors.workflow_executor import WorkflowExecutor
from ...infrastructure.factories.agent_factory import AgentFactory


class WorkflowService:
    def __init__(self):
        self.agent_factory = AgentFactory()
        self.converter = WorkflowConverter(self.agent_factory)
        self.executor = WorkflowExecutor(self.agent_factory)

    async def execute_workflow_from_json(self, json_definition: Dict[str, Any], initial_data: Any) -> Dict[str, Any]:
        # Convertir JSON en WorkflowDefinition
        workflow = self.converter.json_to_workflow(json_definition)

        # Exécuter le workflow
        result = await self.executor.execute(workflow, initial_data)

        return result

    def create_pydantic_graph_from_json(self, json_definition: Dict[str, Any]):
        workflow = self.converter.json_to_workflow(json_definition)
        return self.converter.workflow_to_pydantic_graph(workflow)
