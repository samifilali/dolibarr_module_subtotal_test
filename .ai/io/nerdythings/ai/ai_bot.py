# Apache License
# Version 2.0, January 2004
# Author: Eugene Tkachenko
# Modifié par Sami Filali, ATM Consulting - 16/12/2024

from abc import ABC, abstractmethod
from ai.line_comment import LineComment


class AiBot(ABC):
    __no_response = "Aucun problème critique détecté"
    __problems = "erreurs de conventions de nommage Dolibarr"
    __chat_gpt_ask_long = """
Pour le code suivant, veuillez vérifier la conformité aux conventions de nommage et aux bonnes pratiques Dolibarr ci-dessous, et faites tous vos commentaires en français. 
Ne donnez aucune phrase d'introduction, listez uniquement les problèmes détectés au format : "numero_de_ligne : cause et effet". 
Si aucun problème n'est détecté, répondez "{no_response}".

Conventions Dolibarr à respecter :
- Nom des variables et fonctions : camelCase, privilégier l'anglais, utiliser des verbes pour les fonctions

DIFFS:

{diffs}

Code complet du fichier :

{code}
"""

    @abstractmethod
    def ai_request_diffs(self, code, diffs) -> str:
        pass

    @staticmethod
    def build_ask_text(code, diffs) -> str:
        return AiBot.__chat_gpt_ask_long.format(
            problems=AiBot.__problems,
            no_response=AiBot.__no_response,
            diffs=diffs,
            code=code,
        )

    @staticmethod
    def is_no_issues_text(source: str) -> bool:
        target = AiBot.__no_response.replace(" ", "")
        source_no_spaces = source.replace(" ", "")
        return source_no_spaces.startswith(target)

    @staticmethod
    def split_ai_response(input) -> list[LineComment]:
        if input is None or not input:
            return []

        lines = input.strip().split("\n")
        models = []

        for full_text in lines:
            number_str = ''
            number = 0
            full_text = full_text.strip()
            if len(full_text) == 0:
                continue

            reading_number = True
            for char in full_text.strip():
                if reading_number:
                    if char.isdigit():
                        number_str += char
                    else:
                        break

            if number_str:
                number = int(number_str)

            models.append(LineComment(line=number, text=full_text))
        return models
