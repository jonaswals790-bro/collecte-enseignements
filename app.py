import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuration de la page pour un rendu professionnel et large
st.set_page_config(
    page_title="Collecte & Analyse - Histoire-Géo & EC",
    page_icon="📚",
    layout="wide"
)

# Fichier de stockage CSV
DATA_FILE = "reponses_questionnaire.csv"

# --- INITIALISATION ET SÉCURISATION DU CSV ---
COLUMNS_BLOC = ["Horodatage", "Sexe", "Age", "Diplome", "Specialite", "Anciennete", "Etablissement", "Statut_Etablissement", "Frequence_Exercices", "Analyse de documents historiques ou géographiques", "Lecture et interprétation des cartes", "Travaux de groupe", "Sorties pédagogiques", "Jeux de rôle", "Materiel_Suffisant", "Manques_Materiel", "Formation_Specifique", "Formation_Details", "Temps_Accorde", "Effectif pléthorique", "Insuffisance de matériel", "Manque de temps dans l’emploi du temps", "Manque de formation pratique", "Motivation faible des élèves", "Exemple_Echec", "Conditions_Etab_Favorables", "Justification_Conditions", "Notes individuelles", "Travaux de groupes", "Observation en classe", "Participation orale", "Amelioration_Citoyennete", "Explication_Amelioration", "Propositions_Solutions"]
df_global = pd.read_csv(DATA_FILE) if (os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0) else pd.DataFrame(columns=COLUMNS_BLOC)

