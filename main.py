import argparse
import asyncio

from dotenv import load_dotenv

from src.application.services import WorkflowService
from src.blueprints import (
    ADVANCED_CONTENT_WORKFLOW,
    DEVELOPMENT_WORKFLOW,
    HIRING_WORKFLOW,
    WRITER_REVIEWER_WORKFLOW,
)

load_dotenv()


async def run_writer_reviewer_workflow(workflow_service):
    """Test du workflow Writer-Reviewer"""
    print("=== Writer-Reviewer Workflow ===")
    result = await workflow_service.execute_workflow_from_json(
        WRITER_REVIEWER_WORKFLOW,
        {
            "topic": "L'intelligence artificielle dans les petites entreprises",
            "length": "100 mots",
            "format": "article de blog",
            "audience": "dirigeants de PME",
            "tone": "professionnel mais accessible",
        },
    )
    print_workflow_summary(result)
    return result


async def run_content_creation_with_tools(workflow_service):
    """Test du workflow avancé avec révision"""
    print("=== Advanced Content Creation Workflow ===")
    result = await workflow_service.execute_workflow_from_json(
        ADVANCED_CONTENT_WORKFLOW,
        {
            "topic": "Les 3 outils IA incontournables pour développeurs Python en 2025",
            "keywords": "IA, développeurs Python, outils, productivité, automatisation, 2025",
            "target_length": "300 mots",
            "tone": "technique mais accessible",
            "audience": "développeurs Python de niveau intermédiaire à avancé",
            "format": "guide pratique avec exemples de code",
        },
    )
    print("🏁 Article final:")
    print(result["final_result"])
    print(f"\n📊 Statistiques: {result['total_iterations']} itérations")
    return result


async def run_development_workflow(workflow_service):
    """Test du workflow Development"""
    print("=== Development Workflow ===")
    result = await workflow_service.execute_workflow_from_json(
        DEVELOPMENT_WORKFLOW,
        {
            "project": "API REST pour gestion de tâches",
            "requirements": ["CRUD operations pour les tâches", "Authentification JWT", "Base de données SQLite", "Documentation API"],
            "technology": "Python FastAPI",
            "timeline": "1 semaine",
        },
    )
    print_workflow_summary(result)
    return result


async def run_hiring_workflow_senior(workflow_service):
    """Test du workflow Hiring avec candidat senior"""
    print("=== Hiring Workflow (candidat senior) ===")
    result = await workflow_service.execute_workflow_from_json(
        HIRING_WORKFLOW,
        {
            "name": "Marie Dupont",
            "cv": "Senior Python Developer avec 6 ans d'expérience. Expertise en Django, FastAPI, PostgreSQL, Docker. A dirigé une équipe de 4 développeurs. Diplômée d'une école d'ingénieur.",
            "position": "Lead Backend Developer",
            "salary_range": "65000-75000",
            "team": "équipe produit de 8 personnes",
        },
    )
    print_workflow_summary(result)
    return result


async def run_hiring_workflow_junior(workflow_service):
    """Test du workflow Hiring avec candidat junior"""
    print("=== Hiring Workflow (candidat junior) ===")
    result = await workflow_service.execute_workflow_from_json(
        HIRING_WORKFLOW,
        {
            "name": "Paul Martin",
            "cv": "Développeur Python junior avec 1 an d'expérience. Connaissance basique de Flask et MySQL. Stage de 6 mois. Diplômé récemment.",
            "position": "Senior Backend Developer",
            "salary_range": "60000-70000",
            "team": "équipe technique senior",
        },
    )
    print_workflow_summary(result)
    return result


