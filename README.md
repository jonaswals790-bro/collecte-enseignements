# 📚 Système d'Évaluation de la Conduite des Exercices Pratiques (Histoire-Géo & EC)
### *Unité d'Enseignement : INF 232 — Système de Gestion et Collecte de Données*

---

## 📝 Présentation du Projet
Ce projet consiste en une application web moderne et intuitive développée avec **Streamlit** et **Python**. Elle a été conçue pour automatiser la collecte, la gestion (CRUD) et l'analyse statistique rigoureuse des données empiriques liées à l'évaluation des dysfonctionnements dans la conduite des exercices pratiques en Histoire, Géographie et Éducation à la Citoyenneté dans l'Arrondissement de **Ngaoundéré 1er**.

L'application sépare strictement la gestion opérationnelle des données (Panneau de contrôle latéral gauche) et l'exploitation analytique et visuelle (Zone centrale d'affichage).

---

## ✨ Fonctionnalités Majeures & Optimisations de l'Interface

### 1. 🎛️ Panneau de Contrôle Latéral Gauche (Cadre Opérationnel)
* **Alignement Vertical Élégant :** Regroupe toutes les options de manipulation de la base de données à gauche de l'écran (`st.sidebar`).
* **Sélecteur d'Action CRUD :** Permet de basculer instantanément entre l'ajout d'une nouvelle entrée, la modification ou la suppression.
* **Extraction Directe :** Bouton de téléchargement instantané du fichier CSV brut, accessible à tout moment par les examinateurs.

### 2. ⚡ Mise à Jour Dynamique et Réactivité
* **Synchronisation Instantanée :** Intégration de mécanismes de rafraîchissement automatique (`st.rerun()`) après chaque soumission de formulaire (Ajout, Modification, Suppression).
* **Affichage Sans Délai :** Les tableaux statistiques, le tableau croisé dynamique et le visualisateur de données se mettent à jour immédiatement sans nécessiter un rechargement manuel de la page.

### 3. 📝 Formulaire de Collecte Académique (Create)
* Formulaire structuré en 4 sections réglementaires (Informations personnelles, Pratiques pédagogiques, Dysfonctionnements, Évaluations & Propositions).
* Horodatage automatique précis à la seconde pour chaque enregistrement.

### 4. 📊 Analyses Automatiques & Graphiques (Read)
* **Visualisation Graphique :** Diagrammes en barres horizontales pour les 14 tableaux statistiques réglementaires.
* **Tableau de Synthèse Croisé :** Évaluation croisée dynamique (`pd.crosstab`) du taux de disponibilité du matériel didactique selon le statut de l'établissement (Public, Privé, Confessionnel).

---

## 🚀 Directives de Déploiement

### 1. Exécution en local (Ubuntu Linux)
```bash
cd ~/Projets/CollecteEnseignement
streamlit run app.py
