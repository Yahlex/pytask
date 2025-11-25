"""
MainWindow - Fenêtre principale avec vues multiples
Onglets : Aujourd'hui | Cette semaine | Ce mois | Urgent | Toutes
"""

from datetime import datetime, timedelta
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QPushButton, QTableWidget, QTableWidgetItem, QLabel,
    QComboBox, QMessageBox, QHeaderView, QTabWidget, QInputDialog
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor

from controllers.task_controller import TaskController
from controllers.comment_controller import CommentController
from styles.app_style import APP_STYLESHEET


class MainWindow(QMainWindow):
    """
    Fenêtre principale avec système d'onglets pour différentes vues
    """

    task_selected = Signal(int)

    def __init__(self, task_controller: TaskController, comment_controller: CommentController):
        super().__init__()

        self.task_ctrl = task_controller
        self.comment_ctrl = comment_controller
        self.current_view = "all"

        self.setWindowTitle("📋 Gestionnaire de Tâches Pro")
        self.setGeometry(100, 100, 1200, 700)
        
        # ✅ APPLICATION DU STYLE
        self.setStyleSheet(APP_STYLESHEET)

        self._setup_ui()
        self._load_tasks()

    def _setup_ui(self):
        """Construit l'interface avec onglets"""

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # === BARRE DE STATISTIQUES ===
        stats_layout = QHBoxLayout()

        self.label_total = QLabel("📊 Total : 0")
        self.label_a_faire = QLabel("📝 À faire : 0")
        self.label_en_cours = QLabel("⚙️ En cours : 0")
        self.label_realise = QLabel("✅ Réalisé : 0")
        self.label_retard = QLabel("⚠️ En retard : 0")

        for label in [self.label_total, self.label_a_faire, self.label_en_cours, 
                      self.label_realise, self.label_retard]:
            label.setStyleSheet("font-weight: bold; padding: 8px; font-size: 13px;")
            stats_layout.addWidget(label)

        stats_layout.addStretch()
        main_layout.addLayout(stats_layout)

        # === ONGLETS ===
        self.tabs = QTabWidget()
        self.tabs.currentChanged.connect(self._on_tab_changed)

        # Créer les 5 onglets
        self.table_today = self._create_table()
        self.table_week = self._create_table()
        self.table_month = self._create_table()
        self.table_urgent = self._create_table()
        self.table_all = self._create_table()

        self.tabs.addTab(self.table_today, "📅 Aujourd'hui")
        self.tabs.addTab(self.table_week, "📆 Cette semaine")
        self.tabs.addTab(self.table_month, "🗓️ Ce mois")
        self.tabs.addTab(self.table_urgent, "🔥 Urgent")
        self.tabs.addTab(self.table_all, "📋 Toutes")

        main_layout.addWidget(self.tabs)

        # === BOUTONS D'ACTION ===
        btn_layout = QHBoxLayout()

        self.btn_add = QPushButton("➕ Ajouter")
        self.btn_edit = QPushButton("✏️ Modifier")
        self.btn_delete = QPushButton("🗑️ Supprimer")
        self.btn_close = QPushButton("✅ Clôturer")
        self.btn_change_state = QPushButton("🔄 Changer l'état")
        self.btn_comments = QPushButton("💬 Commentaires")

        self.btn_add.clicked.connect(self._on_add_task)
        self.btn_edit.clicked.connect(self._on_edit_task)
        self.btn_delete.clicked.connect(self._on_delete_task)
        self.btn_close.clicked.connect(self._on_close_task) 
        self.btn_change_state.clicked.connect(self._on_change_state)
        self.btn_comments.clicked.connect(self._on_show_comments)

        for btn in [self.btn_add, self.btn_edit, self.btn_delete, 
                    self.btn_change_state, self.btn_comments, self.btn_close]:
            btn_layout.addWidget(btn)

        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

    def _create_table(self) -> QTableWidget:
        """Crée un tableau standardisé pour toutes les vues"""
        table = QTableWidget()
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "ID", "Titre", "État", "Échéance", "💬", "Priorité", "Retard"
        ])

        # Configuration du header
        header = table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.ResizeToContents)  # ID
        header.setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)           # Titre
        header.setSectionResizeMode(2, QHeaderView.ResizeMode.ResizeToContents)  # État
        header.setSectionResizeMode(3, QHeaderView.ResizeMode.ResizeToContents)  # Échéance
        header.setSectionResizeMode(4, QHeaderView.ResizeMode.ResizeToContents)  # Commentaires
        header.setSectionResizeMode(5, QHeaderView.ResizeMode.ResizeToContents)  # Priorité
        header.setSectionResizeMode(6, QHeaderView.ResizeMode.ResizeToContents)  # Retard

        table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        table.setAlternatingRowColors(True)
        table.verticalHeader().setVisible(False)

        # Double-clic pour éditer
        table.itemDoubleClicked.connect(self._on_row_double_clicked)

        return table

    def _get_current_table(self) -> QTableWidget:
        """Retourne le tableau de l'onglet actif"""
        index = self.tabs.currentIndex()
        return [self.table_today, self.table_week, self.table_month, 
                self.table_urgent, self.table_all][index]

    def _on_tab_changed(self, index: int):
        """Callback quand on change d'onglet"""
        views = ["today", "week", "month", "urgent", "all"]
        self.current_view = views[index]
        self._load_tasks()

    def _load_tasks(self):
        """Charge les tâches selon la vue active"""
        
        # Récupération des tâches filtrées
        if self.current_view == "today":
            tasks = self._filter_today()
            table = self.table_today
        elif self.current_view == "week":
            tasks = self._filter_week()
            table = self.table_week
        elif self.current_view == "month":
            tasks = self._filter_month()
            table = self.table_month
        elif self.current_view == "urgent":
            tasks = self._filter_urgent()
            table = self.table_urgent
        else:
            tasks = self.task_ctrl.get_all_tasks()
            table = self.table_all

        # Remplissage du tableau
        table.setRowCount(len(tasks))

        for row, task in enumerate(tasks):
            # ID
            table.setItem(row, 0, QTableWidgetItem(str(task.id)))

            # Titre
            table.setItem(row, 1, QTableWidgetItem(task.titre))

            # État
            etat_item = QTableWidgetItem(task.etat)
            if task.etat == "Réalisé":
                etat_item.setForeground(QColor("#a6e3a1"))
            elif task.etat == "En cours":
                etat_item.setForeground(QColor("#89b4fa"))
            else:
                etat_item.setForeground(QColor("#f9e2af"))
            table.setItem(row, 2, etat_item)

            # Échéance
            if task.date_echeance:
                echeance_str = task.date_echeance.strftime("%d/%m/%Y")
                echeance_item = QTableWidgetItem(echeance_str)
                if task.est_en_retard():
                    echeance_item.setForeground(QColor("#f38ba8"))
                table.setItem(row, 3, echeance_item)
            else:
                table.setItem(row, 3, QTableWidgetItem("-"))

            # Commentaires
            nb_comments = len(self.comment_ctrl.get_comments_for_task(task.id))
            table.setItem(row, 4, QTableWidgetItem(str(nb_comments)))

            # Priorité
            priorite = "🔥 Haute" if task.est_en_retard() else "Normal"
            priorite_item = QTableWidgetItem(priorite)
            if task.est_en_retard():
                priorite_item.setForeground(QColor("#f38ba8"))
            table.setItem(row, 5, priorite_item)

            # Retard
            retard_item = QTableWidgetItem("⚠️ OUI" if task.est_en_retard() else "")
            if task.est_en_retard():
                retard_item.setForeground(QColor("#f38ba8"))
            table.setItem(row, 6, retard_item)

        # Mise à jour des statistiques
        self._update_stats()

    def _filter_today(self):
        """Tâches avec échéance aujourd'hui"""
        all_tasks = self.task_ctrl.get_all_tasks()
        today = datetime.now().date()
        return [t for t in all_tasks if t.date_echeance and t.date_echeance.date() == today]

    def _filter_week(self):
        """Tâches de la semaine en cours"""
        all_tasks = self.task_ctrl.get_all_tasks()
        today = datetime.now().date()
        week_end = today + timedelta(days=7)
        return [t for t in all_tasks if t.date_echeance and today <= t.date_echeance.date() <= week_end]

    def _filter_month(self):
        """Tâches du mois en cours"""
        all_tasks = self.task_ctrl.get_all_tasks()
        today = datetime.now()
        return [t for t in all_tasks if t.date_echeance and 
                t.date_echeance.month == today.month and 
                t.date_echeance.year == today.year]

    def _filter_urgent(self):
        """Tâches en retard ou échéance < 3 jours"""
        all_tasks = self.task_ctrl.get_all_tasks()
        today = datetime.now().date()
        limit = today + timedelta(days=3)
        return [t for t in all_tasks if t.date_echeance and 
                t.date_echeance.date() <= limit and t.etat != "Réalisé"]

    def _update_stats(self):
        """Met à jour la barre de statistiques"""
        stats = self.task_ctrl.get_stats()

        self.label_total.setText(f"📊 Total : {stats['total']}")
        self.label_a_faire.setText(f"📝 À faire : {stats['a_faire']}")
        self.label_en_cours.setText(f"⚙️ En cours : {stats['en_cours']}")
        self.label_realise.setText(f"✅ Réalisé : {stats['realise']}")
        self.label_retard.setText(f"⚠️ En retard : {stats['en_retard']}")

    def _get_selected_task_id(self) -> int:
        """Retourne l'ID de la tâche sélectionnée"""
        table = self._get_current_table()
        selected_rows = table.selectionModel().selectedRows()

        if not selected_rows:
            QMessageBox.warning(self, "⚠️ Attention", "Aucune tâche sélectionnée !")
            return 0

        row = selected_rows[0].row()
        return int(table.item(row, 0).text())

    def _on_add_task(self):
        """Ouvre le formulaire de création"""
        from views.task_form_view import TaskFormView

        dialog = TaskFormView(self.task_ctrl, parent=self)
        if dialog.exec():
            self._load_tasks()

    def _on_edit_task(self):
        """Ouvre le formulaire d'édition"""
        task_id = self._get_selected_task_id()
        if not task_id:
            return

        from views.task_form_view import TaskFormView

        dialog = TaskFormView(self.task_ctrl, task_id=task_id, parent=self)
        if dialog.exec():
            self._load_tasks()

    def _on_delete_task(self):
        """Supprime la tâche sélectionnée"""
        task_id = self._get_selected_task_id()
        if not task_id:
            return

        task = self.task_ctrl.get_task_by_id(task_id)

        reply = QMessageBox.question(
            self,
            "❓ Confirmer la suppression",
            f"Voulez-vous vraiment supprimer la tâche :\n\n« {task.titre} » ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            self.task_ctrl.delete_task(task_id)
            QMessageBox.information(self, "✅ Succès", "Tâche supprimée !")
            self._load_tasks()

    def _on_change_state(self):
        """Change l'état de la tâche"""
        task_id = self._get_selected_task_id()
        if not task_id:
            return

        task = self.task_ctrl.get_task_by_id(task_id)

        etats = ["À faire", "En cours", "Réalisé"]
        nouvel_etat, ok = QInputDialog.getItem(
            self,
            "🔄 Changer l'état",
            f"Nouvel état pour « {task.titre} » :",
            etats,
            etats.index(task.etat),
            False
        )

        if ok and nouvel_etat:
            # Appel avec titre + description
            self.task_ctrl.update_task(
                task_id, 
                titre=task.titre,
                description=task.description,
                etat=nouvel_etat,
                date_echeance=task.date_echeance
            )
            QMessageBox.information(self, "✅ Succès", f"État changé en « {nouvel_etat} » !")
            self._load_tasks()

    def _on_show_comments(self):
        """Affiche les commentaires de la tâche"""
        task_id = self._get_selected_task_id()
        if not task_id:
            return

        from views.comment_view import CommentView

        dialog = CommentView(self.comment_ctrl, task_id, parent=self)
        dialog.exec()
        self._load_tasks()
    
    def _on_close_task(self):
        """Clôture rapide de la tâche sélectionnée"""
        task_id = self._get_selected_task_id()
        if not task_id:
            return

        task = self.task_ctrl.get_task_by_id(task_id)

        if task.etat == "Réalisé":
            QMessageBox.information(self, "ℹ️ Information", "Cette tâche est déjà clôturée.")
            return

        reply = QMessageBox.question(
            self,
            "❓ Confirmer la clôture",
            f"Voulez-vous vraiment clôturer la tâche :\n\n« {task.titre} » ?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )

        if reply == QMessageBox.StandardButton.Yes:
            try:
                self.task_ctrl.close_task(task_id)
                QMessageBox.information(self, "✅ Succès", "Tâche clôturée !")
                self._load_tasks()
            except ValueError as e:
                QMessageBox.warning(self, "⚠️ Attention", str(e))

    def _on_row_double_clicked(self):
        """Double-clic = édition"""
        self._on_edit_task()

    def refresh(self):
        """Méthode publique pour rafraîchir depuis l'extérieur"""
        self._load_tasks()
