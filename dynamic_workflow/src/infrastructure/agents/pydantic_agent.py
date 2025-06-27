import json
import re
from typing import Any, Dict

from pydantic_ai import Agent

from ...domain.interfaces.i_agent import IAgent


class PydanticAgent(IAgent):
    def __init__(self, agent_config: Dict[str, Any]):
        self.config = agent_config
        self.agent = Agent(model=agent_config.get("model", "openai:gpt-4o-mini"), system_prompt=agent_config.get("system_prompt", ""))
        self.name = agent_config.get("name", "GenericAgent")

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
                print(f"[PydanticAgent] ⚠️ Erreur parsing JSON: {e}")
                return {"error": "parsing_failed", "raw_response": str(result.data)}

        return result.data

    def _is_decision_agent(self) -> bool:
        return "decision" in self.config.get("node_type", "") or "reviewer" in self.name.lower() or "tester" in self.name.lower()

    def _parse_structured_response(self, response: str) -> Dict[str, Any]:
        # Nettoyer la réponse pour extraire le JSON
        # Supprimer les retours à la ligne dans les strings JSON
        cleaned_response = re.sub(r"\n\s*", " ", response)

        # Chercher un JSON dans la réponse
        json_match = re.search(r"\{[^{}]*\}", cleaned_response)
        if json_match:
            json_str = json_match.group()
            try:
                # Nettoyer encore plus le JSON
                json_str = re.sub(r'",\s*"', '", "', json_str)
                parsed = json.loads(json_str)
                print(f"✅ JSON parsé avec succès: {parsed}")
                return parsed
            except json.JSONDecodeError as e:
                print(f"❌ Erreur JSON parsing: {e}")
                print(f"JSON string: {json_str}")

        # Fallback: essayer de parser la réponse complète
        try:
            return json.loads(cleaned_response)
        except Exception as e:
            print(f"[PydanticAgent] ❌ Erreur de parsing JSON complet: {e}")
            # Si ça échoue, créer une structure par défaut
            if "approved" in response.lower():
                approved = "true" in response.lower() or '"approved": true' in response.lower()
                return {"approved": approved, "feedback": response, "final_review": False}
            return {"status": "unknown", "response": response}

    def get_name(self) -> str:
        return self.name
