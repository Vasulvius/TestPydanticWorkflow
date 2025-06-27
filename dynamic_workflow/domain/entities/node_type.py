from enum import Enum


class NodeType(str, Enum):
    START = "start"
    PROCESS = "process"
    DECISION = "decision"
    END = "end"
