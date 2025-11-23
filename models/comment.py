"""
Modèle Comment - Représente un commentaire lié à une tâche
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Comment:
    """
    Un commentaire avec texte et date automatique
    task_id lie le commentaire à une tâche précise
    """
    texte: str
    task_id: int
    date_creation: datetime
    id: Optional[int] = None
    
    def __post_init__(self):
        """Validation du texte"""
        if not self.texte or not self.texte.strip():
            raise ValueError("Le texte du commentaire ne peut pas être vide")
