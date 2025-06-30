from typing import Any, Dict, List, Optional

from pydantic import BaseModel

from .node_type import NodeType


class WorkflowNode(BaseModel):
    id: str
    name: str
    type: NodeType
    max_iterations: Optional[int] = None
    agent_config: Dict[str, Any]
    tools: Optional[List[str]] = None