# =============================================================================
# 🛠️ BARRE LATÉRALE GAUCHE : CADRE INDÉPENDANT DE NAVIGATION & ACTIONS (CRUD)
# =============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluent/96/000000/database.png", width=80)
    st.title("🎛️ Panneau de Contrôle")
    st.markdown("---")
    
    # Menu de sélection d'action aligné verticalement
    action = st.radio(
        "Sélectionnez une action opérationnelle :",
        ["➕ Ajouter une personne", "✏️ Modifier une entrée", "❌ Supprimer une entrée"],
        index=0
    )
    
    st.markdown("---")
    st.subheader("📥 Extraction")
    # Option Télécharger toujours disponible à gauche dans son cadre
    if not df_global.empty:
        csv_data = df_global.to_csv(index=False, encoding="utf-8")
        st.download_button(
            label="📊 Télécharger le CSV complet",
            data=csv_data,
            file_name=f"Rapport_Enquete_INF232_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.caption("Aucune donnée à télécharger pour le moment.")

# =============================================================================
# ZONE CENTRALE DE L'APPLICATION
# =============================================================================
st.title("📋 Évaluation de la conduite des exercices pratiques")
st.subheader("Histoire-Géographie et Éducation à la Citoyenneté (Arrondissement de Ngaoundéré 1er)")

# Organisation en onglets principaux
tab_form, tab_dash = st.tabs(["📝 Formulaire & Opérations", "📊 Tableaux Statistiques & Analyses"])

# =============================================================================
# ONGLET 1 : TRAITEMENT DE L'ACTION SÉLECTIONNÉE (AJOUTER / MODIFIER / SUPPRIMER)
# =============================================================================
with tab_form:
    
    # CAS 1 : AJOUTER UNE PERSONNE
    if action == "➕ Ajouter une personne":
        st.info(
            "**Mode Ajout :** Remplissez le formulaire académique ci-dessous pour insérer un nouvel enseignant dans le registre."
        )
        with st.form("form_evaluation"):
            st.header("I. Informations Personnelles et Professionnelles")
            col1, col2 = st.columns(2)
            with col1:
                sexe = st.radio("1. Sexe :", ["Masculin", "Féminin"], horizontal=True)
                age = st.radio("2. Âge :", ["Moins de 30 ans", "30 – 40 ans", "41 – 50 ans", "Plus de 50 ans"], horizontal=True)
                diplome = st.selectbox("3. Diplôme le plus élevé obtenu :", ["DIPES I", "DIPES II", "Licence", "Master", "Autre"])
                diplome_autre = st.text_input("Précisez votre diplôme :") if diplome == "Autre" else ""
            with col2:
                specialite = st.radio("Spécialité dominante :", ["Histoire", "Géographie"], horizontal=True)
                anciennete = st.radio("4. Ancienneté dans l'enseignement :", ["Moins de 5 ans", "6 à 10 ans", "11 à 15 ans", "Plus de 15 ans"], horizontal=True)
                nom_etab = st.text_input("5. Nom de l'établissement :")
                statut_etab = st.radio("Statut de l'établissement :", ["Public", "Privé", "Confessionnel"], horizontal=True)
            
            st.markdown("---")
            st.header("II. Pratiques Pédagogiques")
            frequence = st.select_slider("6. Fréquence d'intégration :", options=["Jamais", "Rarement", "Parfois", "Souvent", "À chaque leçon"])
            
            type_doc = st.checkbox("Analyse de documents historiques ou géographiques")
            type_carte = st.checkbox("Lecture et interprétation des cartes")
            type_groupe = st.checkbox("Travaux de groupe", key="key_sec2_travaux_groupe")
            type_terrain = st.checkbox("Sorties pédagogiques / visites de terrain")
            type_jeux = st.checkbox("Jeux de rôle ou simulations citoyennes")
            
            mat_didactique = st.radio("8. Matériel didactique suffisant ?", ["Oui", "Non"], horizontal=True)
            manques_mat = st.text_area("Si non, précisez les manques :") if mat_didactique == "Non" else ""
            
            formation_specifique = st.radio("9. Formation spécifique reçue ?", ["Oui", "Non"], horizontal=True)
            formation_details = st.text_input("Si oui, où et quand ?") if formation_specifique == "Oui" else ""
            temps_accorde = st.radio("10. Temps accordé :", ["Moins de 15 min", "15 – 30 min", "30 – 60 min", "Plus d’une heure"], horizontal=True)
            
            st.markdown("---")
            st.header("III. Dysfonctionnements et Obstacles Rencontrés")
            obs_effectifs = st.checkbox("Effectif pléthorique")
            obs_materiel = st.checkbox("Insuffisance de matériel")
            obs_temps = st.checkbox("Manque de temps")
            obs_formation = st.checkbox("Manque de formation pratique")
            obs_motivation = st.checkbox("Motivation faible des élèves")
            
            exemple_concret = st.text_area("2. Exemple concret d'échec :")
            conditions_etab = st.radio("3. Conditions favorables ?", ["Oui", "Non", "Partiellement"], horizontal=True)
            justification_cond = st.text_area("Justifiez votre réponse :")
            
            st.markdown("---")
            st.header("IV. Évaluation, Suivi et Propositions")
            eval_notes = st.checkbox("Notes individuelles")
            eval_groupes = st.checkbox("Travaux de groupes", key="key_sec4_travaux_groupe")
            eval_obs = st.checkbox("Observation en classe")
            eval_orale = st.checkbox("Participation orale")
            
            amelioration_apprentissage = st.radio("2. Amélioration constatée ?", ["Oui, beaucoup", "Oui, un peu", "Non, vraiment pas", "Pas du tout"], horizontal=True)
            explication_apprentissage = st.text_area("Expliquez :")
            solutions_propositions = st.text_area("3. Vos solutions proposées :")
            
            submit_button = st.form_submit_button(label="💾 Enregistrer et Ajouter la ligne")

        if submit_button:
            if not nom_etab:
                st.error("Le nom de l'établissement est requis.")
            else:
                nouvelle_reponse = {
                    "Horodatage": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Sexe": sexe, "Age": age,
                    "Diplome": diplome if diplome != "Autre" else diplome_autre, "Specialite": specialite,
                    "Anciennete": anciennete, "Etablissement": nom_etab, "Statut_Etablissement": statut_etab,
                    "Frequence_Exercices": frequence, "Analyse de documents historiques ou géographiques": 1 if type_doc else 0,
                    "Lecture et interprétation des cartes": 1 if type_carte else 0, "Travaux de groupe": 1 if type_groupe else 0,
                    "Sorties pédagogiques": 1 if type_terrain else 0, "Jeux de rôle": 1 if type_jeux else 0,
                    "Materiel_Suffisant": mat_didactique, "Manques_Materiel": manques_mat, "Formation_Specifique": formation_specifique,
                    "Formation_Details": formation_details, "Temps_Accorde": temps_accorde, "Effectif pléthorique": 1 if obs_effectifs else 0,
                    "Insuffisance de matériel": 1 if obs_materiel else 0, "Manque de temps dans l’emploi du temps": 1 if obs_temps else 0,
                    "Manque de formation pratique": 1 if obs_formation else 0, "Motivation faible des élèves": 1 if obs_motivation else 0,
                    "Exemple_Echec": exemple_concret, "Conditions_Etab_Favorables": conditions_etab, "Justification_Conditions": justification_cond,
                    "Notes individuelles": 1 if eval_notes else 0, "Travaux de groupes": 1 if eval_groupes else 0, "Observation en classe": 1 if eval_obs else 0,
                    "Participation orale": 1 if eval_orale else 0, "Amelioration_Citoyennete": amelioration_apprentissage,
                    "Explication_Amelioration": explication_apprentissage, "Propositions_Solutions": solutions_propositions
                }
                df_nouvelle = pd.DataFrame([nouvelle_reponse])
                if not os.path.isfile(DATA_FILE):
                    df_nouvelle.to_csv(DATA_FILE, index=False, encoding="utf-8")
                else:
                    df_nouvelle.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding="utf-8")
                st.success("🎉 Enregistrement effectué avec succès !")
                st.rerun()

    # CAS 2 : MODIFIER UNE ENTRÉE
    elif action == "✏️ Modifier une entrée":
        st.subheader("📝 Modification d'un enregistrement")
        if not df_global.empty:
            options_mod = df_global.apply(lambda r: f"{r['Etablissement']} ({r['Horodatage']})", axis=1).tolist()
            selected_edit = st.selectbox("Sélectionner la ligne à mettre à jour :", options_mod)
            idx_edit = options_mod.index(selected_edit)
            row_data = df_global.iloc[idx_edit]
            
            new_etab = st.text_input("Nom de l'établissement :", value=row_data['Etablissement'])
            new_statut = st.selectbox("Statut :", ["Public", "Privé", "Confessionnel"], index=["Public", "Privé", "Confessionnel"].index(row_data['Statut_Etablissement']))
            new_sol = st.text_area("Modifier les propositions :", value=str(row_data['Propositions_Solutions']))
            
            if st.button("💾 Sauvegarder les modifications"):
                df_global.at[idx_edit, 'Etablissement'] = new_etab
                df_global.at[idx_edit, 'Statut_Etablissement'] = new_statut
                df_global.at[idx_edit, 'Propositions_Solutions'] = new_sol
                df_global.to_csv(DATA_FILE, index=False, encoding="utf-8")
                st.success(" Entrée mise à jour !")
                st.rerun()
        else:
            st.warning("Aucune donnée disponible à modifier.")

    # CAS 3 : SUPPRIMER UNE ENTRÉE
    elif action == " Supprimer une entrée":
        st.subheader("Zone de Suppression")
        if not df_global.empty:
            options_sup = df_global.apply(lambda r: f"{r['Etablissement']} ({r['Horodatage']})", axis=1).tolist()
            selected_del = st.selectbox("Sélectionner l'élément à détruire :", options_sup)
            
            st.error("Cette action supprimera définitivement la ligne du fichier CSV.")
            if st.button(" Confirmer la suppression"):
                idx_del = options_sup.index(selected_del)
                df_global = df_global.drop(df_global.index[idx_del])
                df_global.to_csv(DATA_FILE, index=False, encoding="utf-8")
                st.success(" L'entrée a été effacée.")
                st.rerun()
        else:
            st.warning("Aucune donnée à supprimer.")

