import asyncio

from dotenv import load_dotenv
from src.application.services import WorkflowService
from src.blueprints import HIRING_WORKFLOW, WRITER_REVIEWER_WORKFLOW

load_dotenv()


async def main():
    workflow_service = WorkflowService()

    # Exemple 1: Writer-Reviewer
    print("=== Writer-Reviewer Workflow ===")
    result = await workflow_service.execute_workflow_from_json(
        WRITER_REVIEWER_WORKFLOW, {"topic": "AI in healthcare", "length": "1000 words"}
    )
    print(f"Final result: {result['final_result']}")
    print(f"Execution history: {result['execution_history']}")
    print(f"Iterations: {result['node_iterations']}")

    # # Exemple 2: Hiring Process
    # print("\n=== Hiring Workflow ===")
    # result = await workflow_service.execute_workflow_from_json(
    #     HIRING_WORKFLOW,
    #     {"name": "John Doe", "cv": "Senior Python Developer with 5 years experience", "position": "Senior Backend Developer"},
    # )
    # print(f"Final result: {result['final_result']}")
    # print(f"Execution history: {len(result['execution_history'])} steps")


if __name__ == "__main__":
    asyncio.run(main())
