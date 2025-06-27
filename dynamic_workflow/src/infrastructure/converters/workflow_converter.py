from typing import Any, Dict

from pydantic_graph import Graph

from ...domain.entities.workflow_definition import WorkflowDefinition
from ...domain.entities.workflow_edge import WorkflowEdge
from ...domain.entities.workflow_node import WorkflowNode
from ...domain.interfaces.i_workflow_converter import IWorkflowConverter
from ...infrastructure.factories.agent_factory import AgentFactory


class WorkflowConverter(IWorkflowConverter):
    def __init__(self, agent_factory: AgentFactory):
        self.agent_factory = agent_factory

    def json_to_workflow(self, json_data: Dict[str, Any]) -> WorkflowDefinition:
        nodes = [WorkflowNode(**node) for node in json_data["nodes"]]
        edges = [WorkflowEdge(**edge) for edge in json_data["edges"]]

        return WorkflowDefinition(
            name=json_data["name"], description=json_data["description"], nodes=nodes, edges=edges, start_node=json_data["start_node"]
        )

    def workflow_to_pydantic_graph(self, workflow: WorkflowDefinition) -> Graph:
        graph = Graph()

        # Créer les nœuds avec les agents
        for node in workflow.nodes:
            agent = self.agent_factory.create_agent(node.agent_config)
            graph.add_node(node.id, agent)

        # Ajouter les edges avec conditions
        for edge in workflow.edges:
            graph.add_edge(edge.from_node, edge.to_node, condition=edge.condition)

        return graph
