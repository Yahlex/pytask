"""
Repository - Gère toute l'interaction avec la base SQLite
Centralise toutes les requêtes SQL
"""

from datetime import datetime
from typing import List, Optional
import sqlite3

from models.task import Task
from models.comment import Comment
from models.database import Database

class Repository:
    """
    Classe qui gère les requêtes SQL via l'objet Database
    """

    def __init__(self, database: Database):
        """
        Initialise le repository avec une instance Database

        Args:
            database: Instance de la classe Database
        """
        self.database = database

    def _get_connection(self) -> sqlite3.Connection:
        """Retourne la connexion SQLite depuis Database"""
        return self.database.get_connection()

    # ========== TÂCHES ==========

    def create_task(self, task: Task) -> int:
        """
        Crée une nouvelle tâche dans la base

        Returns:
            L'ID de la tâche créée
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO tasks (titre, description, etat, date_echeance, date_fin, date_creation)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            task.titre,
            task.description,
            task.etat,
            task.date_echeance.isoformat() if task.date_echeance else None,
            task.date_fin.isoformat() if task.date_fin else None,
            task.date_creation.isoformat()
        ))

        conn.commit()
        task.id = cursor.lastrowid
        return task.id

    def get_all_tasks(self) -> List[Task]:
        """Récupère toutes les tâches"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, titre, description, etat, date_echeance, date_fin, date_creation
            FROM tasks
            ORDER BY date_creation DESC
        """)

        tasks = []
        for row in cursor.fetchall():
            task = Task(
                id=row['id'],
                titre=row['titre'],
                description=row['description'],
                etat=row['etat'],
                date_echeance=datetime.fromisoformat(row['date_echeance']) if row['date_echeance'] else None,
                date_fin=datetime.fromisoformat(row['date_fin']) if row['date_fin'] else None,
                date_creation=datetime.fromisoformat(row['date_creation'])
            )
            tasks.append(task)

        return tasks

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Récupère une tâche par son ID"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, titre, description, etat, date_echeance, date_fin, date_creation
            FROM tasks
            WHERE id = ?
        """, (task_id,))

        row = cursor.fetchone()
        if not row:
            return None

        return Task(
            id=row['id'],
            titre=row['titre'],
            description=row['description'],
            etat=row['etat'],
            date_echeance=datetime.fromisoformat(row['date_echeance']) if row['date_echeance'] else None,
            date_fin=datetime.fromisoformat(row['date_fin']) if row['date_fin'] else None,
            date_creation=datetime.fromisoformat(row['date_creation'])
        )

    def update_task(self, task: Task) -> bool:
        """
        Met à jour une tâche existante

        Returns:
            True si la tâche a été modifiée
        """
        if task.id is None:
            return False

        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE tasks
            SET titre = ?, description = ?, etat = ?, date_echeance = ?, date_fin = ?
            WHERE id = ?
        """, (
            task.titre,
            task.description,
            task.etat,
            task.date_echeance.isoformat() if task.date_echeance else None,
            task.date_fin.isoformat() if task.date_fin else None,
            task.id
        ))

        conn.commit()
        return cursor.rowcount > 0

    def delete_task(self, task_id: int) -> bool:
        """
        Supprime une tâche (et ses commentaires via CASCADE)

        Returns:
            True si la tâche a été supprimée
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        conn.commit()

        return cursor.rowcount > 0

    def get_tasks_by_status(self, etat: str) -> List[Task]:
        """Récupère toutes les tâches d'un certain état"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, titre, description, etat, date_echeance, date_fin, date_creation
            FROM tasks
            WHERE etat = ?
            ORDER BY date_creation DESC
        """, (etat,))

        tasks = []
        for row in cursor.fetchall():
            task = Task(
                id=row['id'],
                titre=row['titre'],
                description=row['description'],
                etat=row['etat'],
                date_echeance=datetime.fromisoformat(row['date_echeance']) if row['date_echeance'] else None,
                date_fin=datetime.fromisoformat(row['date_fin']) if row['date_fin'] else None,
                date_creation=datetime.fromisoformat(row['date_creation'])
            )
            tasks.append(task)

        return tasks

    # ========== COMMENTAIRES ==========

    def create_comment(self, comment: Comment) -> int:
        """
        Crée un nouveau commentaire

        Returns:
            L'ID du commentaire créé
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO comments (task_id, texte, date_creation)
            VALUES (?, ?, ?)
        """, (
            comment.task_id,
            comment.texte,
            comment.date_creation.isoformat()
        ))

        conn.commit()
        comment.id = cursor.lastrowid
        return comment.id

    def get_comments_by_task(self, task_id: int) -> List[Comment]:
        """Récupère tous les commentaires d'une tâche"""
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT id, task_id, texte, date_creation
            FROM comments
            WHERE task_id = ?
            ORDER BY date_creation DESC
        """, (task_id,))

        comments = []
        for row in cursor.fetchall():
            comment = Comment(
                id=row['id'],
                task_id=row['task_id'],
                texte=row['texte'],
                date_creation=datetime.fromisoformat(row['date_creation'])
            )
            comments.append(comment)

        return comments

    def delete_comment(self, comment_id: int) -> bool:
        """
        Supprime un commentaire

        Returns:
            True si le commentaire a été supprimé
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM comments WHERE id = ?", (comment_id,))
        conn.commit()

        return cursor.rowcount > 0
