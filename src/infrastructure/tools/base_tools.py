import json
from pathlib import Path

import httpx


def register_base_tools(registry):
    """Enregistre les outils système de base"""

    @registry.register_tool("file_read", "Lit le contenu d'un fichier")
    async def file_read(filepath: str) -> str:
        """Lit le contenu d'un fichier"""
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            return f"Erreur lors de la lecture: {e}"

    @registry.register_tool("file_write", "Écrit du contenu dans un fichier")
    async def file_write(filepath: str, content: str) -> str:
        """Écrit du contenu dans un fichier"""
        try:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return f"Fichier '{filepath}' écrit avec succès"
        except Exception as e:
            return f"Erreur lors de l'écriture: {e}"

    @registry.register_tool("http_request", "Effectue une requête HTTP")
    async def http_request(url: str, method: str = "GET", data: str = None) -> str:
        """Effectue une requête HTTP"""
        try:
            async with httpx.AsyncClient() as client:
                if method.upper() == "POST" and data:
                    response = await client.post(url, json=json.loads(data))
                else:
                    response = await client.request(method, url)
                return f"Status: {response.status_code}\nContent: {response.text[:500]}"
        except Exception as e:
            return f"Erreur HTTP: {e}"

    @registry.register_tool("current_time", "Returns the current date and time")
    async def current_time() -> str:
        """Returns the current date and time"""
        from datetime import datetime

        print(f"   [BaseTools] 🕒 Current time tool registered: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}")

        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
