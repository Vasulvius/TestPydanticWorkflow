from typing import List

from pydantic import BaseModel

from .workflow_edge import WorkflowEdge
from .workflow_node import WorkflowNode


class WorkflowDefinition(BaseModel):
    name: str
    description: str
    nodes: List[WorkflowNode]
    edges: List[WorkflowEdge]
    start_node: str
