from typing import Optional

from pydantic import BaseModel


class WorkflowEdge(BaseModel):
    from_node: str
    to_node: str
    condition: Optional[str] = None
