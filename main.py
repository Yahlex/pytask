"""
main.py - Point d'entrée de l'application
Lance l'interface graphique avec tous les contrôleurs
"""

import sys
from PySide6.QtWidgets import QApplication

from models.database import Database
from models.repository import Repository
from controllers.task_controller import TaskController
from controllers.comment_controller import CommentController
from views.main_window import MainWindow
from views.task_form_view import TaskFormView
from views.comment_view import CommentView
from styles.app_style import APP_STYLESHEET  # ← AJOUT

def main():
    """
    Fonction principale qui :
    1. Initialise la base de données
    2. Crée les contrôleurs
    3. Lance l'interface graphique
    """

    # === INITIALISATION ===
    print("🚀 Démarrage de l'application...")

    # Base de données SQLite
    db = Database()
    db.init_database()
    print("✅ Base de données initialisée")

    # Repository (accès aux données)
    repository = Repository(db)
    print("✅ Repository créé")

    # Contrôleurs (logique métier)
    task_ctrl = TaskController(repository)
    comment_ctrl = CommentController(repository)
    print("✅ Contrôleurs créés")

    # === LANCEMENT DE L'APPLICATION QT ===
    app = QApplication(sys.argv)
    app.setApplicationName("Gestionnaire de Tâches")
    
    # ✨ Appliquer le thème sombre moderne
    app.setStyleSheet(APP_STYLESHEET)

    # Fenêtre principale
    main_window = MainWindow(task_ctrl, comment_ctrl)

    # === CONNEXION DES SIGNAUX ===

    # Gestion du signal task_selected (nouvelle tâche ou édition)
    def on_task_selected(task_id: int):
        if task_id == -1:  # Nouvelle tâche
            form = TaskFormView(task_ctrl, parent=main_window)
            if form.exec():
                main_window.refresh()
        else:  # Édition
            form = TaskFormView(task_ctrl, task_id=task_id, parent=main_window)
            if form.exec():
                main_window.refresh()

    main_window.task_selected.connect(on_task_selected)

    # Quand on clique sur "Commentaires"
    def open_comment_view():
        task_id = main_window._get_selected_task_id()
        if task_id:
            comment_view = CommentView(task_id, task_ctrl, comment_ctrl, parent=main_window)
            comment_view.exec()

    main_window.btn_comments.clicked.connect(open_comment_view)

    # === AFFICHAGE ===
    main_window.show()
    print("✅ Interface graphique lancée\n")
    print("=" * 50)
    print("🎨 APPLICATION PRÊTE EN MODE SOMBRE !")
    print("=" * 50)

    # Boucle d'événements Qt
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
