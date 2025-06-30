def register_content_tools(registry):
    """Outils spécifiques à la création de contenu"""

    @registry.register_tool("seo_analyze", "Analyse SEO d'un texte")
    async def seo_analyze(title: str, content: str, keywords: str) -> str:
        """Analyse les métriques SEO d'un contenu"""
        keyword_list = [k.strip() for k in keywords.split(",")]

        # Analyse basique
        title_score = sum(1 for kw in keyword_list if kw.lower() in title.lower())
        content_score = sum(content.lower().count(kw.lower()) for kw in keyword_list)

        return f"""Analyse SEO:
- Titre: {title_score}/{len(keyword_list)} mots-clés présents
- Contenu: {content_score} occurrences des mots-clés
- Longueur: {len(content)} caractères
- Recommandation: {'Bon' if content_score > 3 else 'À améliorer'}"""

    @registry.register_tool("grammar_check", "Vérification grammaticale basique")
    async def grammar_check(text: str) -> str:
        """Vérification grammaticale basique"""
        issues = []

        # Vérifications simples
        if not text.endswith("."):
            issues.append("Texte ne se termine pas par un point")
        if len([s for s in text.split(".") if len(s.strip()) > 100]) == 0:
            issues.append("Phrases trop courtes ou trop longues")

        return f"Issues trouvées: {'; '.join(issues) if issues else 'Aucune'}"

    @registry.register_tool("translate_text", "Traduction simple")
    async def translate_text(text: str, target_lang: str = "en") -> str:
        """Traduction basique via API gratuite (placeholder)"""
        # Implémentation placeholder - à remplacer par une vraie API
        return f"[TRADUCTION {target_lang.upper()}] {text}"
