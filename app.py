import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuration de la page
st.set_page_config(
    page_title="Collecte & Analyse - Histoire-Géo & EC",
    page_icon="📚",
    layout="wide"  # Mode large pour mieux afficher les graphiques d'analyse
)

# Initialisation du fichier de stockage CSV
DATA_FILE = "reponses_questionnaire.csv"

# Titre principal tiré du document
st.title("📋 Système d'Évaluation de la conduite des exercices pratiques")
st.subheader("Histoire-Géographie et Éducation à la Citoyenneté (Arrondissement de Ngaoundéré 1er)")

# Création des onglets sur l'interface
tab_formulaire, tab_analyse = st.tabs(["📝 Formulaire de Collecte", "📊 Tableau de Bord & Analyse Comparative"])

# =============================================================================
# ONGLET 1 : FORMULAIRE DE COLLECTE
# =============================================================================
with tab_formulaire:
    st.info(
        "**Introduction :** Ce questionnaire s'inscrit dans le cadre d'une étude sur l'évaluation "
        "des dysfonctionnements de la conduite des exercices pratiques. Les réponses resteront "
        "strictement confidentielles et ne serviront qu'à des fins scientifiques."
    )

    # --- FORMULAIRE ---
    with st.form("form_evaluation"):
        
        # SECTION I
        st.header("I. Informations Personnelles et Professionnelles")
        sexe = st.radio("1. Sexe :", ["Masculin", "Féminin"], horizontal=True)
        age = st.radio("2. Âge :", ["Moins de 30 ans", "30-40 ans", "41-50 ans", "Plus de 50 ans"], horizontal=True)
        
        diplome = st.selectbox("3. Diplôme le plus élevé obtenu :", ["DIPES I", "DIPES II", "Licence", "Master", "Autre"])
        diplome_autre = ""
        if diplome == "Autre":
            diplome_autre = st.text_input("Précisez votre diplôme :")
            
        anciennete = st.radio("4. Ancienneté dans l'enseignement :", ["Moins de 5 ans", "6-10 ans", "11-15 ans", "Plus de 15 ans"], horizontal=True)
        nom_etab = st.text_input("5. Nom de l'établissement :")
        statut_etab = st.radio("Statut de l'établissement :", ["Public", "Privé", "Confessionnel"], horizontal=True)
        
        st.markdown("---")
        
        # SECTION II
        st.header("II. Pratiques Pédagogiques")
        frequence = st.select_slider(
            "6. À quelle fréquence intégrez-vous des exercices pratiques dans vos cours ?",
            options=["Jamais", "Rarement", "Parfois", "Souvent", "A chaque leçon"]
        )
        
        st.write("7. Quels types d'exercices pratiques organisez-vous le plus souvent ? (Plusieurs choix possibles)")
        type_doc = st.checkbox("Analyse de documents historiques ou géographiques")
        type_carte = st.checkbox("Lecture et interprétation de cartes")
        type_groupe = st.checkbox("Travaux de groupe", key="sec2_travaux_groupe")
        type_terrain = st.checkbox("Sorties pédagogiques / visites de terrain")
        type_jeux = st.checkbox("Jeux de rôles ou simulations citoyennes")
        type_autre_check = st.checkbox("Autre type d'exercice")
        type_autre_txt = ""
        if type_autre_check:
            type_autre_txt = st.text_input("Précisez l'autre type d'exercice :")

        mat_didactique = st.radio("8. Disposez-vous du matériel didactique nécessaire (cartes, manuels, atlas, affiches, etc.) ?", ["Oui", "Non"], horizontal=True)
        manques_mat = ""
        if mat_didactique == "Non":
            manques_mat = st.text_area("Si non, précisez les manques :")
            
        formation_specifique = st.radio("9. Avez-vous reçu une formation spécifique sur la conception et la conduite des exercices pratiques ?", ["Oui", "Non"], horizontal=True)
        formation_details = ""
        if formation_specifique == "Oui":
            formation_details = st.text_input("Si oui, où et quand ?")
            
        temps_accorde = st.radio("10. Combien de temps accordez-vous en moyenne aux exercices pratiques par séquence ou par leçon ?", ["Moins de 15 min", "15-30 min", "30-60 min", "Plus d'une heure"], horizontal=True)
        
        st.markdown("---")
        
        # SECTION III
        st.header("III. Dysfonctionnements et Obstacles Rencontrés")
        st.write("1. Quels sont selon vous les principaux obstacles à la bonne conduite des exercices pratiques ? (Plusieurs choix)")
        obs_effectifs = st.checkbox("Effectifs pléthoriques (trop d'élèves par classe)")
        obs_materiel = st.checkbox("Insuffisance de matériel")
        obs_temps = st.checkbox("Manque de temps dans l'emploi du temps")
        obs_formation = st.checkbox("Manque de formation pratique")
        obs_motivation = st.checkbox("Motivation faible des élèves")
        obs_admin = st.checkbox("Manque de soutien de l'administration")
        obs_autres_check = st.checkbox("Autres obstacles")
        
        exemple_concret = st.text_area("2. Donnez un exemple concret d'un exercice pratique qui n'a pas bien fonctionné et expliquez pourquoi.")
        conditions_etab = st.radio("3. Les conditions matérielles et pédagogiques de votre établissement favorisent-elles la mise en œuvre des exercices pratiques ?", ["Oui", "Non", "Partiellement"], horizontal=True)
        justification_cond = st.text_area("Justifiez votre réponse :")
        
        st.markdown("---")
        
        # SECTION IV
        st.header("IV. Évaluation, Suivi et Propositions")
        st.write("1. Comment évaluez-vous les travaux pratiques réalisés par les élèves ? (Plusieurs choix)")
        eval_notes = st.checkbox("Notes individuelles")
        eval_groupes = st.checkbox("Travaux de groupe", key="sec4_travaux_groupe")
        eval_obs = st.checkbox("Observation en classe")
        eval_orale = st.checkbox("Participation orale")
        eval_autre = st.text_input("Autres modes d'évaluation :")
        
        amelioration_apprentissage = st.radio("2. Selon vous, les exercices pratiques améliorent-ils les apprentissages et les comportements citoyens des élèves ?", ["Oui, beaucoup", "Oui, un peu", "Non vraiment", "Pas du tout"], horizontal=True)
        explication_apprentissage = st.text_area("Expliquez :")
        solutions_propositions = st.text_area("3. Quelles solutions ou propositions formuleriez-vous pour améliorer la conduite des exercices pratiques ?")
        
        submit_button = st.form_submit_button(label="💾 Enregistrer mes réponses")

    # --- ENREGISTREMENT DES DONNÉES ---
    if submit_button:
        if not nom_etab:
            st.error("⚠️ Veuillez renseigner le nom de votre établissement avant de valider.")
        else:
            nouvelle_reponse = {
                "Horodatage": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Sexe": sexe,
                "Age": age,
                "Diplome": diplome if diplome != "Autre" else diplome_autre,
                "Anciennete": anciennete,
                "Etablissement": nom_etab,
                "Statut_Etablissement": statut_etab,
                "Frequence_Exercices": frequence,
                "Types_Exercices": ", ".join([k for k, v in {
                    "Analyse Doc": type_doc, "Cartes": type_carte, "Groupes": type_groupe, 
                    "Terrain": type_terrain, "Simulation": type_jeux, type_autre_txt: type_autre_check
                }.items() if v]),
                "Materiel_Suffisant": mat_didactique,
                "Manques_Materiel": manques_mat,
                "Formation_Specifique": formation_specifique,
                "Formation_Details": formation_details,
                "Temps_Accorde": temps_accorde,
                "Obstacles": ", ".join([k for k, v in {
                    "Effectifs pléthoriques": obs_effectifs, "Insuffisance matériel": obs_materiel,
                    "Manque temps": obs_temps, "Manque formation": obs_formation,
                    "Faible motivation": obs_motivation, "Soutien admin manquant": obs_admin,
                    "Autres": obs_autres_check
                }.items() if v]),
                "Exemple_Echec": exemple_concret,
                "Conditions_Etab_Favorables": conditions_etab,
                "Justification_Conditions": justification_cond,
                "Modes_Evaluation": ", ".join([k for k, v in {
                    "Notes individuelles": eval_notes, "Travaux de groupe": eval_groupes,
                    "Observation": eval_obs, "Orale": eval_orale
                }.items() if v]) + (f", {eval_autre}" if eval_autre else ""),
                "Amelioration_Citoyennete": amelioration_apprentissage,
                "Explication_Amelioration": explication_apprentissage,
                "Propositions_Solutions": solutions_propositions
            }
            
            df_nouvelle = pd.DataFrame([nouvelle_reponse])
            if not os.path.isfile(DATA_FILE):
                df_nouvelle.to_csv(DATA_FILE, index=False, encoding="utf-8")
            else:
                df_nouvelle.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding="utf-8")
                
            st.success("🎉 Réponses enregistrées localement avec succès ! Allez sur l'onglet Analyse pour voir la mise à jour.")

