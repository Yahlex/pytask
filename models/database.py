"""
Database - Gestion de la connexion SQLite
Crée et initialise la base de données
"""

import sqlite3
import os

class Database:
    """
    Classe singleton pour gérer la connexion à SQLite
    Crée automatiquement le dossier et les tables si nécessaire
    """

    def __init__(self, db_path: str = "database/tasks.db"):
        """
        Initialise la connexion à la base de données

        Args:
            db_path: Chemin vers le fichier SQLite (défaut: database/tasks.db)
        """
        self.db_path = db_path

        # Créer le dossier database/ s'il n'existe pas
        db_dir = os.path.dirname(db_path)
        if db_dir and not os.path.exists(db_dir):
            os.makedirs(db_dir)
            print(f"📁 Dossier '{db_dir}' créé")

        self.connection = None

    def get_connection(self) -> sqlite3.Connection:
        """
        Retourne la connexion SQLite (crée si nécessaire)
        Utilise row_factory pour accéder aux colonnes par nom
        """
        if self.connection is None:
            self.connection = sqlite3.connect(self.db_path)
            self.connection.row_factory = sqlite3.Row  # Accès par nom de colonne
        return self.connection

    def init_database(self):
        """
        Crée les tables si elles n'existent pas
        """
        conn = self.get_connection()
        cursor = conn.cursor()

        # Table des tâches (noms en français)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                description TEXT,
                etat TEXT NOT NULL DEFAULT 'À faire',
                date_echeance TEXT,
                date_fin TEXT,
                date_creation TEXT NOT NULL
            )
        """)

        # Table des commentaires (noms en français)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS comments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task_id INTEGER NOT NULL,
                texte TEXT NOT NULL,
                date_creation TEXT NOT NULL,
                FOREIGN KEY (task_id) REFERENCES tasks (id) ON DELETE CASCADE
            )
        """)

        conn.commit()
        print("✅ Tables créées/vérifiées")

    def close(self):
        """Ferme proprement la connexion"""
        if self.connection:
            self.connection.close()
            self.connection = None
            print("🔌 Connexion fermée")
