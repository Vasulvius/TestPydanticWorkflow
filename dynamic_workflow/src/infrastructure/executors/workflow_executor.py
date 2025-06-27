from typing import Any, Dict, List, Optional

from ...domain.entities.workflow_definition import WorkflowDefinition
from ...domain.entities.workflow_node import NodeType
from ...domain.interfaces.i_workflow_executor import IWorkflowExecutor
from ...infrastructure.factories.agent_factory import AgentFactory


class WorkflowExecutor(IWorkflowExecutor):
    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory
        self.execution_history: List[Dict[str, Any]] = []
        self.node_iterations: Dict[str, int] = {}

    async def execute(self, workflow: WorkflowDefinition, initial_data: Any) -> Dict[str, Any]:
        current_node_id = workflow.start_node
        current_data = initial_data
        context = {"workflow_name": workflow.name, "history": []}

        while current_node_id:
            current_node = self._find_node(workflow, current_node_id)
            if not current_node:
                break

            # Vérifier les iterations max
            if self._should_stop_iteration(current_node, current_node_id):
                break

            # Exécuter le nœud
            result = await self._execute_node(current_node, current_data, context)

            # Enregistrer l'historique
            self._record_execution(current_node_id, current_data, result)

            # Déterminer le prochain nœud
            next_node_id = self._determine_next_node(workflow, current_node_id, result)

            current_node_id = next_node_id
            current_data = result

        return {"final_result": current_data, "execution_history": self.execution_history, "node_iterations": self.node_iterations}

    def _find_node(self, workflow: WorkflowDefinition, node_id: str):
        return next((node for node in workflow.nodes if node.id == node_id), None)

    def _should_stop_iteration(self, node, node_id: str) -> bool:
        if node.max_iterations is None:
            return False

        current_iterations = self.node_iterations.get(node_id, 0)
        return current_iterations >= node.max_iterations

    async def _execute_node(self, node, input_data: Any, context: Dict[str, Any]) -> Any:
        # Incrémenter le compteur d'itérations
        self.node_iterations[node.id] = self.node_iterations.get(node.id, 0) + 1

        if node.type == NodeType.END:
            return input_data

        # Créer et exécuter l'agent
        agent = self.agent_factory.create_agent(node.agent_config)
        result = await agent.execute(input_data, context)

        return result

    def _determine_next_node(self, workflow: WorkflowDefinition, current_node_id: str, result: Any) -> Optional[str]:
        edges = [edge for edge in workflow.edges if edge.from_node == current_node_id]

        for edge in edges:
            if self._evaluate_condition(edge.condition, result):
                return edge.to_node

        return None

    def _evaluate_condition(self, condition: Optional[str], result: Any) -> bool:
        if condition is None:
            return True

        # Logique d'évaluation des conditions
        # Peut être étendue pour supporter des conditions complexes
        if hasattr(result, "approved") and condition == "approved":
            return getattr(result, "approved", False)
        elif hasattr(result, "status") and condition in str(getattr(result, "status", "")):
            return True

        return condition == "default"

    def _record_execution(self, node_id: str, input_data: Any, output_data: Any):
        self.execution_history.append(
            {
                "node_id": node_id,
                "iteration": self.node_iterations.get(node_id, 1),
                "input": input_data,
                "output": output_data,
                "timestamp": __import__("datetime").datetime.now().isoformat(),
            }
        )
