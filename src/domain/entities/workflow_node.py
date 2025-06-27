from typing import Any, Dict, Optional

from pydantic import BaseModel

from .node_type import NodeType


class WorkflowNode(BaseModel):
    id: str
    name: str
    type: NodeType
    max_iterations: Optional[int] = None
    agent_config: Dict[str, Any]
