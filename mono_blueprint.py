import asyncio

from src.application.services import WorkflowService
from src.blueprints.workflow_definitions import MONO_AGENT_WITH_TOOLS


async def test_mono_agent():
    workflow_service = WorkflowService()

    # Message utilisateur en input
    user_message = (
        "Peux-tu m'aider à analyser ce texte et me dire quelle heure il est ? Voici le texte : 'Bonjour, comment allez-vous aujourd'hui ?'"
    )

    # Exécuter le workflow
    result = await workflow_service.execute_workflow_from_json(MONO_AGENT_WITH_TOOLS, user_message)

    print("🏁 Résultat :")
    print(result["final_result"])

    print("\n📊 Statistiques :")
    print(f"Étapes : {len(result['execution_history'])}")
    print(f"Itérations : {result['total_iterations']}")


if __name__ == "__main__":
    asyncio.run(test_mono_agent())
