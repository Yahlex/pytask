# 📚 PyTask - Gestionnaire de Tâches Desktop

> **Projet universitaire** - Gestionnaire de tâches complet développé en Python avec architecture MVC  
> Auteur : **Alexis R.** | Année universitaire 2024-2025

---

## 📖 Table des matières

- [Présentation du projet](#-présentation-du-projet)
  - [Objectifs pédagogiques](#objectifs-pédagogiques)
  - [Spécifications fonctionnelles](#spécifications-fonctionnelles)
- [Captures d'écran](#️-captures-décran)
- [Architecture technique](#️-architecture-technique)
  - [Principe MVC appliqué](#principe-mvc-appliqué)
- [Fonctionnalités](#-fonctionnalités)
  - [Gestion des tâches](#-gestion-des-tâches)
  - [Gestion des commentaires](#-gestion-des-commentaires)
  - [Filtrage et tri](#-filtrage-et-tri)
  - [Persistance automatique](#-persistance-automatique)
- [Technologies utilisées](#️-technologies-utilisées)
  - [Pourquoi ces choix ?](#pourquoi-ces-choix-)
- [Installation et configuration](#-installation-et-configuration)
  - [Prérequis](#prérequis)
  - [Étapes d'installation](#étapes-dinstallation)
- [Utilisation](#-utilisation)
  - [Créer une tâche](#créer-une-tâche)
  - [Modifier une tâche](#modifier-une-tâche)
  - [Supprimer une tâche](#supprimer-une-tâche)
  - [Marquer comme terminée](#marquer-comme-terminée)
  - [Ajouter un commentaire](#ajouter-un-commentaire)
  - [Naviguer entre les onglets](#naviguer-entre-les-onglets)
- [Structure du code](#-structure-du-code)
  - [Rôle de chaque fichier](#-rôle-de-chaque-fichier)
- [Choix techniques et justifications](#-choix-techniques-et-justifications)
  - [Architecture MVC stricte](#architecture-mvc-stricte)
  - [Gestion des dates](#gestion-des-dates)
  - [Gestion des erreurs](#gestion-des-erreurs)
  - [Relation 1-N (Task ↔ Comments)](#relation-1-n-task--comments)
- [Difficultés rencontrées](#-difficultés-rencontrées)
  - [1. Configuration Git LFS](#1-configuration-git-lfs)
  - [2. Certificat SSL auto-signé](#2-certificat-ssl-auto-signé)
  - [3. Synchronisation des signaux Qt](#3-synchronisation-des-signaux-qt)
  - [4. Gestion du mode sombre](#4-gestion-du-mode-sombre)
- [Améliorations futures](#-améliorations-futures)
  - [Priorité haute (v2.0)](#priorité-haute-v20)
  - [Priorité moyenne (v2.5)](#priorité-moyenne-v25)
  - [Priorité basse (v3.0)](#priorité-basse-v30)
- [Ressources et références](#-ressources-et-références)
- [Licence](#-licence)
- [Auteur](#-auteur)
- [Remerciements](#-remerciements)

---

## 🎯 Présentation du projet

**PyTask** est une application desktop de gestion de tâches développée dans le cadre d'un projet universitaire. L'objectif était de créer un gestionnaire complet suivant les principes de l'architecture **MVC (Modèle-Vue-Contrôleur)**, avec une interface graphique moderne et une persistance des données locale.

### Objectifs pédagogiques

- Maîtriser l'architecture **MVC** en Python
- Développer une interface graphique complète avec **PySide6** (Qt)
- Gérer la persistance avec **SQLite**
- Respecter les bonnes pratiques Python (**PEP8**)
- Documenter et versionner un projet professionnel

### Spécifications fonctionnelles

✅ **CRUD complet** : Créer, lire, modifier, supprimer des tâches  
✅ **États multiples** : À faire, En cours, Réalisé, Abandonné, En attente  
✅ **Gestion des commentaires** : Chaque tâche peut avoir plusieurs commentaires  
✅ **Filtrage intelligent** : Aujourd'hui, Cette semaine, Ce mois  
✅ **Clôture de tâches** : Marquer une tâche comme terminée avec date automatique  
✅ **Interface moderne** : Mode sombre, responsive, intuitive  

---

## 🖼️ Captures d'écran


### Vue principale - Liste des tâches
┌─────────────────────────────────────────────────────┐
│  PyTask - Gestionnaire de Tâches          [─][□][×] │
├─────────────────────────────────────────────────────┤
│  [+ Nouvelle tâche]                                 │
├─────────────────────────────────────────────────────┤
│  📅 Aujourd'hui | Cette semaine | Ce mois          │
├─────────────────────────────────────────────────────┤
│  ☐ Titre de la tâche           [Modifier][Suppr]   │
│     📝 Description courte...                        │
│     🏷️ En cours | 📅 15/01/2025                     │
│  ─────────────────────────────────────────────────  │
│  ☑ Tâche terminée              [Modifier][Suppr]   │
│     📝 Cette tâche est complète                     │
│     🏷️ Réalisé | 📅 14/01/2025                      │
└─────────────────────────────────────────────────────┘


---

## 🏗️ Architecture technique

### Principe MVC appliqué

L'application respecte strictement l'architecture **Modèle-Vue-Contrôleur** :
┌─────────────┐         ┌──────────────┐         ┌─────────┐
│    VUE      │ ◄────── │  CONTRÔLEUR  │ ◄────── │  MODÈLE │
│  (PySide6)  │         │   (Logique)  │         │ (Données)│
└─────────────┘         └──────────────┘         └─────────┘
      │                        │                       │
      │                        │                       │
   Interface             Orchestration           Entités +
   graphique              métier                 Repository


#### 🎨 **VUE** (`views/`)

- Affichage des données à l'utilisateur
- Capture des interactions (clics, saisies)
- **Aucune logique métier**
- Communication uniquement avec le contrôleur

#### 🎮 **CONTRÔLEUR** (`controllers/`)

- Reçoit les actions de la vue
- Applique la logique métier
- Demande au repository de persister les données
- Met à jour la vue

#### 📦 **MODÈLE** (`models/`)

- Définit les entités (`Task`, `Comment`)
- Gère l'accès aux données (`Repository`)
- Contient la logique de persistance SQLite

---

## ✨ Fonctionnalités

### 🎫 Gestion des tâches

| Fonctionnalité | Description |
|----------------|-------------|
| **Création** | Formulaire avec titre, description, dates, priorité, état |
| **Modification** | Double-clic ou bouton "Modifier" |
| **Suppression** | Avec confirmation |
| **Clôture** | Marque une tâche comme "Réalisé" automatiquement |
| **États** | 5 états : À faire, En cours, Réalisé, Abandonné, En attente |
| **Dates** | Date de début et de fin (optionnelles) |
| **Priorité** | Basse, Normale, Haute |

### 💬 Gestion des commentaires

- Ajouter des commentaires à chaque tâche
- Affichage chronologique avec horodatage
- Suppression individuelle
- Format : `[JJ/MM/AAAA HH:MM] Texte du commentaire`

### 🔎 Filtrage et tri

**3 onglets intelligents :**

- **Aujourd'hui** : Tâches dont l'échéance est aujourd'hui
- **Cette semaine** : Échéance dans les 7 prochains jours
- **Ce mois** : Échéance dans les 30 prochains jours

### 💾 Persistance automatique

- Toutes les modifications sont **immédiatement sauvegardées**
- Base de données SQLite stockée dans `data/app.db`
- Initialisation automatique au premier lancement

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

- Langage pédagogique, lisible
- Riche écosystème pour les GUI
- Excellent pour le prototypage rapide

#### ✅ **PySide6 (Qt6)**

- Framework GUI professionnel et multiplateforme
- Plus moderne que Tkinter
- Documentation exhaustive
- Stylisation avancée (QSS)
- **Code pur Python** (pas de Qt Designer)

#### ✅ **SQLite**

- Base de données locale, sans serveur
- Intégrée à Python (`sqlite3`)
- Parfaite pour une application desktop
- Plus robuste que JSON/CSV
- Support des transactions et des relations

**Comparaison SQLite vs JSON :**

| Critère | SQLite | JSON |
|---------|--------|------|
| Relations 1-N | ✅ Natif | ❌ Complexe |
| Requêtes | ✅ SQL puissant | ❌ Parcours manuel |
| Intégrité | ✅ Contraintes | ❌ Validation manuelle |
| Performance | ✅ Optimisé | ❌ Chargement complet |
| Transactions | ✅ ACID | ❌ Risque de corruption |

---

## 🚀 Installation et configuration

### Prérequis

- **Python 3.11** ou supérieur
- **Git** (avec Git LFS configuré)
- **pip** pour installer les dépendances

### Étapes d'installation

#### 1️⃣ Cloner le projet

```bash
# Cloner avec Git LFS (important pour le fichier .db)
git lfs install
git clone https://github.com/Yahlex/pytask.git
cd pytask
```

#### 2️⃣ Créer un environnement virtuel

**Windows :**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

#### 3️⃣ Installer les dépendances 

pip install -r requirements.txt

Contenu de requirements.txt :

PySide6>=6.6.0

#### 4️⃣ Lancer l'application
python main.py

Sortie attendue :
🚀 Démarrage de l'application...
✅ Tables créées/vérifiées
✅ Base de données initialisée
✅ Repository créé
✅ Contrôleurs créés
✅ Interface graphique lancée

==================================================
🎨 APPLICATION PRÊTE EN MODE SOMBRE !
==================================================

## 📂 Structure du code
pytask/
│
├── main.py                      # Point d'entrée
│
├── data/
│   └── app.db                   # Base SQLite (Git LFS)
│
├── models/
│   ├── task.py                  # Classe Task
│   ├── comment.py               # Classe Comment
│   └── repository.py            # CRUD + SQLite
│
├── views/
│   ├── main_window.py           # Fenêtre principale
│   ├── task_form_view.py        # Formulaire de tâche
│   └── comment_view.py          # Gestion des commentaires
│
├── controllers/
│   ├── task_controller.py       # Logique métier tâches
│   └── comment_controller.py    # Logique métier commentaires
│
├── requirements.txt             # Dépendances Python
└── README.md                    # Documentation

## 🔑 Rôle des fichiers clés

### main.py :

Initialise la base

Crée le repository

Instancie les contrôleurs

Lance l’interface PySide6

repository = Repository()
task_controller = TaskController(repository)
app = QApplication(sys.argv)
window = MainWindow(task_controller, comment_controller)
window.show()

### models/repository.py

Toutes les opérations SQLite

CRUD complet

Jointures & filtres datés

### controllers/

Validation des données

Règles métier

Zéro dépendance UI

### views/

Interfaces graphiques PySide6

Signaux → contrôleurs

Aucun accès direct à SQLite

## 🧠 Choix techniques & Justifications

# Architecture MVC stricte

✔ Vues → pas de logique métier
✔ Contrôleurs → pas d'UI
✔ Models → indépendants et testables
✔ Code maintenable, propre et pédagogique

Gestion des dates

Format interface → JJ/MM/AAAA
Format BDD SQLite → YYYY-MM-DD

# Vers SQLite
date_iso = datetime.strptime("15/01/2025", "%d/%m/%Y").date().isoformat()

# Vers interface
date_fr = datetime.fromisoformat("2025-01-15").strftime("%d/%m/%Y")

Gestion des erreurs (3 niveaux)
1️⃣ Validation contrôleur
if not title.strip():
    raise ValueError("Le titre est obligatoire")

2️⃣ Gestion UI
try:
    self.task_controller.create_task(...)
except ValueError as e:
    QMessageBox.warning(self, "Erreur", str(e))

3️⃣ Logging simple
❌ Erreur : Le titre est obligatoire

🔗 Relation 1-N : Task ↔ Comments
CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE
);


👉 ON DELETE CASCADE : si une tâche est supprimée → tous ses commentaires aussi.

🐛 Difficultés rencontrées
1️⃣ Git LFS

Problème : base SQLite > 50 Mo
Solution :

git lfs install
git lfs track "*.db"
git add .gitattributes data/app.db

2️⃣ Certificat SSL auto-signé

Solution temporaire :

git config http.sslVerify false


Solution recommandée :
→ Passage en SSH avec GitHub

3️⃣ Rafraîchissement Qt (signaux)
# TaskFormView
self.task_saved = Signal()

# MainWindow
form.task_saved.connect(self.refresh_tasks)

4️⃣ Mode sombre QSS

Palette cohérente

Contrastes adaptés

Stylesheet global appliqué sur QApplication

🚀 Améliorations futures
🔥 Priorité haute (v2.0)

Notifications (échéances)

Recherche

Export PDF / CSV

⭐ Priorité moyenne (v2.5)

Tags / catégories

Statistiques graphiques

Thèmes personnalisables

🌐 Priorité basse (v3.0)

Synchronisation cloud

Rappels récurrents

Sous-tâches + drag & drop

📚 Ressources

PySide6 Documentation

SQLite Documentation

PEP 8

Git LFS Documentation

📜 Licence

MIT License (c) 2025 – Alexis R.

👤 Auteur

Alexis R.
Étudiant en développement logiciel

