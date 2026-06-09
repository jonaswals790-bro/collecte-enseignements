import streamlit as st
import pandas as pd
import os
from datetime import datetime

# Configuration de la page pour un rendu professionnel et large
st.set_page_config(
    page_title="Analyse Académique - Histoire-Géo & EC",
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
    
    action = st.radio(
        "Sélectionnez une action opérationnelle :",
        ["➕ Ajouter une personne", "✏️ Modifier une entrée", "❌ Supprimer une entrée"],
        index=0
    )
    
    st.markdown("---")
    st.subheader("📥 Extraction")
    if not df_global.empty:
        csv_data = df_global.to_csv(index=False, encoding="utf-8")
        st.download_button(
            label="📊 Télécharger le CSV complet",
            data=csv_data,
            file_name=f"Rapport_Enquete_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    else:
        st.caption("Aucune donnée à télécharger pour le moment.")

# =============================================================================
# ZONE CENTRALE DE L'APPLICATION
# =============================================================================

# --- EN-TÊTE DU QUESTIONNAIRE ACADÉMIQUE (SANS INF 232) ---
st.markdown(
    """
    <div style="background-color:#1E1E2F; padding:20px; border-radius:10px; border-left:8px solid #FF4B4B; margin-bottom:25px;">
        <h2 style="color:white; margin-top:0px; margin-bottom:10px; font-size: 24px; line-height: 1.3;">
            QUESTIONNAIRE DÉTAILLÉ DESTINÉ AUX ENSEIGNANTS ET AUX APPRENANTS SUR LE THÈME :<br>
            <span style="color:#FF4B4B;">« ÉVALUATION DES DYSFONCTIONNEMENTS DE LA CONDUITE DES EXERCICES PRATIQUES EN HISTOIRE-GÉOGRAPHIE ET ÉDUCATION À LA CITOYENNETÉ : CAS DE L'ARRONDISSEMENT DE NGAOUNDÉRÉ 1<sup>ER</sup> »</span>
        </h2>
        <p style="color:#D1D1E0; font-style: italic; margin-bottom:0; font-size: 14px;">
            <b>Introduction :</b> Ce questionnaire s'inscrit dans le cadre d'une étude sur l'évaluation des dysfonctionnements de la conduite des exercices pratiques en Histoire-Géographie et Éducation à la Citoyenneté dans l'arrondissement de Ngaoundéré 1er. L'objectif est de comprendre les difficultés rencontrées, les méthodes utilisées, les ressources disponibles, et les pistes d'amélioration possibles. Les réponses resteront strictement confidentielles et ne serviront qu'à des fins scientifiques. Merci pour votre disponibilité et votre sincerity.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

tab_form, tab_dash = st.tabs(["📝 Formulaire & Opérations", "📊 Rapport d'Analyse & Critique Scientifique"])

# =============================================================================
# ONGLET 1 : TRAITEMENT DE L'ACTION SÉLECTIONNÉE
# =============================================================================
with tab_form:
    if action == "➕ Ajouter une personne":
        st.info("**Mode Ajout :** Remplissez le formulaire académique ci-dessous pour insérer un nouvel enseignant dans le registre.")
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
                st.error("⚠️ Le nom de l'établissement est requis.")
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
                    "Participation orale": 1 if eval_orale else 0, "Amelioration_Citoyennete":  amelioration_apprentissage,
                    "Explication_Amelioration": explication_apprentissage, "Propositions_Solutions": solutions_propositions
                }
                df_nouvelle = pd.DataFrame([nouvelle_reponse])
                if not os.path.isfile(DATA_FILE):
                    df_nouvelle.to_csv(DATA_FILE, index=False, encoding="utf-8")
                else:
                    df_nouvelle.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding="utf-8")
                st.success("🎉 Enregistrement effectué avec succès !")
                st.rerun()

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
                st.success("🔄 Entrée mise à jour !")
                st.rerun()
        else:
            st.warning("Aucune donnée disponible à modifier.")

    elif action == "❌ Supprimer une entrée":
        st.subheader("🗑️ Zone de Suppression")
        if not df_global.empty:
            options_sup = df_global.apply(lambda r: f"{r['Etablissement']} ({r['Horodatage']})", axis=1).tolist()
            selected_del = st.selectbox("Sélectionner l'élément à détruire :", options_sup)
            
            st.error("⚠️ Cette action supprimera définitivement la ligne du fichier CSV.")
            if st.button("🔥 Confirmer la suppression"):
Une fois sur ton applicatio                idx_del = options_sup.index(selected_del)
                df_global = df_global.drop(df_global.index[idx_del])
                df_global.to_csv(DATA_FILE, index=False, encoding="utf-8")
                st.success("🗑️ L'entrée a été effacée.")
                st.rerun()
        else:
            st.warning("Aucune donnée à supprimer.")

# =============================================================================
# ONGLET 2 : RAPPORT D'ANALYSE APPROFONDI ET CRITIQUE (POUR STAGE)
# =============================================================================
with tab_dash:
    st.header("🔬 Rapport de Diagnostic Sociopédagogique et Statistique")
    st.write("Ce module génère des analyses critiques automatiques prêtes à être intégrées dans votre rapport de stage.")
    
    if not df_global.empty:
        statut_selection = st.selectbox("🗂️ Isoler un secteur d'analyse (Filtre Académique) :", ["Tous", "Public", "Privé", "Confessionnel"])
        df = df_global if statut_selection == "Tous" else df_global[df_global["Statut_Etablissement"] == statut_selection]
        total_reponses = len(df)
        
        # Section KPI d'introduction
        c_kpi1, c_kpi2, c_kpi3 = st.columns(3)
        with c_kpi1:
            st.metric("Taille de l'Échantillon ($N$)", f"{total_reponses} Enseignant(s)")
        with c_kpi2:
            Tx_suffisance = (df["Materiel_Suffisant"].value_counts(normalize=True).get("Oui", 0) * 100) if total_reponses > 0 else 0
            st.metric("Taux de Suffisance Matérielle", f"{Tx_suffisance:.1f} %", delta=f"{Tx_suffisance-50:.1f}% vs Seuil critique")
        with c_kpi3:
            Tx_formation = (df["Formation_Specifique"].value_counts(normalize=True).get("Oui", 0) * 100) if total_reponses > 0 else 0
            st.metric("Taux d'Enseignants Formés Pratiquement", f"{Tx_formation:.1f} %")
            
        st.markdown("---")

        if total_reponses > 0:
            def generer_tableau_critique(titre, colonne, options_ordonnees, interpretation_contextuelle):
                st.markdown(f"### 📊 {titre}")
                counts = df[colonne].value_counts()
                for opt in options_ordonnees:
                    if opt not in counts: counts[opt] = 0
                counts = counts.reindex(options_ordonnees, fill_value=0)
                
                df_tab = pd.DataFrame({"Effectifs": counts.values, "Pourcentage": [(v / total_reponses * 100) for v in counts.values]}, index=counts.index)
                
                majoritaire = counts.idxmax()
                pct_majoritaire = (counts.max() / total_reponses) * 100
                
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.dataframe(df_tab.style.format({"Pourcentage": "{:.1f} %"}), use_container_width=True)
                with c2:
                    st.bar_chart(df_tab["Pourcentage"], horizontal=True)
                
                with st.expander("🔍 Interprétation Scientifique et Critique (Idéal pour le rapport)", expanded=True):
                    st.markdown(f"""
                    **Constat statistique :** Les données empiriques révèlent une dominance de la modalité **"{majoritaire}"**, représentant **{pct_majoritaire:.1f}%** de la sous-population analysée.
                    
                    **Analyse critique :** {interpretation_contextuelle(majoritaire, pct_majoritaire)}
                    """)
                st.markdown("")

            def generer_choix_multiples_critique(titre, list_colonnes, type_analyse):
                st.markdown(f"### ⚠️ {titre}")
                effectifs = [df[col].sum() if col in df.columns else 0 for col in list_colonnes]
                pourcentages = [(eff / total_reponses * 100) if total_reponses > 0 else 0 for eff in effectifs]
                df_tab = pd.DataFrame({"Effectifs": effectifs, "Pourcentage": pourcentages}, index=list_colonnes).sort_values(by="Effectifs", ascending=False)
                
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.dataframe(df_tab.style.format({"Pourcentage": "{:.1f} %"}), use_container_width=True)
                with c2:
                    st.bar_chart(df_tab["Pourcentage"], horizontal=True)
                
                top_obstacle = df_tab.index[0]
                top_pct = df_tab.iloc[0]["Pourcentage"]
                
                with st.expander("🚨 Diagnostic des Vulnérabilités Institutionnelles", expanded=True):
                    if type_analyse == "obstacles":
                        st.markdown(f"""
                        **Facteur d'achoppement prédominant :** Le principal goulet d'étranglement identifié par l'échantillon est **"{top_obstacle}"** avec un taux d'impact critique de **{top_pct:.1f}%**.
                        
                        **Interprétation pour le stage :** Ce résultat met en évidence une crise structurelle. Lorsque les variables matérielles ou de surpeuplement des classes étouffent l'approche par compétences (APC), l'évaluation sommative se limite à de la récitation théorique, vidant l'Éducation à la Citoyenneté de sa substance pragmatique.
                        """)
                    else:
                        st.markdown(f"""
                        **Priorité méthodologique :** La méthode d'évaluation la plus exploitée est **"{top_obstacle}"** ({top_pct:.1f}%).
                        
                        **Interprétation pour le stage :** L'hégémonie de ce mode d'évaluation indique que la notation reste classique. Un équilibre avec les travaux de groupe et les observations en situation réelle est indispensable pour valider de réelles compétences citoyennes.
                        """)
                st.markdown("<br>", unsafe_allow_html=True)

            # --- CORPS DU RAPPORT DIRECTEMENT EXPLOITABLE ---
            
            # 1. Profil des répondants
            st.subheader("1. Analyse du Profil Socio-Professionnel des Enseignants")
            generer_tableau_critique(
                "Profil d'Ancienneté des répondants", 
                "Anciennete", 
                ["Moins de 5 ans", "6 à 10 ans", "11 à 15 ans", "Plus de 15 ans"],
                lambda maj, pct: f"La forte proportion d'enseignants ayant une ancienneté de ({maj} : {pct:.1f}%) implique un corps enseignant qui possède des habitudes pédagogiques bien ancrées. S'ils n'ont pas reçu de recyclage récent sur les outils numériques ou cartographiques, le risque d'ankylose méthodologique est élevé."
            )
            
            # 2. Pratiques réelles
            st.subheader("2. Évaluation Critique des Pratiques Pédagogiques")
            generer_tableau_critique(
                "Fréquence d'intégration des exercices pratiques", 
                "Frequence_Exercices", 
                ["À chaque leçon", "Souvent", "Parfois", "Rarement", "Jamais"],
                lambda maj, pct: f"L'évaluation de la fréquence montre que la modalité majoritaire est '{maj}' ({pct:.1f}%). Si cette fréquence est faible ('Rarement'/'Jamais'), cela prouve que les exercices pratiques sont considérés comme des activités secondaires ou optionnelles, souvent sacrifiées pour boucler les programmes théoriques volumineux exigés par les inspections d'Histoire-Géographie."
            )

            # 3. Obstacles et Crise structurelle
            st.subheader("3. Analyse des Dysfonctionnements Système")
            generer_choix_multiples_critique("Hiérarchisation des obstacles à l'apprentissage", ["Effectif pléthorique", "Insuffisance de matériel", "Manque de temps dans l’emploi du temps", "Manque de formation pratique", "Motivation faible des élèves"], "obstacles")

            # 4. Évaluations
            st.subheader("4. Typologie des Systèmes d'Évaluation Appliqués")
            generer_choix_multiples_critique("Modes d'évaluations appliqués sur le terrain", ["Notes individuelles", "Travaux de groupes", "Observation en classe", "Participation orale"], "evaluations")

            # =============================================================================
            # SYNTHÈSE ET CROISÉ COMPORTEMENTAL (LE COEUR DU RAPPORT DE STAGE)
            # =============================================================================
            st.header("🏁 Analyse Croisée Comparative Avancée")
            st.markdown("### Tableau Croisé : Dotation Matérielle selon le Statut de l'Établissement")
            
            if "Statut_Etablissement" in df_global.columns and "Materiel_Suffisant" in df_global.columns:
                ct_synthese = pd.crosstab(df_global["Statut_Etablissement"], df_global["Materiel_Suffisant"], normalize='index') * 100
                st.dataframe(ct_synthese.style.format("{:.1f} %"), use_container_width=True)
                
                st.markdown("#### 🔍 Lecture et Analyse Critique de la Corrélation :")
                st.info("""
                **Interprétation de la fracture sectorielle :**
                * **Secteur Public :** Généralement marqué par des effectifs massifs, les infrastructures y peinent à suivre, créant une insuffisance chronique de cartes murales et de manuels.
                * **Secteur Privé / Confessionnel :** Bénéficiant d'un mode de gouvernance plus flexible, ces structures affichent souvent des taux de satisfaction matérielle supérieurs, se traduisant par une mise en œuvre plus fréquente des travaux dirigés et simulations citoyennes.
                """)
            
            # RECOMMANDATIONS OPÉRATIONNELLES DE STAGE
            st.markdown("### 💡 Propositions de Résolution et Recommandations (Section Stage)")
            st.success("""
            Au terme de cette étude empirique menée dans l'Arrondissement de **Ngaoundéré 1er**, trois axes stratégiques se dégagent pour rehausser le niveau de conduite des exercices pratiques :
            1. **Réaménagement Horaire :** Sanctuariser une plage horaire hebdomadaire de deux heures exclusivement dédiée aux manipulations pratiques (Cartographie, Travaux de groupes).
            2. **Mutualisation Institutionnelle :** Créer une banque de ressources numériques (Cartes vectorielles, guides d'exercices d'Histoire) partagée entre les établissements publics et privés de la place.
            3. **Renforcement des Capacités Locales :** Mettre en place des séminaires d'animation pédagogique au sein des bassins d'apprentissage afin d'initier les jeunes enseignants aux méthodes actives (jeux de rôles citoyennes).
            """)
            
        else:
            st.warning("⚠️ Aucune donnée disponible pour ce filtre.")
    else:
        st.info("💡 En attente des premières réponses pour projeter le rapport d'analyse automatique.")
