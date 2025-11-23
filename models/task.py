"""
Modèle Task - Représente une tâche dans mon application
J'utilise une dataclass pour simplifier la gestion des attributs
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Task:
    """
    Une tâche avec tous ses attributs
    J'ai mis id en Optional parce qu'il sera None avant insertion en base
    """
    titre: str
    description: str
    etat: str  # "À faire", "En cours", "Réalisé"
    date_creation: datetime
    date_echeance: Optional[datetime] = None
    date_fin: Optional[datetime] = None
    id: Optional[int] = None
    
    def __post_init__(self):
        """Validation basique après création"""
        etats_valides = ["À faire", "En cours", "Réalisé"]
        if self.etat not in etats_valides:
            raise ValueError(f"État invalide. Doit être parmi : {etats_valides}")
    
    def est_terminee(self) -> bool:
        """Check rapide pour savoir si la tâche est finie"""
        return self.etat == "Réalisé"
    
    def est_en_retard(self) -> bool:
        """Vérifie si la date d'échéance est dépassée"""
        if not self.date_echeance or self.est_terminee():
            return False
        return datetime.now() > self.date_echeance
