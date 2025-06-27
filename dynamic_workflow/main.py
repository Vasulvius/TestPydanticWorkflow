import asyncio

from dotenv import load_dotenv
from src.application.services import WorkflowService
from src.blueprints import HIRING_WORKFLOW, WRITER_REVIEWER_WORKFLOW

load_dotenv()


async def main():
    workflow_service = WorkflowService()

    # Exemple 1: Writer-Reviewer avec un sujet plus approprié
    print("=== Writer-Reviewer Workflow ===")
    result = await workflow_service.execute_workflow_from_json(
        WRITER_REVIEWER_WORKFLOW,
        {
            "topic": "L'intelligence artificielle dans les petites entreprises",
            "length": "800 mots",
            "format": "article de blog",
            "audience": "dirigeants de PME",
        },
    )
    print()
    print(f"Final result: {result['final_result']}")
    print()
    print(f"Iterations: {result['node_iterations']}")

    # # Exemple 2: Hiring Process
    # print("\n=== Hiring Workflow ===")
    # result = await workflow_service.execute_workflow_from_json(
    #     HIRING_WORKFLOW,
    #     {"name": "John Doe", "cv": "Senior Python Developer with 5 years experience", "position": "Senior Backend Developer"},
    # )
    # print(f"Final result: {result['final_result']}")
    # print(f"Execution history: {len(result['execution_history'])} steps")


def display_history(history):
    for step in history:
        print()
        print("=== Step History ===")
        print(f"Node: {step['node_id']}, Input: {step['input']}, Output: {step['output']}")
        print()


if __name__ == "__main__":
    asyncio.run(main())
