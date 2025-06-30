import json
import re
from typing import Any, Dict, List, Optional

from pydantic_ai import Agent
from pydantic_ai.tools import Tool

from ...domain.interfaces.i_agent import IAgent


class PydanticAgent(IAgent):
    def __init__(self, agent_config: Dict[str, Any], tools: Optional[List[Tool]] = None):
        self.config = agent_config
        self.name = agent_config.get("name", "GenericAgent")
        self.tools = tools or []
        self._create_agent()

    async def execute(self, input_data: Any, context: Dict[str, Any]) -> Any:
        # Préparer le prompt avec les données d'entrée
        if isinstance(input_data, dict):
            prompt = f"Input data: {json.dumps(input_data, indent=2)}"
        else:
            prompt = f"Input: {input_data}"

        result = await self.agent.run(prompt)

        # Essayer de parser la réponse comme JSON si c'est un agent de décision
        if self._is_decision_agent():
            try:
                return self._parse_structured_response(str(result.data))
            except Exception as e:
                print(f"   [PydanticAgent] ⚠️ Erreur de parsing JSON pour {self.name}: {e}")
                return {"error": "parsing_failed", "raw_response": str(result.data)}

        return result.data

    def set_tools(self, tools: List[Tool]) -> None:
        """Met à jour les outils et recrée l'agent"""
        self.tools = tools
        self._create_agent()

    def _create_agent(self):
        """Crée l'agent Pydantic AI avec les outils"""
        agent_kwargs = {"model": self.config.get("model", "openai:gpt-4o-mini"), "system_prompt": self.config.get("system_prompt", "")}

        # Ajouter les outils si disponibles
        if self.tools:
            agent_kwargs["tools"] = self.tools
            print(
                f"   [PydanticAgent] 🔧 Agent {self.name} configuré avec {len(self.tools)} outils: {[tool.function.__name__ for tool in self.tools]}"
            )

        self.agent = Agent(**agent_kwargs)

    def _is_decision_agent(self) -> bool:
        return "decision" in self.config.get("node_type", "") or "reviewer" in self.name.lower() or "tester" in self.name.lower()

    def _parse_structured_response(self, response: str) -> Dict[str, Any]:
        # Nettoyer la réponse pour extraire le JSON
        cleaned_response = re.sub(r"\n\s*", " ", response)

        # Chercher un JSON dans la réponse
        json_match = re.search(r"\{[^{}]*\}", cleaned_response)
        if json_match:
            json_str = json_match.group()
            try:
                json_str = re.sub(r'",\s*"', '", "', json_str)
                parsed = json.loads(json_str)
                return parsed
            except json.JSONDecodeError:
                pass

        # Fallback: essayer de parser la réponse complète
        try:
            return json.loads(cleaned_response)
        except Exception as e:
            print(f"   [PydanticAgent] ⚠️ Erreur de parsing JSON: {e}")
            # Si ça échoue, créer une structure par défaut
            if "approved" in response.lower():
                approved = "true" in response.lower() or '"approved": true' in response.lower()
                return {"approved": approved, "feedback": response, "final_review": False}
            return {"status": "unknown", "response": response}

    def get_name(self) -> str:
        return self.name
