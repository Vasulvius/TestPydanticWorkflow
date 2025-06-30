from typing import Any, Dict, List, Optional

from ...core.condition_evaluator import ConditionEvaluator
from ...domain.entities.workflow_definition import WorkflowDefinition
from ...domain.entities.workflow_node import NodeType
from ...domain.interfaces.i_workflow_executor import IWorkflowExecutor
from ...infrastructure.factories.agent_factory import AgentFactory


class WorkflowExecutor(IWorkflowExecutor):
    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory
        self.execution_history: List[Dict[str, Any]] = []
        self.node_iterations: Dict[str, int] = {}
        self.condition_evaluator = ConditionEvaluator()

    async def execute(self, workflow: WorkflowDefinition, initial_data: Any) -> Dict[str, Any]:
        current_node_id = workflow.start_node
        current_data = initial_data
        context = {"workflow_name": workflow.name, "history": [], "original_request": initial_data}

        max_total_iterations = 20  # Sécurité contre les boucles infinies

        iteration_count = 0
        while current_node_id and iteration_count < max_total_iterations:
            iteration_count += 1
            current_node = self._find_node(workflow, current_node_id)
            if not current_node:
                print(f"❌ Nœud {current_node_id} non trouvé")
                break

            # Vérifier les iterations max pour ce nœud spécifique
            if self._should_stop_iteration(current_node, current_node_id):
                print(f"⏹️ Max iterations atteint: {current_node.name}")
                # Pour le reviewer, on force la final_review
                if current_node_id == "reviewer":
                    context["force_final_review"] = True
                else:
                    break

            node_iteration = self.node_iterations.get(current_node_id, 0) + 1
            print(f"🔄 {current_node.name} - Iteration {node_iteration}")

            # Exécuter le nœud
            result = await self._execute_node(current_node, current_data, context)

            # Enregistrer l'historique
            self._record_execution(current_node_id, current_data, result)

            # Déterminer le prochain nœud
            next_node_id = self._determine_next_node(workflow, current_node_id, result, context)

            if next_node_id:
                next_node = self._find_node(workflow, next_node_id)
                next_node_name = next_node.name if next_node else next_node_id
                print(f"   ➡️ {current_node.name} → {next_node_name}")
            else:
                print("   ✅ Workflow terminé")

            current_node_id = next_node_id
            current_data = result

        return {
            "final_result": current_data,
            "execution_history": self.execution_history,
            "node_iterations": self.node_iterations,
            "total_iterations": iteration_count,
        }

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

        # Préparer les données d'entrée selon le nœud
        if node.id == "manager_final":
            # Le manager final a besoin du contexte complet
            enhanced_input = {
                "content": input_data,
                "original_request": context.get("original_request"),
                "iterations": self.node_iterations,
                "history": self.execution_history,
            }
            input_data = enhanced_input

        # Créer et exécuter l'agent
        agent = self.agent_factory.create_agent(node.agent_config, node)
        result = await agent.execute(input_data, context)

        return result

    def _determine_next_node(
        self, workflow: WorkflowDefinition, current_node_id: str, result: Any, context: Dict[str, Any]
    ) -> Optional[str]:
        edges = [edge for edge in workflow.edges if edge.from_node == current_node_id]

        for edge in edges:
            if self._evaluate_condition(edge.condition, result, context, current_node_id):
                return edge.to_node

        # Si aucune condition n'est satisfaite, prendre le premier edge sans condition
        default_edge = next((edge for edge in edges if edge.condition is None), None)
        if default_edge:
            return default_edge.to_node

        return None

    def _evaluate_condition(self, condition: Optional[str], result: Any, context: Dict[str, Any], current_node_id: str) -> bool:
        return self.condition_evaluator.evaluate(condition, result, context)

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