async def main():
    parser = argparse.ArgumentParser(
        description="Test des workflows avec options de sélection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemples d'utilisation:
  python main.py --all                    # Lance tous les tests
  python main.py --writer                 # Lance seulement le test Writer-Reviewer
  python main.py --dev --hiring-senior    # Lance Development et Hiring senior
  python main.py --hiring                 # Lance les deux tests de hiring
  python main.py --detailed               # Lance tous les tests avec détails
        """,
    )

    # Flags pour les workflows spécifiques
    parser.add_argument("--writer", action="store_true", help="Lance le test Writer-Reviewer workflow")
    parser.add_argument("--content-tools", action="store_true", help="Lance le test Content Creation with Tools")
    # parser.add_argument("--dev", action="store_true", help="Lance le test Development workflow")
    parser.add_argument("--hiring-senior", action="store_true", help="Lance le test Hiring workflow avec candidat senior")
    parser.add_argument("--hiring-junior", action="store_true", help="Lance le test Hiring workflow avec candidat junior")
    parser.add_argument("--hiring", action="store_true", help="Lance les deux tests de hiring (senior + junior)")

    # Flags globaux
    parser.add_argument("--all", "-a", action="store_true", help="Lance tous les tests")
    parser.add_argument("--detailed", action="store_true", help="Affiche l'historique détaillé de chaque workflow")
    parser.add_argument("--separator", default="=" * 60, help="Caractère de séparation entre les tests")

    args = parser.parse_args()

    # Si aucun flag n'est spécifié, lancer tous les tests par défaut
    if not any([args.writer, args.content_tools, args.hiring_senior, args.hiring_junior, args.hiring, args.all]):
        args.all = True

    workflow_service = WorkflowService()
    results = []

    # Définir quels tests lancer
    tests_to_run = []

    if args.all:
        # tests_to_run = ["writer", "dev", "hiring_senior", "hiring_junior"]
        tests_to_run = ["writer", "hiring_senior", "hiring_junior"]
    else:
        if args.writer:
            tests_to_run.append("writer")
        if args.content_tools:
            tests_to_run.append("content_tools")
        # if args.dev:
        #     tests_to_run.append("dev")
        if args.hiring or args.hiring_senior:
            tests_to_run.append("hiring_senior")
        if args.hiring or args.hiring_junior:
            tests_to_run.append("hiring_junior")

    # Exécuter les tests sélectionnés
    for i, test in enumerate(tests_to_run):
        if i > 0:  # Ajouter séparateur entre les tests
            print(f"\n{args.separator}\n")

        if test == "writer":
            result = await run_writer_reviewer_workflow(workflow_service)
        elif test == "content_tools":
            result = await run_content_creation_with_tools(workflow_service)
        elif test == "dev":
            result = await run_development_workflow(workflow_service)
        elif test == "hiring_senior":
            result = await run_hiring_workflow_senior(workflow_service)
        elif test == "hiring_junior":
            result = await run_hiring_workflow_junior(workflow_service)

        results.append((test, result))

        # Afficher les détails si demandé
        if args.detailed:
            print(f"\n📋 Historique détaillé pour {test}:")
            display_detailed_history(result["execution_history"])

    # Résumé final
    if len(results) > 1:
        print(f"\n{args.separator}")
        print("📈 RÉSUMÉ GLOBAL:")
        for test_name, result in results:
            total_iterations = result["total_iterations"]
            steps = len(result["execution_history"])
            print(f"   • {test_name}: {steps} étapes, {total_iterations} itérations")


def print_workflow_summary(result):
    """Affiche un résumé du workflow"""
    print("🏁 Résultat final:")
    print(f"   {str(result['final_result'])[:300]}...")
    print()
    print("📊 Statistiques:")
    print(f"   • Itérations par nœud: {result['node_iterations']}")
    print(f"   • Total d'itérations: {result['total_iterations']}")
    print(f"   • Étapes d'exécution: {len(result['execution_history'])}")

    print("\n📝 Parcours du workflow:")
    for i, step in enumerate(result["execution_history"], 1):
        node_name = step["node_id"].replace("_", " ").title()
        iteration = step["iteration"]
        print(f"   {i}. {node_name} (iter. {iteration})")


def display_detailed_history(history):
    """Affiche l'historique détaillé (pour debug)"""
    for i, step in enumerate(history, 1):
        print(f"\n--- Étape {i}: {step['node_id']} (itération {step['iteration']}) ---")
        print(f"Input: {str(step['input'])[:200]}...")
        print(f"Output: {str(step['output'])[:200]}...")
        print(f"Timestamp: {step['timestamp']}")


if __name__ == "__main__":
    asyncio.run(main())