# =============================================================================
# ONGLET 2 : TABLEAU DE BORD STATISTIQUE & COMPARAISON
# =============================================================================
with tab_analyse:
    st.header("📊 Analyse Comparative en Temps Réel")
    
    if os.path.isfile(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        total_reponses = len(df)
        
        # Indicateurs rapides (KPIs)
        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Total des fiches collectées", f"{total_reponses}")
        
        nb_public = len(df[df["Statut_Etablissement"] == "Public"])
        nb_prive = len(df[df["Statut_Etablissement"].isin(["Privé", "Confessionnel"])])
        
        kpi2.metric("Établissements Publics", f"{nb_public} ({(nb_public/total_reponses*100):.1f}%)" if total_reponses > 0 else "0")
        kpi3.metric("Établissements Privés / Conf.", f"{nb_prive} ({(nb_prive/total_reponses*100):.1f}%)" if total_reponses > 0 else "0")
        
        st.markdown("---")
        
        # Séparation de l'analyse comparative
        st.subheader("🔄 Comparaison : Disponibilité du Matériel Didactique (%)")
        
        # Calcul des pourcentages croisés
        ct_materiel = pd.crosstab(df["Statut_Etablissement"], df["Materiel_Suffisant"], normalize='index') * 100
        st.bar_chart(ct_materiel)
        
        # Affichage des données chiffrées sous le graphique
        st.dataframe(ct_materiel.style.format("{:.1f} %"))
        
        st.markdown("---")
        
        # Analyse des conditions favorables
        st.subheader("🏫 Les conditions favorisent-elles la mise en œuvre ?")
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Répartition globale en Pourcentage (%)**")
            dispo_pct = df["Conditions_Etab_Favorables"].value_counts(normalize=True) * 100
            st.dataframe(dispo_pct.to_frame(name="Pourcentage (%)").style.format("{:.1f} %"))
        
        with col2:
            st.write("**Analyse croisée Statut de l'établissement vs Conditions**")
            ct_conditions = pd.crosstab(df["Statut_Etablissement"], df["Conditions_Etab_Favorables"], normalize='index') * 100
            st.bar_chart(ct_conditions)

        st.markdown("---")
        
        # CRITIQUES, SUGGESTIONS ET INTERPRÉTATIONS TEXTUELLES
        st.subheader("💬 Extraits des Critiques & Exemples de Dysfonctionnements")
        
        critiques_selection = df[["Statut_Etablissement", "Etablissement", "Exemple_Echec", "Justification_Conditions"]].dropna()
        for idx, row in critiques_selection.iterrows():
            with st.expander(f"🔴 {row['Etablissement']} ({row['Statut_Etablissement']})"):
                st.write(f"**Dysfonctionnement concret :** {row['Exemple_Echec']}")
                st.write(f"**Critique des conditions :** {row['Justification_Conditions']}")
                
        st.subheader("💡 Suggestions et Propositions récoltées")
        propositions_list = df[["Statut_Etablissement", "Propositions_Solutions"]].dropna()
        for idx, row in propositions_list.iterrows():
            st.markdown(f"- **[{row['Statut_Etablissement']}]** {row['Propositions_Solutions']}")

        st.markdown("---")
        
        # INTERPRÉTATION ET COMPARAISON FINALE GENERALE
        st.subheader("📝 Interprétation Globale & Synthèse Comparative")
        
        # Logique d'interprétation simple automatique basée sur les chiffres
        if nb_public > 0 and nb_prive > 0:
            pct_oui_public = ct_materiel.loc["Public", "Oui"] if "Oui" in ct_materiel.columns else 0
            # Moyenne pour le privé et confessionnel combinés ou lissés
            pct_oui_prive = ct_materiel.drop("Public")["Oui"].mean() if "Oui" in ct_materiel.columns else 0
            
            st.markdown("### 🔍 Rapport d'analyse généré :")
            if pct_oui_prive > pct_oui_public:
                st.warning(
                    f"**Interprétation :** Les données indiquent que les établissements privés disposent en moyenne de plus de ressources didactiques "
                    f"({pct_oui_prive:.1f}%) comparativement aux établissements publics ({pct_oui_public:.1f}%). "
                    "Cela met en évidence un besoin de dotation urgent dans le secteur public de l'arrondissement de Ngaoundéré 1er pour résorber ce fossé."
                )
            else:
                st.success(
                    f"**Interprétation :** Les structures d'enseignement public affichent un taux de satisfaction matériel de {pct_oui_public:.1f}% "
                    f"contre {pct_oui_prive:.1f}% pour le privé. Les dysfonctionnements semblent donc davantage liés à la gestion du temps ou aux effectifs pléthoriques."
                )
        else:
            st.info("💡 L'interprétation comparative finale s'affinera dès que vous aurez collecté des données à la fois dans le secteur Public et dans le secteur Privé.")

        # ZONE DE TÉLÉCHARGEMENT EXPORT DE SÉCURITÉ
        st.markdown("---")
        csv_data = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Télécharger la base de données brute (CSV)",
            data=csv_data,
            file_name=f"collecte_complete_ngaoundere1er_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.warning("⚠️ Aucune donnée n'a encore été enregistrée. Remplissez le formulaire dans le premier onglet pour générer les graphiques automatiquement.")
