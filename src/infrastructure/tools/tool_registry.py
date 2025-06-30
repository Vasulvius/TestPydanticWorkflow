from typing import Dict, List

from pydantic_ai.tools import Tool

from .base_tools import register_base_tools
from .business_tools import register_business_tools
from .custom.content_tools import register_content_tools


class ToolRegistry:
    """Registre centralisé des outils disponibles"""

    def __init__(self):
        self._tools: Dict[str, Tool] = {}
        self._register_all_tools()

    def _register_all_tools(self):
        """Enregistre tous les outils disponibles"""
        # Outils de base (système)
        register_base_tools(self)

        # Outils métier
        register_business_tools(self)

        # Outils personnalisés par domaine
        register_content_tools(self)

    def register_tool(self, name: str, description: str = ""):
        """Décorateur pour enregistrer un outil"""

        def decorator(func):
            tool = Tool(func, description=description)
            self._tools[name] = tool
            return func

        return decorator

    def get_tools(self, tool_names: List[str]) -> List[Tool]:
        """Récupère les outils par nom"""
        tools = []
        for name in tool_names:
            if name in self._tools:
                tools.append(self._tools[name])
            else:
                print(f"⚠️  Outil '{name}' non trouvé dans le registre")
        return tools

    def list_available_tools(self) -> Dict[str, str]:
        """Liste tous les outils avec leurs descriptions"""
        return {name: getattr(tool.function, "__doc__", "Pas de description") for name, tool in self._tools.items()}
