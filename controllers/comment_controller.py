"""
CommentController - Gère la logique métier des commentaires
Plus simple que TaskController car moins de logique
"""

from datetime import datetime
from typing import List

from models.comment import Comment
from models.repository import Repository

class CommentController:
    """
    Contrôleur pour gérer les commentaires
    """

    def __init__(self, repository: Repository):
        """Initialise avec une instance du repository"""
        self.repository = repository

    def add_comment(self, task_id: int, texte: str) -> Comment:
        """
        Ajoute un commentaire à une tâche
        Retourne le commentaire créé avec son ID
        """
        # Validation
        if not texte or not texte.strip():
            raise ValueError("Le commentaire ne peut pas être vide")

        # Vérification que la tâche existe
        task = self.repository.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Tâche #{task_id} introuvable")

        # Création du commentaire
        comment = Comment(
            texte=texte.strip(),
            task_id=task_id,
            date_creation=datetime.now()
        )

        # Sauvegarde
        comment_id = self.repository.create_comment(comment)
        comment.id = comment_id

        return comment

    def get_comments_for_task(self, task_id: int) -> List[Comment]:
        """Récupère tous les commentaires d'une tâche"""
        return self.repository.get_comments_by_task(task_id)

    def delete_comment(self, comment_id: int):
        """Supprime un commentaire"""
        self.repository.delete_comment(comment_id)

    def count_comments_for_task(self, task_id: int) -> int:
        """Compte le nombre de commentaires d'une tâche"""
        comments = self.repository.get_comments_by_task(task_id)
        return len(comments)