# =============================================================================
# ONGLET 2 : GRAPHIQUES ET ANALYSES STATISTIQUES
# =============================================================================
with tab_dash:
    st.header(" Tableaux de Répartition et Analyse par Critères")
    if not df_global.empty:
        statut_selection = st.selectbox(" Filtrer par Statut d'Établissement :", ["Tous", "Public", "Privé", "Confessionnel"])
        df = df_global if statut_selection == "Tous" else df_global[df_global["Statut_Etablissement"] == statut_selection]
        total_reponses = len(df)
        
        st.write(f"Données basées sur un effectif de **{total_reponses}** enseignant(s).")
        
        if total_reponses > 0:
            def generer_tableau_simple(titre, colonne, options_ordonnees):
                st.subheader(titre)
                counts = df[colonne].value_counts()
                for opt in options_ordonnees:
                    if opt not in counts: counts[opt] = 0
                counts = counts.reindex(options_ordonnees, fill_value=0)
                
                df_tab = pd.DataFrame({"Effectifs": counts.values, "Pourcentage": [(v / total_reponses * 100) for v in counts.values]}, index=counts.index)
                df_total = pd.DataFrame({"Effectifs": [total_reponses], "Pourcentage": [100.0]}, index=["Total"])
                
                c1, c2 = st.columns([1, 1])
                with c1: st.dataframe(pd.concat([df_tab, df_total]).style.format({"Pourcentage": "{:.1f} %"}))
                with c2: st.bar_chart(df_tab["Pourcentage"], horizontal=True)
                st.markdown("---")

            def generer_tableau_choix_multiples(titre, list_colonnes):
                st.subheader(titre)
                effectifs = [df[col].sum() if col in df.columns else 0 for col in list_colonnes]
                pourcentages = [(eff / total_reponses * 100) if total_reponses > 0 else 0 for eff in effectifs]
                df_tab = pd.DataFrame({"Effectifs": effectifs, "Pourcentage": pourcentages}, index=list_colonnes)
                
                c1, c2 = st.columns([1, 1])
                with c1: st.dataframe(df_tab.style.format({"Pourcentage": "{:.1f} %"}))
                with c2: st.bar_chart(df_tab["Pourcentage"], horizontal=True)
                st.markdown("---")

            # Appels des tableaux réglementaires
            generer_tableau_simple("Tableau 1 : Répartition selon le sexe", "Sexe", ["Masculin", "Féminin"])
            generer_tableau_simple("Tableau 2 : Répartition selon l'âge", "Age", ["Moins de 30 ans", "30 – 40 ans", "41 – 50 ans", "Plus de 50 ans"])
            generer_tableau_simple("Tableau 3 : Répartition selon le diplôme", "Diplome", ["DIPES I", "DIPES II", "Licence", "Master"])
            generer_tableau_simple("Tableau 4 : Répartition selon la spécialité", "Specialite", ["Histoire", "Géographie"])
            generer_tableau_simple("Tableau 5 : Répartition selon l'ancienneté", "Anciennete", ["Moins de 5 ans", "6 à 10 ans", "11 à 15 ans", "Plus de 15 ans"])
            generer_tableau_simple("Tableau 6 : Fréquence d'intégration des exercices", "Frequence_Exercices", ["À chaque leçon", "Souvent", "Parfois", "Rarement", "Jamais"])
            generer_tableau_choix_multiples("Tableau 7 : Types d'exercices organisés", ["Analyse de documents historiques ou géographiques", "Lecture et interprétation des cartes", "Travaux de groupe", "Sorties pédagogiques", "Jeux de rôle"])
            generer_tableau_simple("Tableau 8 : Matériels didactiques disponibles", "Materiel_Suffisant", ["Oui", "Non"])
            generer_tableau_simple("Tableau 9 : Formation spécifique reçue", "Formation_Specifique", ["Oui", "Non"])
            generer_tableau_simple("Tableau 10 : Temps accordé aux exercices pratiques", "Temps_Accorde", ["Moins de 15 min", "15 – 30 min", "30 – 60 min", "Plus d’une heure"])
            generer_tableau_choix_multiples("Tableau 11 : Obstacles rencontrés", ["Effectif pléthorique", "Insuffisance de matériel", "Manque de temps dans l’emploi du temps", "Manque de formation pratique", "Motivation faible des élèves"])
            generer_tableau_simple("Tableau 12 : Conditions matérielles globales", "Conditions_Etab_Favorables", ["Oui", "Non", "Partiellement"])
            generer_tableau_choix_multiples("Tableau 13 : Modes d'évaluations appliqués", ["Notes individuelles", "Travaux de groupes", "Observation en classe", "Participation orale"])
            generer_tableau_simple("Tableau 14 : Amélioration des apprentissages", "Amelioration_Citoyennete", ["Oui, beaucoup", "Oui, un peu", "Non, vraiment pas", "Pas du tout"])

            # --- LE TABLEAU CROISÉ CORRIGÉ (LIGNE 303 FERMÉE) ---
            st.header(" Synthèse Comparative Finale entre Statuts")
            if "Statut_Etablissement" in df_global.columns and "Materiel_Suffisant" in df_global.columns:
                ct_synthese = pd.crosstab(df_global["Statut_Etablissement"], df_global["Materiel_Suffisant"], normalize='index') * 100
                st.dataframe(ct_synthese.style.format("{:.1f} %"))
            
            st.markdown("### Conclusion d'interprétation générale :")
            st.info("L'examen comparatif des données empiriques recueillies met en exergue des disparités significatives...")
        else:
            st.warning(" Aucune donnée disponible pour ce filtre.")
    else:
        st.info(" En attente des premières réponses pour projeter l'analyse automatique.")
