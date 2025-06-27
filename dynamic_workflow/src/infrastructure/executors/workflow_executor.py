import json
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
        context = {"workflow_name": workflow.name, "history": [], "original_request": initial_data}

        max_total_iterations = 20  # Sécurité contre les boucles infinies

        iteration_count = 0
        while current_node_id and iteration_count < max_total_iterations:
            iteration_count += 1
            current_node = self._find_node(workflow, current_node_id)
            if not current_node:
                print(f"⚠️ Nœud {current_node_id} non trouvé")
                break

            # Vérifier les iterations max pour ce nœud spécifique
            if self._should_stop_iteration(current_node, current_node_id):
                print(f"⚠️ Nombre max d'itérations atteint pour {current_node_id}")
                # Pour le reviewer, on force la final_review
                if current_node_id == "reviewer":
                    context["force_final_review"] = True
                else:
                    break

            print(f"🔄 Exécution du nœud: {current_node.name} (iteration {self.node_iterations.get(current_node_id, 0) + 1})")

            # Exécuter le nœud
            result = await self._execute_node(current_node, current_data, context)

            # Enregistrer l'historique
            self._record_execution(current_node_id, current_data, result)

            # Déterminer le prochain nœud
            next_node_id = self._determine_next_node(workflow, current_node_id, result, context)

            print(f"➡️ Transition: {current_node_id} -> {next_node_id}")
            print(f"📝 Résultat: {result}")

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
        agent = self.agent_factory.create_agent(node.agent_config)
        result = await agent.execute(input_data, context)

        return result

    def _determine_next_node(
        self, workflow: WorkflowDefinition, current_node_id: str, result: Any, context: Dict[str, Any]
    ) -> Optional[str]:
        edges = [edge for edge in workflow.edges if edge.from_node == current_node_id]

        print(f"🔍 Évaluation des transitions depuis {current_node_id}")
        print(f"📊 Résultat à évaluer: {result}")

        for edge in edges:
            print(f"   Condition '{edge.condition}' -> {edge.to_node}")
            if self._evaluate_condition(edge.condition, result, context, current_node_id):
                print("   ✅ Condition satisfaite!")
                return edge.to_node
            else:
                print("   ❌ Condition non satisfaite")

        # Si aucune condition n'est satisfaite, prendre le premier edge sans condition
        default_edge = next((edge for edge in edges if edge.condition is None), None)
        if default_edge:
            print(f"   🔄 Utilisation de la transition par défaut -> {default_edge.to_node}")
            return default_edge.to_node

        print("   ⚠️ Aucune transition trouvée")
        return None

    def _evaluate_condition(self, condition: Optional[str], result: Any, context: Dict[str, Any], current_node_id: str) -> bool:
        if condition is None:
            return True

        # Convertir le résultat en dict si c'est une string JSON
        if isinstance(result, str):
            try:
                result_dict = json.loads(result.replace("'", '"'))
                result = result_dict
            except Exception as e:
                print(f"      [WorkflowExecutor] ❗ Erreur de conversion du résultat en dict: {e}")
                pass

        print(f"      🧮 Évaluation: condition='{condition}', result_type={type(result)}")

        # Conditions spéciales pour le reviewer
        if current_node_id == "reviewer" and isinstance(result, dict):
            approved = result.get("approved", False)
            final_review = result.get("final_review", False) or context.get("force_final_review", False)
            current_iteration = self.node_iterations.get("reviewer", 0)

            if condition == "rejected_not_final":
                return not approved and not final_review and current_iteration < 3
            elif condition == "approved":
                return approved
            elif condition == "final_review":
                return final_review or current_iteration >= 3

        # Conditions classiques
        if isinstance(result, dict):
            if condition == "approved" and "approved" in result:
                return result["approved"] is True
            elif condition == "rejected" and "approved" in result:
                return result["approved"] is False
            elif condition == "complete" and "status" in result:
                return result["status"] == "complete"
            elif condition == "incomplete" and "status" in result:
                return result["status"] == "incomplete"
            elif condition == "has_bugs" and "has_bugs" in result:
                return result["has_bugs"] is True
            elif condition == "no_bugs" and "has_bugs" in result:
                return result["has_bugs"] is False

        print(f"      ❓ Condition '{condition}' non reconnue pour le résultat {result}")
        return False

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
