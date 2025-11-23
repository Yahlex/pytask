"""
TaskFormView - Formulaire moderne de création/édition de tâches
Avec heure optionnelle et meilleure UX
"""

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLineEdit, QTextEdit, QDateEdit, QTimeEdit, QPushButton,
    QLabel, QMessageBox, QCheckBox, QGroupBox
)
from PySide6.QtCore import Qt, QDate, QTime
from datetime import datetime, time

from controllers.task_controller import TaskController
from models.task import Task

class TaskFormView(QDialog):
    """
    Formulaire modal avec :
    - Heure optionnelle (case à cocher)
    - Validation améliorée
    - Interface claire
    - DateEdit cliquable partout
    - Enter bloqué (pas de validation accidentelle)
    """

    def __init__(self, task_controller: TaskController, task_id: int = None, parent=None):
        super().__init__(parent)

        self.task_ctrl = task_controller
        self.task_id = task_id
        self.task = None

        # Mode édition
        if self.task_id:
            self.task = self.task_ctrl.get_task_by_id(self.task_id)
            if not self.task:
                QMessageBox.critical(self, "❌ Erreur", "Tâche introuvable !")
                self.reject()
                return

        self.setWindowTitle("✏️ Modifier la tâche" if self.task_id else "➕ Nouvelle tâche")
        self.setModal(True)
        self.setMinimumWidth(550)
        self.setMinimumHeight(450)

        self._setup_ui()

        if self.task:
            self._load_task_data()

    def keyPressEvent(self, event):
        """
        ✅ EMPÊCHER ENTER DE VALIDER LE FORMULAIRE PAR ACCIDENT
        Enter valide uniquement si on clique explicitement sur le bouton
        """
        if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
            # Si on est dans une zone de texte multiligne, on autorise le retour à la ligne
            if isinstance(self.focusWidget(), QTextEdit):
                super().keyPressEvent(event)
            # Sinon, on ignore (pas de validation automatique)
            else:
                event.ignore()
        else:
            super().keyPressEvent(event)

    def _setup_ui(self):
        """Construit le formulaire moderne"""

        layout = QVBoxLayout(self)
        layout.setSpacing(15)

        # === SECTION INFORMATIONS ===
        info_group = QGroupBox("📋 Informations principales")
        info_layout = QFormLayout()
        info_layout.setSpacing(10)

        # Titre
        self.input_titre = QLineEdit()
        self.input_titre.setPlaceholderText("Ex: Terminer le projet Python")
        self.input_titre.setMinimumHeight(35)
        info_layout.addRow("📌 Titre* :", self.input_titre)

        # Description
        self.input_description = QTextEdit()
        self.input_description.setPlaceholderText("Décrivez la tâche en détail...")
        self.input_description.setMaximumHeight(120)
        info_layout.addRow("📄 Description* :", self.input_description)

        info_group.setLayout(info_layout)
        layout.addWidget(info_group)

        # === SECTION ÉCHÉANCE ===
        echeance_group = QGroupBox("📅 Date d'échéance")
        echeance_layout = QVBoxLayout()
        echeance_layout.setSpacing(10)

        # Activation échéance
        self.checkbox_echeance = QCheckBox("Définir une date d'échéance")
        self.checkbox_echeance.stateChanged.connect(self._toggle_echeance)
        echeance_layout.addWidget(self.checkbox_echeance)

        # Date
        date_layout = QHBoxLayout()
        date_layout.addWidget(QLabel("📆 Date :"))

        # ✅ DATEEDIT CLIQUABLE PARTOUT
        self.input_date = QDateEdit()
        self.input_date.setCalendarPopup(True)  # Calendrier au clic
        self.input_date.setDisplayFormat("dd/MM/yyyy")
        self.input_date.setDate(QDate.currentDate().addDays(7))  # +7 jours
        self.input_date.setMinimumHeight(35)
        self.input_date.setEnabled(False)
        
        # ✅ FORCER LE CALENDRIER À S'OUVRIR AU CLIC N'IMPORTE OÙ
        self.input_date.lineEdit().setReadOnly(True)  # Empêche la saisie clavier
        self.input_date.setButtonSymbols(QDateEdit.ButtonSymbols.NoButtons)  # Cache le bouton de dropdown (on clique partout)

        date_layout.addWidget(self.input_date)
        echeance_layout.addLayout(date_layout)

        # Heure optionnelle
        heure_layout = QHBoxLayout()

        self.checkbox_heure = QCheckBox("Ajouter une heure précise")
        self.checkbox_heure.stateChanged.connect(self._toggle_heure)
        heure_layout.addWidget(self.checkbox_heure)

        self.input_heure = QTimeEdit()
        self.input_heure.setDisplayFormat("HH:mm")
        self.input_heure.setTime(QTime(9, 0))  # 09:00 par défaut
        self.input_heure.setMinimumHeight(35)
        self.input_heure.setEnabled(False)
        heure_layout.addWidget(self.input_heure)

        echeance_layout.addLayout(heure_layout)

        echeance_group.setLayout(echeance_layout)
        layout.addWidget(echeance_group)

        # Note
        note_label = QLabel("* Champs obligatoires")
        note_label.setStyleSheet("color: #6c7086; font-size: 10pt; font-style: italic;")
        layout.addWidget(note_label)

        layout.addStretch()

        # === BOUTONS ===
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)

        self.btn_cancel = QPushButton("❌ Annuler")
        self.btn_cancel.clicked.connect(self.reject)
        self.btn_cancel.setMinimumHeight(40)

        self.btn_save = QPushButton("💾 Enregistrer")
        self.btn_save.clicked.connect(self._on_save)
        # ✅ ON RETIRE setDefault(True) pour éviter validation par Enter
        self.btn_save.setMinimumHeight(40)

        button_layout.addStretch()
        button_layout.addWidget(self.btn_cancel)
        button_layout.addWidget(self.btn_save)

        layout.addLayout(button_layout)

    def _toggle_echeance(self, state):
        """Active/désactive la section date"""
        enabled = state == Qt.CheckState.Checked.value
        self.input_date.setEnabled(enabled)

        if enabled:
            self.checkbox_heure.setEnabled(True)
        else:
            self.checkbox_heure.setEnabled(False)
            self.checkbox_heure.setChecked(False)

    def _toggle_heure(self, state):
        """Active/désactive le sélecteur d'heure"""
        self.input_heure.setEnabled(state == Qt.CheckState.Checked.value)

    def _load_task_data(self):
        """Charge les données en mode édition"""
        self.input_titre.setText(self.task.titre)
        self.input_description.setPlainText(self.task.description)

        if self.task.date_echeance:
            self.checkbox_echeance.setChecked(True)

            # Date
            qdate = QDate(
                self.task.date_echeance.year,
                self.task.date_echeance.month,
                self.task.date_echeance.day
            )
            self.input_date.setDate(qdate)

            # Heure si différente de 00:00
            if self.task.date_echeance.time() != time(0, 0):
                self.checkbox_heure.setChecked(True)
                qtime = QTime(
                    self.task.date_echeance.hour,
                    self.task.date_echeance.minute
                )
                self.input_heure.setTime(qtime)

    def _validate_form(self) -> bool:
        """Validation des champs"""

        titre = self.input_titre.text().strip()
        description = self.input_description.toPlainText().strip()

        if not titre:
            QMessageBox.warning(self, "⚠️ Validation", "Le titre est obligatoire !")
            self.input_titre.setFocus()
            return False

        if len(titre) < 3:
            QMessageBox.warning(self, "⚠️ Validation", "Le titre doit contenir au moins 3 caractères !")
            self.input_titre.setFocus()
            return False

        if not description:
            QMessageBox.warning(self, "⚠️ Validation", "La description est obligatoire !")
            self.input_description.setFocus()
            return False

        if len(description) < 10:
            QMessageBox.warning(self, "⚠️ Validation", "La description doit contenir au moins 10 caractères !")
            self.input_description.setFocus()
            return False

        # Vérifier que la date n'est pas dans le passé
        if self.checkbox_echeance.isChecked():
            selected_date = self.input_date.date().toPython()
            today = QDate.currentDate().toPython()

            if selected_date < today:
                reply = QMessageBox.question(
                    self,
                    "⚠️ Date passée",
                    "La date d'échéance est dans le passé. Continuer quand même ?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                if reply == QMessageBox.StandardButton.No:
                    return False

        return True

    def _on_save(self):
        """Enregistrement de la tâche"""

        if not self._validate_form():
            return

        # Récupération des données
        titre = self.input_titre.text().strip()
        description = self.input_description.toPlainText().strip()

        date_echeance = None
        if self.checkbox_echeance.isChecked():
            qdate = self.input_date.date()

            if self.checkbox_heure.isChecked():
                # Avec heure
                qtime = self.input_heure.time()
                date_echeance = datetime(
                    qdate.year(), qdate.month(), qdate.day(),
                    qtime.hour(), qtime.minute()
                )
            else:
                # Sans heure (minuit par défaut)
                date_echeance = datetime(
                    qdate.year(), qdate.month(), qdate.day()
                )

        try:
            if self.task_id:
                # Édition
                self.task_ctrl.update_task(
                    self.task_id,
                    titre=titre,
                    description=description,
                    etat=self.task.etat,
                    date_echeance=date_echeance
                )
                QMessageBox.information(self, "✅ Succès", "Tâche modifiée avec succès !")
            else:
                # Création
                self.task_ctrl.create_task(
                    titre=titre,
                    description=description,
                    date_echeance=date_echeance
                )
                QMessageBox.information(self, "✅ Succès", "Tâche créée avec succès !")

            self.accept()

        except ValueError as e:
            QMessageBox.warning(self, "⚠️ Erreur", str(e))
        except Exception as e:
            QMessageBox.critical(self, "❌ Erreur", f"Erreur : {str(e)}")
