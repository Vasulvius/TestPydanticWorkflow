import re
from datetime import datetime


def register_business_tools(registry):
    """Enregistre les outils métier génériques"""

    @registry.register_tool("validate_email", "Valide une adresse email")
    async def validate_email(email: str) -> str:
        """Valide une adresse email"""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        is_valid = bool(re.match(pattern, email))
        return f"Email '{email}' est {'valide' if is_valid else 'invalide'}"

    @registry.register_tool("word_count", "Compte les mots dans un texte")
    async def word_count(text: str) -> str:
        """Compte les mots dans un texte"""
        words = len(text.split())
        chars = len(text)
        return f"Mots: {words}, Caractères: {chars}"

    @registry.register_tool("current_time", "Retourne la date et heure actuelles")
    async def current_time() -> str:
        """Retourne la date et heure actuelles"""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
