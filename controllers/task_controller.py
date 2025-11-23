"""
TaskController - Gère toute la logique métier liée aux tâches
C'est lui qui orchestre les actions entre la vue et le repository
"""

from datetime import datetime
from typing import List, Optional

from models.task import Task
from models.repository import Repository


class TaskController:
    """
    Contrôleur principal pour gérer les tâches
    J'isole ici toute la logique pour garder les vues simples
    """
    
    def __init__(self, repository: Repository):
        """Initialise avec une instance du repository"""
        self.repository = repository
    
    def create_task(self, titre: str, description: str, 
                   date_echeance: Optional[datetime] = None) -> Task:
        """
        Crée une nouvelle tâche avec validation
        Retourne la tâche créée avec son ID
        """
        # Validation
        if not titre or not titre.strip():
            raise ValueError("Le titre ne peut pas être vide")
        
        if not description or not description.strip():
            raise ValueError("La description ne peut pas être vide")
        
        # Création de la tâche
        task = Task(
            titre=titre.strip(),
            description=description.strip(),
            etat="À faire",
            date_creation=datetime.now(),
            date_echeance=date_echeance
        )
        
        # Sauvegarde en base
        task_id = self.repository.create_task(task)
        task.id = task_id
        
        return task
    
    def get_all_tasks(self) -> List[Task]:
        """Récupère toutes les tâches"""
        return self.repository.get_all_tasks()
    
    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """Récupère une tâche par son ID"""
        return self.repository.get_task_by_id(task_id)
    
    def update_task(self, task_id: int, titre: str, description: str, 
                   etat: str, date_echeance: Optional[datetime] = None):
        """
        Met à jour une tâche existante
        Gère automatiquement la date de fin si l'état passe à "Réalisé"
        """
        # Récupération de la tâche
        task = self.repository.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Tâche #{task_id} introuvable")
        
        # Validation
        if not titre or not titre.strip():
            raise ValueError("Le titre ne peut pas être vide")
        
        if not description or not description.strip():
            raise ValueError("La description ne peut pas être vide")
        
        # Mise à jour des champs
        task.titre = titre.strip()
        task.description = description.strip()
        task.etat = etat
        task.date_echeance = date_echeance
        
        # Si la tâche passe à "Réalisé", on enregistre la date de fin
        if etat == "Réalisé" and task.date_fin is None:
            task.date_fin = datetime.now()
        
        # Si on repasse la tâche en cours, on retire la date de fin
        if etat != "Réalisé" and task.date_fin is not None:
            task.date_fin = None
        
        # Sauvegarde
        self.repository.update_task(task)
    
    def delete_task(self, task_id: int):
        """Supprime une tâche (et tous ses commentaires)"""
        task = self.repository.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Tâche #{task_id} introuvable")
        
        self.repository.delete_task(task_id)
    
    def change_task_state(self, task_id: int, new_state: str):
        """Change uniquement l'état d'une tâche"""
        task = self.repository.get_task_by_id(task_id)
        if not task:
            raise ValueError(f"Tâche #{task_id} introuvable")
        
        task.etat = new_state
        
        # Gestion de la date de fin
        if new_state == "Réalisé" and task.date_fin is None:
            task.date_fin = datetime.now()
        elif new_state != "Réalisé":
            task.date_fin = None
        
        self.repository.update_task(task)
    
    def get_tasks_by_state(self, etat: str) -> List[Task]:
        """Filtre les tâches par état"""
        all_tasks = self.repository.get_all_tasks()
        return [task for task in all_tasks if task.etat == etat]
    
    def get_overdue_tasks(self) -> List[Task]:
        """Retourne les tâches en retard"""
        all_tasks = self.repository.get_all_tasks()
        return [task for task in all_tasks if task.est_en_retard()]
    
    def get_stats(self) -> dict:
        """
        Retourne des statistiques sur les tâches
        Utile pour un tableau de bord
        """
        all_tasks = self.repository.get_all_tasks()
        
        return {
            "total": len(all_tasks),
            "a_faire": len([t for t in all_tasks if t.etat == "À faire"]),
            "en_cours": len([t for t in all_tasks if t.etat == "En cours"]),
            "realise": len([t for t in all_tasks if t.etat == "Réalisé"]),
            "en_retard": len([t for t in all_tasks if t.est_en_retard()])
        }
