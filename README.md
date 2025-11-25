# 📚 PyTask - Gestionnaire de Tâches Desktop

> **Projet universitaire** - Gestionnaire de tâches complet développé en Python avec architecture MVC  
> Auteur : **Alexis R.** | Année universitaire 2024-2025

---

## 📖 Table des matières

- [Présentation du projet](#-présentation-du-projet)
- [Captures d'écran](#️-captures-décran)
- [Architecture technique](#️-architecture-technique)
- [Fonctionnalités](#-fonctionnalités)
- [Technologies utilisées](#️-technologies-utilisées)
- [Installation et configuration](#-installation-et-configuration)
- [Utilisation](#-utilisation)
- [Structure du code](#-structure-du-code)
- [Mécanismes techniques détaillés](#-mécanismes-techniques-détaillés)
- [Choix techniques et justifications](#-choix-techniques-et-justifications)
- [Difficultés rencontrées](#-difficultés-rencontrées)
- [Améliorations futures](#-améliorations-futures)
- [Ressources et références](#-ressources)
- [Licence](#-licence)

---

## 🎯 Présentation du projet

**PyTask** est une application desktop de gestion de tâches développée dans le cadre d'un projet universitaire. L'objectif était de créer un gestionnaire complet suivant les principes de l'architecture **MVC (Modèle-Vue-Contrôleur)**, avec une interface graphique moderne et une persistance des données locale.

### Objectifs pédagogiques

- Maîtriser l'architecture **MVC** en Python
- Développer une interface graphique complète avec **PySide6** (Qt6)
- Gérer la persistance avec **SQLite**
- Respecter les bonnes pratiques Python (**PEP8**)
- Documenter et versionner un projet professionnel

### Spécifications fonctionnelles

✅ **CRUD complet** : Créer, lire, modifier, supprimer des tâches  
✅ **États multiples** : À faire, En cours, Réalisé, Abandonné, En attente  
✅ **Gestion des commentaires** : Chaque tâche peut avoir plusieurs commentaires  
✅ **Filtrage intelligent** : Aujourd'hui, Cette semaine, Ce mois, Urgent, Toutes  
✅ **Clôture de tâches** : Marquer une tâche comme terminée avec date automatique  
✅ **Interface moderne** : Mode sombre, responsive, intuitive  

---

## 🖼️ Captures d'écran

> **TODO :** Ajouter 3-4 captures d'écran ici :
> - Vue principale avec onglets
> - Formulaire d'ajout/modification
> - Modal de commentaires
> - Statistiques

---

## 🏗️ Architecture technique

### Principe MVC appliqué

L'application respecte strictement l'architecture **Modèle-Vue-Contrôleur** :

```
┌─────────────┐         ┌──────────────┐         ┌─────────┐
│    VUE      │ ◄────── │  CONTRÔLEUR  │ ◄────── │  MODÈLE │
│  (PySide6)  │         │   (Logique)  │         │ (Données)│
└─────────────┘         └──────────────┘         └─────────┘
      │                        │                       │
      │                        │                       │
   Interface             Orchestration           Entités +
   graphique              métier                 Repository
```

#### 🎨 **VUE** (`views/`)

- Affichage des données à l'utilisateur
- Capture des interactions (clics, saisies)
- **Aucune logique métier**
- Communication uniquement avec le contrôleur via signaux Qt

#### 🎮 **CONTRÔLEUR** (`controllers/`)

- Reçoit les actions de la vue
- Applique la logique métier (validation, règles de gestion)
- Demande au repository de persister les données
- Renvoie les résultats à la vue

#### 📦 **MODÈLE** (`models/`)

- Définit les entités (`Task`, `Comment`)
- Gère l'accès aux données (`Repository`)
- Contient la logique de persistance SQLite
- Indépendant de l'interface graphique

---

## ✨ Fonctionnalités

### 🎫 Gestion des tâches

| Fonctionnalité | Description |
|----------------|-------------|
| **Création** | Formulaire avec titre, description, dates, priorité, état |
| **Modification** | Double-clic sur une tâche ou bouton "Modifier" |
| **Suppression** | Avec confirmation (supprime aussi les commentaires associés) |
| **Clôture** | Bouton "Terminer" → marque comme "Réalisé" + date automatique |
| **États** | 5 états : À faire, En cours, Réalisé, Abandonné, En attente |
| **Dates** | Date de début et date de fin (optionnelles) |
| **Priorité** | Basse, Normale, Haute (avec code couleur) |

### 💬 Gestion des commentaires

- Ajouter des commentaires à chaque tâche
- Affichage chronologique avec horodatage
- Suppression individuelle avec confirmation
- Format : `[JJ/MM/AAAA HH:MM] Texte du commentaire`
- Badge indiquant le nombre de commentaires sur chaque tâche

### 🔎 Filtrage et tri

**5 onglets intelligents :**

| Onglet | Critère de filtrage |
|--------|---------------------|
| **Aujourd'hui** | Échéance = date du jour |
| **Cette semaine** | Échéance dans les 7 prochains jours |
| **Ce mois** | Échéance dans les 30 prochains jours |
| **Urgent** | Priorité = Haute OU échéance dépassée |
| **Toutes** | Toutes les tâches (sans filtre) |

### 💾 Persistance automatique

- Toutes les modifications sont **immédiatement sauvegardées** dans SQLite
- Base de données stockée dans `data/app.db`
- Initialisation automatique au premier lancement
- Transactions ACID pour garantir l'intégrité

---

## 🛠️ Technologies utilisées

| Technologie | Version | Utilisation |
|-------------|---------|-------------|
| **Python** | 3.11+ | Langage principal |
| **PySide6** | 6.6+ | Interface graphique (Qt6) |
| **SQLite** | 3.x | Base de données embarquée |
| **Git LFS** | 3.x | Gestion des fichiers volumineux |

### Pourquoi ces choix ?

#### ✅ **Python**
- Langage pédagogique, lisible et moderne
- Riche écosystème pour les applications GUI
- Excellent pour le prototypage rapide et la POO

#### ✅ **PySide6 (Qt6)**
- Framework GUI professionnel et multiplateforme (Windows, Linux, macOS)
- Plus moderne et complet que Tkinter
- Documentation exhaustive et communauté active
- Stylisation avancée avec QSS (comme du CSS)
- **Code pur Python** (pas de Qt Designer) pour une meilleure compréhension

#### ✅ **SQLite**
- Base de données locale, sans serveur à installer
- Intégrée nativement à Python (`sqlite3`)
- Parfaite pour une application desktop mono-utilisateur
- Plus robuste que JSON/CSV pour les relations de données
- Support des transactions, contraintes et triggers

**Comparaison SQLite vs JSON :**

| Critère | SQLite | JSON |
|---------|--------|------|
| Relations 1-N | ✅ Clés étrangères natives | ❌ Complexe à gérer manuellement |
| Requêtes | ✅ SQL puissant et optimisé | ❌ Parcours manuel des listes |
| Intégrité | ✅ Contraintes et validations | ❌ Validation manuelle |
| Performance | ✅ Index et optimisations | ❌ Chargement complet en RAM |
| Transactions | ✅ ACID (atomicité, cohérence) | ❌ Risque de corruption de fichier |

---

## 🚀 Installation et configuration

### Prérequis

- **Python 3.11** ou supérieur
- **Git** (avec Git LFS configuré)
- **pip** pour installer les dépendances

### Étapes d'installation

#### 1️⃣ Cloner le projet

```bash
# Installer Git LFS (si ce n'est pas déjà fait)
git lfs install

# Cloner le projet
git clone https://github.com/Yahlex/pytask.git
cd pytask
```

#### 2️⃣ Créer un environnement virtuel

**Windows :**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux / macOS :**
```bash
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

**Contenu de `requirements.txt` :**
```
PySide6>=6.6.0
```

#### 4️⃣ Lancer l'application

```bash
python main.py
```

**Sortie attendue :**
```
🚀 Démarrage de l'application...
✅ Tables créées/vérifiées
✅ Base de données initialisée
✅ Repository créé
✅ Contrôleurs créés
✅ Interface graphique lancée
```

---

## 📖 Utilisation

### Créer une tâche

1. Cliquer sur le bouton **"➕ Nouvelle tâche"**
2. Remplir le formulaire :
   - **Titre** (obligatoire)
   - **Description** (optionnelle)
   - **Date de début** (optionnelle)
   - **Date de fin** (optionnelle)
   - **Priorité** : Basse / Normale / Haute
   - **État** : À faire / En cours / Réalisé / Abandonné / En attente
3. Cliquer sur **"💾 Enregistrer"**

### Modifier une tâche

- **Double-cliquer** sur une ligne de tâche, **OU**
- Sélectionner une tâche et cliquer sur **"✏️ Modifier"**

### Supprimer une tâche

1. Sélectionner une tâche
2. Cliquer sur **"🗑️ Supprimer"**
3. Confirmer la suppression

> ⚠️ **Attention :** La suppression est définitive et supprime aussi tous les commentaires associés.

### Marquer comme terminée

1. Sélectionner une tâche
2. Cliquer sur **"✅ Terminer"**
3. La tâche passe automatiquement à l'état "Réalisé" et la date de fin est définie à aujourd'hui

### Ajouter un commentaire

1. Sélectionner une tâche
2. Cliquer sur **"💬 Commentaires"**
3. Saisir le texte dans la zone de saisie
4. Cliquer sur **"➕ Ajouter"**

### Naviguer entre les onglets

Les tâches sont automatiquement filtrées selon l'onglet sélectionné :

- **Aujourd'hui** : Tâches à échéance aujourd'hui
- **Cette semaine** : Échéance dans les 7 prochains jours
- **Ce mois** : Échéance dans les 30 prochains jours
- **Urgent** : Priorité haute OU échéance dépassée
- **Toutes** : Toutes les tâches sans filtre

---

## 📂 Structure du code

```
pytask/
│
├── main.py                      # Point d'entrée de l'application
│
├── data/
│   └── app.db                   # Base SQLite (géré par Git LFS)
│
├── models/
│   ├── task.py                  # Classe Task (entité)
│   ├── comment.py               # Classe Comment (entité)
│   └── repository.py            # CRUD + accès SQLite
│
├── views/
│   ├── main_window.py           # Fenêtre principale avec onglets
│   ├── task_form_view.py        # Formulaire création/modification
│   └── comment_view.py          # Modal de gestion des commentaires
│
├── controllers/
│   ├── task_controller.py       # Logique métier des tâches
│   └── comment_controller.py    # Logique métier des commentaires
│
├── styles/
│   └── app_style.py             # Stylesheet QSS (mode sombre)
│
├── requirements.txt             # Dépendances Python
├── .gitattributes               # Configuration Git LFS
└── README.md                    # Cette documentation
```

### 🔑 Rôle de chaque fichier

#### `main.py`
Point d'entrée de l'application. Responsabilités :
- Initialise la base de données SQLite
- Crée le repository
- Instancie les contrôleurs
- Lance l'interface graphique PySide6

```python
repository = Repository()
task_controller = TaskController(repository)
comment_controller = CommentController(repository)

app = QApplication(sys.argv)
window = MainWindow(task_controller, comment_controller)
window.show()
sys.exit(app.exec())
```

#### `models/repository.py`
Couche d'accès aux données. Responsabilités :
- Toutes les opérations SQLite (CREATE, READ, UPDATE, DELETE)
- Gestion des transactions
- Jointures et filtres complexes (par date, priorité, etc.)
- Initialisation des tables au premier lancement

#### `controllers/`
Logique métier pure. Responsabilités :
- Validation des données avant persistance
- Application des règles métier (ex: clôture de tâche)
- Aucune dépendance à l'interface graphique
- Gestion des erreurs métier

#### `views/`
Interfaces graphiques PySide6. Responsabilités :
- Affichage des données reçues du contrôleur
- Capture des interactions utilisateur
- Émission de signaux Qt vers les contrôleurs
- Aucun accès direct à SQLite

---

## 🔧 Mécanismes techniques détaillés

### 1️⃣ Clôture d'une tâche

La clôture d'une tâche est une fonctionnalité métier importante qui illustre bien l'architecture MVC.

#### **Déclenchement (Vue → Contrôleur)**

Dans `main_window.py` :

```python
def _on_complete_task(self):
    """Marque la tâche sélectionnée comme terminée"""
    selected_row = self._get_selected_row()
    if selected_row < 0:
        QMessageBox.warning(self, "Attention", "Veuillez sélectionner une tâche")
        return

    task_id = self.current_table.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)

    try:
        # ✅ Appel au contrôleur
        self.task_ctrl.complete_task(task_id)
        self._load_tasks()  # Rafraîchir l'affichage
        QMessageBox.information(self, "Succès", "✅ Tâche marquée comme terminée !")
    except Exception as e:
        QMessageBox.critical(self, "Erreur", f"Erreur : {str(e)}")
```

#### **Logique métier (Contrôleur)**

Dans `task_controller.py` :

```python
def complete_task(self, task_id: int):
    """
    Marque une tâche comme terminée
    - Change l'état à 'realise'
    - Définit date_fin à aujourd'hui si vide
    """
    task = self.repository.get_task_by_id(task_id)
    if not task:
        raise ValueError(f"Tâche #{task_id} introuvable")

    # ✅ Règles métier
    task.etat = "realise"
    
    # Si pas de date de fin définie, on met aujourd'hui
    if not task.date_fin:
        task.date_fin = datetime.now().date()

    # Persistance
    self.repository.update_task(task)
```

#### **Persistance (Modèle)**

Dans `repository.py` :

```python
def update_task(self, task: Task):
    """Met à jour une tâche existante"""
    query = """
        UPDATE tasks
        SET titre = ?, description = ?, date_debut = ?, date_fin = ?,
            priorite = ?, etat = ?
        WHERE id = ?
    """
    self.cursor.execute(query, (
        task.titre,
        task.description,
        task.date_debut.isoformat() if task.date_debut else None,
        task.date_fin.isoformat() if task.date_fin else None,
        task.priorite,
        task.etat,
        task.id
    ))
    self.conn.commit()
```

#### **Flux complet**

```
┌──────────────┐
│ 1. Utilisateur clique sur "Terminer"
│    → Vue capture l'événement
└────────┬─────┘
         │
         ▼
┌──────────────┐
│ 2. Vue appelle contrôleur.complete_task(task_id)
│    → Pas de logique métier dans la vue
└────────┬─────┘
         │
         ▼
┌──────────────┐
│ 3. Contrôleur applique les règles :
│    - Vérifie que la tâche existe
│    - Change l'état → "realise"
│    - Si date_fin vide → aujourd'hui
└────────┬─────┘
         │
         ▼
┌──────────────┐
│ 4. Contrôleur appelle repository.update_task()
│    → Exécution de la requête SQL UPDATE
└────────┬─────┘
         │
         ▼
┌──────────────┐
│ 5. Vue rafraîchit l'affichage
│    → Appel à _load_tasks()
└──────────────┘
```

**💡 Pourquoi cette approche ?**

✅ **Séparation des responsabilités** : La vue ne connaît pas les règles métier  
✅ **Testabilité** : Le contrôleur peut être testé sans lancer l'interface  
✅ **Réutilisabilité** : La logique de clôture peut être appelée depuis plusieurs vues  
✅ **Maintenabilité** : Si les règles changent, on modifie uniquement le contrôleur  

---

### 2️⃣ Gestion des dates

#### **Formats utilisés**

| Contexte | Format | Exemple |
|----------|--------|---------|
| **Interface utilisateur** | `JJ/MM/AAAA` | `15/01/2025` |
| **Base de données SQLite** | `YYYY-MM-DD` | `2025-01-15` |
| **Objet Python** | `datetime.date` | `date(2025, 1, 15)` |

#### **Conversion Interface → SQLite**

```python
from datetime import datetime

# Depuis QDateEdit (PySide6)
qdate = self.date_debut_edit.date()  # QDate
date_py = qdate.toPython()            # datetime.date
date_iso = date_py.isoformat()        # "2025-01-15"
```

#### **Conversion SQLite → Interface**

```python
from datetime import datetime

# Depuis la base de données
date_str = "2025-01-15"               # Format ISO
date_py = datetime.fromisoformat(date_str).date()  # datetime.date
date_fr = date_py.strftime("%d/%m/%Y")  # "15/01/2025"
```

#### **Filtrage par date (exemple : "Aujourd'hui")**

Dans `repository.py` :

```python
def get_tasks_today(self) -> List[Task]:
    """Récupère les tâches dont l'échéance est aujourd'hui"""
    today = datetime.now().date().isoformat()  # "2025-01-15"
    
    query = """
        SELECT * FROM tasks
        WHERE date(date_fin) = date(?)
        ORDER BY priorite DESC, date_fin ASC
    """
    self.cursor.execute(query, (today,))
    # ... conversion en objets Task
```

**💡 Astuce SQLite** : La fonction `date()` normalise les formats pour des comparaisons fiables.

---

### 3️⃣ Filtrage par onglets

Le filtrage se fait **côté base de données** pour optimiser les performances.

#### **Mécanisme de filtrage**

Dans `main_window.py` :

```python
def _on_tab_changed(self, index: int):
    """Appelé quand l'utilisateur change d'onglet"""
    # Déterminer la vue active
    if index == 0:
        self.current_view = "today"
        self.current_table = self.table_today
    elif index == 1:
        self.current_view = "week"
        self.current_table = self.table_week
    # ... etc.

    # Recharger les tâches avec le bon filtre
    self._load_tasks()
```

#### **Requêtes SQL par vue**

Dans `repository.py` :

```python
def get_tasks_week(self) -> List[Task]:
    """Tâches dont l'échéance est dans les 7 prochains jours"""
    today = datetime.now().date()
    week_end = today + timedelta(days=7)
    
    query = """
        SELECT * FROM tasks
        WHERE date(date_fin) BETWEEN date(?) AND date(?)
        ORDER BY date_fin ASC
    """
    self.cursor.execute(query, (today.isoformat(), week_end.isoformat()))
    # ...
```

**💡 Pourquoi filtrer en SQL ?**

✅ **Performance** : Pas besoin de charger toutes les tâches en mémoire  
✅ **Tri optimisé** : SQLite gère les index et l'ordre  
✅ **Scalabilité** : Fonctionne même avec des milliers de tâches  

---

### 4️⃣ Relation Task ↔ Comments

#### **Modèle relationnel**

```sql
CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    -- ...
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    texte TEXT NOT NULL,
    date_creation TEXT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);
```

**🔑 `ON DELETE CASCADE`** : Quand une tâche est supprimée, tous ses commentaires le sont automatiquement.

#### **Chargement des commentaires**

Dans `repository.py` :

```python
def get_comments_by_task(self, task_id: int) -> List[Comment]:
    """Récupère tous les commentaires d'une tâche (1-N)"""
    query = """
        SELECT id, task_id, texte, date_creation
        FROM comments
        WHERE task_id = ?
        ORDER BY date_creation DESC
    """
    self.cursor.execute(query, (task_id,))
    
    comments = []
    for row in self.cursor.fetchall():
        comment = Comment.from_row(row)
        comments.append(comment)
    
    return comments
```

#### **Affichage du badge "nombre de commentaires"**

Dans `main_window.py` :

```python
def _populate_table(self, table: QTableWidget, tasks: List[Task]):
    """Remplit un tableau avec les tâches"""
    # ...
    for row, task in enumerate(tasks):
        # ... autres colonnes
        
        # Colonne "Commentaires"
        nb_comments = self.comment_ctrl.count_comments_for_task(task.id)
        comment_text = f"💬 {nb_comments}" if nb_comments > 0 else "—"
        comment_item = QTableWidgetItem(comment_text)
        comment_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        table.setItem(row, 6, comment_item)
```

**💡 Optimisation possible** : Ajouter un compteur en cache pour éviter de requêter la base à chaque affichage.

---

## 🧠 Choix techniques et justifications

### Architecture MVC stricte

**Pourquoi MVC ?**

- ✅ **Séparation des responsabilités** : Chaque couche a un rôle clair
- ✅ **Testabilité** : On peut tester la logique métier sans l'interface
- ✅ **Maintenabilité** : Modifier la base de données n'impacte pas la vue
- ✅ **Réutilisabilité** : Les contrôleurs peuvent servir à plusieurs vues
- ✅ **Pédagogie** : Architecture standard enseignée en école

**Règles appliquées :**

| Couche | ✅ Autorisé | ❌ Interdit |
|--------|-------------|-------------|
| **Vue** | Signaux Qt, affichage | Logique métier, accès direct SQLite |
| **Contrôleur** | Validation, règles métier | Connaissance de l'UI (QWidget, etc.) |
| **Modèle** | CRUD, entités | Dépendances à PySide6 |

---

### Gestion des erreurs

**3 niveaux de gestion :**

#### **1️⃣ Validation dans le contrôleur**

```python
def create_task(self, titre: str, ...):
    if not titre or not titre.strip():
        raise ValueError("Le titre est obligatoire")
    
    if date_fin and date_debut and date_fin < date_debut:
        raise ValueError("La date de fin ne peut pas être avant la date de début")
    # ...
```

#### **2️⃣ Gestion dans la vue**

```python
try:
    self.task_controller.create_task(...)
    self.task_saved.emit()
    self.accept()
except ValueError as e:
    QMessageBox.warning(self, "Erreur de validation", str(e))
except Exception as e:
    QMessageBox.critical(self, "Erreur", f"Erreur inattendue : {str(e)}")
```

#### **3️⃣ Logging simple**

```python
print(f"❌ Erreur : {str(e)}")  # Pour le développement
```

**💡 Amélioration future** : Utiliser le module `logging` de Python pour des logs structurés.

---

### Signaux Qt pour le rafraîchissement

**Problème** : Quand on modifie une tâche dans une fenêtre modale, comment rafraîchir la liste principale ?

**Solution** : Signaux personnalisés PySide6

#### **Émission du signal (TaskFormView)**

```python
class TaskFormView(QDialog):
    task_saved = Signal()  # Signal personnalisé
    
    def _on_save(self):
        # ... validation et sauvegarde
        self.task_saved.emit()  # ✅ Émet le signal
        self.accept()
```

#### **Connexion du signal (MainWindow)**

```python
def _on_new_task(self):
    form = TaskFormView(self.task_ctrl, parent=self)
    form.task_saved.connect(self._load_tasks)  # ✅ Connexion
    form.exec()
```

**Flux complet :**

```
1. Utilisateur clique "Enregistrer" dans le formulaire
2. TaskFormView._on_save() émet task_saved
3. MainWindow._load_tasks() est appelée automatiquement
4. L'affichage se rafraîchit
```

---

## 🐛 Difficultés rencontrées

### 1️⃣ Configuration Git LFS

**Problème** : La base de données `app.db` peut rapidement dépasser la limite de 100 Mo de GitHub.

**Solution** :

```bash
# Installer Git LFS
git lfs install

# Déclarer les fichiers volumineux
git lfs track "*.db"

# Ajouter la configuration
git add .gitattributes
git commit -m "Configure Git LFS for database files"
```

**Fichier `.gitattributes` :**
```
*.db filter=lfs diff=lfs merge=lfs -text
```

---

### 2️⃣ Synchronisation des signaux Qt

**Problème initial** : La liste ne se rafraîchissait pas après modification d'une tâche.

**Cause** : Absence de signaux entre le formulaire modal et la fenêtre principale.

**Solution** : Utilisation des signaux Qt personnalisés (voir section précédente).

---

### 3️⃣ Gestion du mode sombre

**Problème** : Les styles par défaut de Qt sont peu lisibles.

**Solution** : Création d'un stylesheet QSS global dans `styles/app_style.py`

```python
APP_STYLESHEET = """
QWidget {
    background-color: #1e1e1e;
    color: #ffffff;
    font-family: 'Segoe UI', Arial;
    font-size: 11pt;
}

QPushButton {
    background-color: #0078d4;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 4px;
}

QPushButton:hover {
    background-color: #1084d8;
}
/* ... etc. */
"""
```

**Application du style** dans `main.py` :

```python
from styles.app_style import APP_STYLESHEET

app = QApplication(sys.argv)
app.setStyleSheet(APP_STYLESHEET)  # ✅ Style global
```

---

## 🚀 Améliorations futures

### Fonctionnalités métier

- 🔔 **Notifications système** pour les échéances proches
- 🔍 **Recherche full-text** dans les titres et descriptions
- 📊 **Statistiques graphiques** (tâches terminées par semaine, etc.)
- 🏷️ **Système de tags/catégories** (Travail, Personnel, Urgent, etc.)
- 🔁 **Tâches récurrentes** (quotidien, hebdomadaire, mensuel)
- 📎 **Pièces jointes** (fichiers liés à une tâche)
- 🌐 **Synchronisation cloud** (Google Drive, Dropbox, etc.)

### Améliorations techniques

- 🧪 **Tests unitaires** avec `pytest`
- 🔒 **Chiffrement de la base** avec `SQLCipher`
- 📦 **Packaging** avec `PyInstaller` (exécutable standalone)
- 🌍 **Internationalisation** (i18n) avec `Qt Linguist`
- 📈 **Logging avancé** avec le module `logging`
- 🎨 **Thèmes personnalisables** (clair/sombre/custom)
- 🖱️ **Drag & drop** pour réorganiser les tâches
- ⌨️ **Raccourcis clavier** (Ctrl+N, Ctrl+S, etc.)

### UX/UI

- 🎨 **Personnalisation des couleurs** par priorité/état
- 📱 **Mode tablette** avec interface tactile
- 🔊 **Feedback sonore** pour les actions
- 💾 **Export PDF/CSV** des tâches
- 📋 **Modèles de tâches** (templates réutilisables)

---

## 📚 Ressources

### Documentation officielle

- [PySide6 Documentation](https://doc.qt.io/qtforpython-6/)
- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Git LFS Documentation](https://git-lfs.com/)

### Tutoriels et guides

- [Real Python - PyQt Tutorials](https://realpython.com/tutorials/gui/)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [MVC Architecture Explained](https://en.wikipedia.org/wiki/Model%E2%80%93view%E2%80%93controller)

### Outils utilisés

- **IDE** : VS Code avec extensions Python et Qt
- **Versioning** : Git + GitHub
- **Documentation** : Markdown

---

## 📜 Licence

```
MIT License

Copyright (c) 2025 Alexis R.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 👤 Auteur

**Alexis R.**  
Étudiant en développement logiciel  
Année universitaire 2024-2025

📧 Contact : [ton-email@exemple.com]  
🔗 GitHub : [@Yahlex](https://github.com/Yahlex)  
💼 LinkedIn : [Ton profil]

---

## 🙏 Remerciements

- **Qt Company** pour le framework PySide6
- **Communauté Python** pour les ressources et la documentation
- **Enseignants** pour l'accompagnement sur le projet
- **Testeurs** pour leurs retours et suggestions

---

**⭐ Si ce projet vous a été utile, n'hésitez pas à le star sur GitHub !**

