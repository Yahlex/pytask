"""
CommentView - Affiche et gère les commentaires d'une tâche
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QListWidgetItem, QTextEdit, QLabel,
    QMessageBox
)
from PySide6.QtCore import Qt

from controllers.comment_controller import CommentController
from controllers.task_controller import TaskController


class CommentView(QDialog):
    """
    Fenêtre modale pour afficher et ajouter des commentaires
    """
    
    def __init__(self, task_id: int, task_controller: TaskController, 
                 comment_controller: CommentController, parent=None):
        super().__init__(parent)
        
        self.task_id = task_id
        self.task_ctrl = task_controller
        self.comment_ctrl = comment_controller
        
        # Récupération de la tâche
        self.task = self.task_ctrl.get_task_by_id(task_id)
        if not self.task:
            QMessageBox.critical(self, "Erreur", "Tâche introuvable !")
            self.reject()
            return
        
        self.setWindowTitle(f"💬 Commentaires - {self.task.titre}")
        self.setModal(True)
        self.setMinimumSize(600, 500)
        
        self._setup_ui()
        self._load_comments()
    
    def _setup_ui(self):
        """Construit l'interface"""
        
        layout = QVBoxLayout(self)
        
        # === INFO TÂCHE ===
        task_info_label = QLabel(f"📋 <b>{self.task.titre}</b> — {self.task.etat}")
        task_info_label.setStyleSheet("padding: 10px; background-color: #f0f0f0; border-radius: 5px;")
        layout.addWidget(task_info_label)
        
        # === LISTE DES COMMENTAIRES ===
        comments_label = QLabel("💬 Commentaires :")
        comments_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(comments_label)
        
        self.comment_list = QListWidget()
        self.comment_list.setAlternatingRowColors(True)
        layout.addWidget(self.comment_list)
        
        # === ZONE D'AJOUT ===
        add_label = QLabel("✍️ Ajouter un commentaire :")
        add_label.setStyleSheet("font-weight: bold; margin-top: 10px;")
        layout.addWidget(add_label)
        
        self.input_comment = QTextEdit()
        self.input_comment.setPlaceholderText("Écrivez votre commentaire ici...")
        self.input_comment.setMaximumHeight(80)
        layout.addWidget(self.input_comment)
        
        # === BOUTONS ===
        button_layout = QHBoxLayout()
        
        self.btn_add = QPushButton("➕ Ajouter")
        self.btn_add.clicked.connect(self._on_add_comment)
        
        self.btn_delete = QPushButton("🗑️ Supprimer")
        self.btn_delete.clicked.connect(self._on_delete_comment)
        self.btn_delete.setEnabled(False)
        
        self.btn_close = QPushButton("❌ Fermer")
        self.btn_close.clicked.connect(self.accept)
        
        button_layout.addWidget(self.btn_add)
        button_layout.addWidget(self.btn_delete)
        button_layout.addStretch()
        button_layout.addWidget(self.btn_close)
        
        layout.addLayout(button_layout)
        
        # Activer le bouton supprimer si sélection
        self.comment_list.itemSelectionChanged.connect(self._on_selection_changed)
    
    def _load_comments(self):
        """Charge les commentaires de la tâche"""
        self.comment_list.clear()
        
        comments = self.comment_ctrl.get_comments_for_task(self.task_id)
        
        if not comments:
            item = QListWidgetItem("Aucun commentaire pour le moment.")
            item.setForeground(Qt.GlobalColor.gray)
            self.comment_list.addItem(item)
            return
        
        for comment in comments:
            date_str = comment.date_creation.strftime("%d/%m/%Y %H:%M")
            text = f"[{date_str}] {comment.texte}"
            
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, comment.id)  # Stocke l'ID du commentaire
            self.comment_list.addItem(item)
    
    def _on_selection_changed(self):
        """Active/désactive le bouton supprimer selon la sélection"""
        has_selection = len(self.comment_list.selectedItems()) > 0
        # Ne pas permettre la suppression du message "Aucun commentaire"
        if has_selection:
            selected_item = self.comment_list.currentItem()
            has_valid_selection = selected_item.data(Qt.ItemDataRole.UserRole) is not None
            self.btn_delete.setEnabled(has_valid_selection)
        else:
            self.btn_delete.setEnabled(False)
    
    def _on_add_comment(self):
        """Ajoute un nouveau commentaire"""
        texte = self.input_comment.toPlainText().strip()
        
        if not texte:
            QMessageBox.warning(self, "Validation", "Le commentaire ne peut pas être vide !")
            return
        
        try:
            self.comment_ctrl.add_comment(self.task_id, texte)
            self.input_comment.clear()
            self._load_comments()
            QMessageBox.information(self, "Succès", "✅ Commentaire ajouté !")
        except Exception as e:
            QMessageBox.critical(self, "Erreur", f"Erreur lors de l'ajout : {str(e)}")
    
    def _on_delete_comment(self):
        """Supprime le commentaire sélectionné"""
        selected_item = self.comment_list.currentItem()
        if not selected_item:
            return
        
        comment_id = selected_item.data(Qt.ItemDataRole.UserRole)
        if not comment_id:
            return
        
        reply = QMessageBox.question(
            self,
            "Confirmation",
            "Supprimer ce commentaire ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.comment_ctrl.delete_comment(comment_id)
                self._load_comments()
                QMessageBox.information(self, "Succès", "✅ Commentaire supprimé !")
            except Exception as e:
                QMessageBox.critical(self, "Erreur", f"Erreur lors de la suppression : {str(e)}")
