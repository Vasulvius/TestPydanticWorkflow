import json
from typing import Any, Dict, Optional


class ConditionEvaluator:
    """Évaluateur de conditions générique pour les workflows"""

    @staticmethod
    def evaluate(condition: Optional[str], result: Any, context: Dict[str, Any]) -> bool:
        if condition is None:
            return True

        # Convertir le résultat en dict si nécessaire
        if isinstance(result, str):
            try:
                result = json.loads(result.replace("'", '"'))
            except Exception as e:
                print(f"   [ConditionEvaluator] ⚠️ Erreur de parsing JSON: {e}")

        if not isinstance(result, dict):
            return False

        return ConditionEvaluator._evaluate_generic_condition(condition, result, context)

    @staticmethod
    def _evaluate_generic_condition(condition: str, result: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Évalue les conditions génériques"""

        # Conditions booléennes simples (approved, passed, hired, etc.)
        if condition in result:
            return result[condition] is True

        # Conditions négatives (rejected = !approved, failed = !passed)
        negative_mappings = {"rejected": "approved", "failed": "passed", "not_hired": "hired", "incomplete": "complete"}

        if condition in negative_mappings:
            positive_field = negative_mappings[condition]
            if positive_field in result:
                return result[positive_field] is False

        # Conditions de statut
        if condition.startswith("status_"):
            expected_status = condition.replace("status_", "")
            return result.get("status") == expected_status

        # Conditions spéciales avec logique métier
        return ConditionEvaluator._evaluate_special_conditions(condition, result, context)

    @staticmethod
    def _evaluate_special_conditions(condition: str, result: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Conditions spéciales avec logique métier"""

        # Boucle de feedback avec limite d'itérations
        if condition == "rejected_not_final":
            is_approved = result.get("approved", False) or result.get("passed", False)
            is_final = result.get("final_review", False) or context.get("force_final_review", False)
            return not is_approved and not is_final

        # Finalisation forcée
        if condition == "final_review":
            return result.get("final_review", False) or context.get("force_final_review", False)

        # Présence de problèmes/bugs
        if condition == "has_issues":
            return result.get("has_bugs", False) or result.get("has_errors", False)

        if condition == "no_issues":
            return not (result.get("has_bugs", False) or result.get("has_errors", False))

        return False
