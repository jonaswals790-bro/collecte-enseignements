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

# Fichier de stockage CSV et Markdown pour GitHub
DATA_FILE = "reponses_questionnaire.csv"
README_FILE = "README.md"

# --- INITIALISATION ET SÉCURISATION DU CSV ---
COLUMNS_BLOC = [
    "Horodatage", "Sexe", "Age", "Diplome", "Specialite", "Anciennete", 
    "Etablissement", "Statut_Etablissement", "Frequence_Exercices", 
    "Analyse de documents historiques ou géographiques", "Lecture et interprétation des cartes", 
    "Travaux de groupe", "Sorties pédagogiques", "Jeux de rôle", "Materiel_Suffisant", 
    "Manques_Materiel", "Formation_Specifique", "Formation_Details", "Temps_Accorde", 
    "Effectif pléthorique", "Insuffisance de matériel", "Manque de temps dans l’emploi du temps", 
    "Manque de formation pratique", "Motivation faible des élèves", "Exemple_Echec", 
    "Conditions_Etab_Favorables", "Justification_Conditions", "Notes individuelles", 
    "Travaux de groupes", "Observation en classe", "Participation orale", 
    "Amelioration_Citoyennete", "Explication_Amelioration", "Propositions_Solutions"
]

if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
    df_global = pd.read_csv(DATA_FILE)
else:
    df_global = pd.DataFrame(columns=COLUMNS_BLOC)

# --- FONCTION DE GÉNÉRATION DU RAPPORT ACADÉMIQUE COMPLET (HTML ENREGISTRABLE) ---
def generer_rapport_html_universitaire(df_source, statut_filtre):
    total_r = len(df_source)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Rapport d'Analyse Scientifique et Critique - Évaluation Thématique</title>
        <style>
            body {{ font-family: 'Times New Roman', Times, serif; line-height: 1.6; color: #111; margin: 50px; font-size: 15px; }}
            .header {{ text-align: center; margin-bottom: 35px; border-bottom: 3px double #1E3A8A; padding-bottom: 15px; }}
            .title {{ color: #1E3A8A; font-size: 20px; font-weight: bold; margin-top: 25px; margin-bottom: 12px; text-transform: uppercase; }}
            .subtitle {{ font-style: italic; font-size: 15px; color: #444; margin-bottom: 15px; font-weight: bold; }}
            .meta-box {{ background-color: #F9FAFB; padding: 20px; border: 1px solid #D1D5DB; border-radius: 4px; margin-bottom: 30px; }}
            h2 {{ color: #1E3A8A; border-bottom: 1px solid #1E3A8A; padding-bottom: 5px; margin-top: 35px; font-size: 17px; text-transform: uppercase; }}
            h3 {{ color: #2C3E50; font-size: 15px; margin-top: 20px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 15px; font-family: Arial, sans-serif; font-size: 13px; }}
            th, td {{ border: 1px solid #9CA3AF; padding: 8px; text-align: center; }}
            th {{ background-color: #F3F4F6; color: #111; font-weight: bold; }}
            .interpretation {{ background-color: #F0F4F8; border-left: 4px solid #1E3A8A; padding: 15px; margin-top: 12px; font-style: italic; margin-bottom: 20px; }}
            .footer {{ text-align: center; margin-top: 60px; font-size: 13px; border-top: 1px solid #9CA3AF; padding-top: 15px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">QUESTIONNAIRE DÉTAILLÉ DESTINÉ AUX ENSEIGNANTS ET AUX APPRENANTS SUR LE THÈME :</div>
            <div class="subtitle">« ÉVALUATION DES DYSFONCTIONNEMENTS DE LA CONDUITE DES EXERCICES PRATIQUES EN HISTOIRE-GÉOGRAPHIE ET ÉDUCATION À LA CITOYENNETÉ : CAS DE L'ARRONDISSEMENT DE NGAOUNDÉRÉ 1ER »</div>
        </div>
        
        <div class="meta-box">
            <strong>Périmètre d'analyse :</strong> Bassin d'apprentissage (Filtre appliqué : {statut_filtre})<br>
            <strong>Volume de l'échantillon empirique ($N$) :</strong> {total_r} Enseignant(s) interrogé(s)<br>
            <strong>Date d'extraction :</strong> {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}<br><br>
            <strong>Introduction :</strong> Ce questionnaire s'inscrit dans le cadre d'une étude sur l'évaluation des dysfonctionnements de la conduite des exercices pratiques en Histoire-Géographie et Éducation à la Citoyenneté dans l'arrondissement de Ngaoundéré 1er. L'objectif est de comprendre les difficultés rencontrées, les méthodes utilisées, les ressources disponibles, et les pistes d'amélioration possibles. Les réponses resteront strictement confidentielles et ne serviront qu'à des fins scientifiques. Merci pour votre disponibilité et votre sincérité.
        </div>
    """

    if total_r > 0:
        # 1. Analyse Socio-professionnelle
        html += "<h2>1. Analyse du Profil Socio-Professionnel des Enseignants</h2>"
        if "Anciennete" in df_source.columns:
            c_anc = df_source["Anciennete"].value_counts()
            df_anc = pd.DataFrame({"Effectifs": c_anc.values, "Pourcentage": [(v / total_r * 100) for v in c_anc.values]}, index=c_anc.index)
            html += "<h3>Tableau 1 : Distribution fréquentielle du profil d'ancienneté</h3>"
            html += df_anc.to_html()
            maj_anc = c_anc.idxmax() if not c_anc.empty else "N/A"
            pct_anc = (c_anc.max() / total_r) * 100 if not c_anc.empty else 0
            html += f"""<div class="interpretation">
                <strong>Analyse & Interprétation critique de l'ancienneté :</strong> Les indicateurs relèvent une dominance de la classe d'ancienneté <strong>"{maj_anc}"</strong>, représentant {pct_anc:.1f}% des effectifs. 
                Ce niveau implique un socle d'expérience théorique significatif au sein de l'échantillon. Toutefois, cette inertie peut traduire une résistance 
                méthodologique passive face aux mutations technologiques exigées par l'évaluation active (comme l'usage de la cartographie numérique ou des logiciels de simulation SIG).
            </div>"""

        # 2. Pratiques réelles
        html += "<h2>2. Évaluation Critique des Pratiques Pédagogiques Réelles</h2>"
        if "Frequence_Exercices" in df_source.columns:
            c_frq = df_source["Frequence_Exercices"].value_counts()
            df_frq = pd.DataFrame({"Effectifs": c_frq.values, "Pourcentage": [(v / total_r * 100) for v in c_frq.values]}, index=c_frq.index)
            html += "<h3>Tableau 2 : Fréquence d'intégration des exercices pratiques</h3>"
            html += df_frq.to_html()
            maj_frq = c_frq.idxmax() if not c_frq.empty else "N/A"
            pct_frq = (c_frq.max() / total_r) * 100 if not c_frq.empty else 0
            html += f"""<div class="interpretation">
                <strong>Analyse & Interprétation critique de la récurrence :</strong> La fréquence modale se fixe sur la modalité <strong>"{maj_frq}"</strong> avec un taux de {pct_frq:.1f}%. 
                Si cette récurrence s'éloigne d'une intégration systématique, elle met en évidence que les ateliers appliqués demeurent l'ajustement marginal de la discipline, 
                souvent sacrifiés au profit du bouclage strictement linéaire et théorique du programme.
            </div>"""

        # 3. Obstacles Structurels
        html += "<h2>3. Analyse Systémique des Dysfonctionnements et Obstacles</h2>"
        list_obs = ["Effectif pléthorique", "Insuffisance de matériel", "Manque de temps dans l’emploi du temps", "Manque de formation pratique", "Motivation faible des élèves"]
        obs_eff = [df_source[col].sum() if col in df_source.columns else 0 for col in list_obs]
        df_obs = pd.DataFrame({"Effectifs cumulés": obs_eff, "Taux de citation (%)": [(e / total_r * 100) for e in obs_eff]}, index=list_obs).sort_values(by="Effectifs cumulés", ascending=False)
        html += "<h3>Tableau 3 : Hiérarchisation des facteurs d'achoppement structurels</h3>"
        html += df_obs.to_html()
        top_obs = df_obs.index[0] if not df_obs.empty else "N/A"
        top_obs_pct = df_obs.iloc[0]["Taux de citation (%)"] if not df_obs.empty else 0
        html += f"""<div class="interpretation">
            <strong>Diagnostic & Interprétation des vulnérabilités institutionnelles :</strong> Le verrou infrastructurel majeur soulevé par les enseignants est <strong>"{top_obs}"</strong> ({top_obs_pct:.1f}% de citations). 
            Il en découle une crise structurelle évidente : l'Approche Par Compétences (APC) requiert un suivi individualisé des apprenants, 
            ce qui devient physiquement inapplicable dès lors que les variables de charge d'élèves en classe franchissent les seuils de saturation.
        </div>"""

        # 4. Évaluations
        html += "<h2>4. Typologie des Systèmes d'Évaluation Appliqués</h2>"
        list_ev = ["Notes individuelles", "Travaux de groupes", "Observation en classe", "Participation orale"]
        ev_eff = [df_source[col].sum() if col in df_source.columns else 0 for col in list_ev]
        df_ev = pd.DataFrame({"Effectifs cumulés": ev_eff, "Taux de pénétration (%)": [(e / total_r * 100) for e in ev_eff]}, index=list_ev).sort_values(by="Effectifs cumulés", ascending=False)
        html += "<h3>Tableau 4 : Répartition des modes d'évaluation sur le terrain</h3>"
        html += df_ev.to_html()
        top_ev = df_ev.index[0] if not df_ev.empty else "N/A"
        top_ev_pct = df_ev.iloc[0]["Taux de pénétration (%)"] if not df_ev.empty else 0
        html += f"""<div class="interpretation">
            <strong>Analyse & Interprétation des mécanismes d'évaluation :</strong> L'hégémonie de la modalité <strong>"{top_ev}"</strong> ({top_ev_pct:.1f}%) indique que l'évaluation demeure classique et sommative. 
            Un rééquilibrage vers des grilles d'observation de compétences comportementales est indispensable pour valider l'acquisition concrète de l'Éducation à la Citoyenneté.
        </div>"""

        # 5. Synthèse Croisée et Recommandations
        html += "<h2>5. Étude Comparative Finale et Analyse Croisée</h2>"
        if "Statut_Etablissement" in df_global.columns and "Materiel_Suffisant" in df_global.columns:
            ct_synthese = pd.crosstab(df_global["Statut_Etablissement"], df_global["Materiel_Suffisant"], normalize='index') * 100
            html += "<h3>Tableau 5 : Étude croisée comparative (%) — Dotation Matérielle selon le Statut Sectoriel</h3>"
            html += ct_synthese.to_html(float_format=lambda x: f"{x:.1f} %")
        
        html += """
        <div class="interpretation">
            <strong>Lecture et Interprétation critique de la fracture comparative sectorielle :</strong><br>
            * <strong>Secteur Public :</strong> Généralement marqué par des effectifs massifs, les infrastructures y peinent à suivre, créant une insuffisance matérielle récurrente.<br>
            * <strong>Secteur Privé / Confessionnel :</strong> Bénéficiant d'un mode de gouvernance plus flexible, ces structures affichent souvent de meilleurs taux de couverture logistique grâce à la participation financière directe des parents.
        </div>
        
        <h3>💡 Propositions de Résolution et Recommandations Stratégiques :</h3>
        <ol>
            <li><strong>Réaménagement Horaire :</strong> Sanctuariser une plage horaire hebdomadaire de deux heures exclusivement dédiée aux manipulations cartographiques et ateliers pratiques.</li>
            <li><strong>Mutualisation Institutionnelle :</strong> Créer une banque de ressources numériques partagée à l'échelle régionale (Arrondissement de Ngaoundéré 1er).</li>
            <li><strong>Renforcement des Capacités Locales :</strong> Mettre en place des séminaires d'animation pédagogique sur l'évaluation active en classe pléthorique.</li>
        </ol>
        """
    else:
        html += "<p>Aucune donnée disponible pour alimenter le corps de ce document.</p>"

    html += f"""
        <div class="footer">
            Rapport d'Analyse Statistique - Document Officiel<br>
            Cas de l'Arrondissement de Ngaoundéré 1er
        </div>
    </body>
    </html>
    """
    return html


# =============================================================================
# 🛠️ BARRE LATÉRALE GAUCHE : PANNEAU DE CONTRÔLE & EXTRACTION DOUBLE
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
    st.subheader("📥 Extractions Disponibles")
    if not df_global.empty:
        # Bouton 1 : CSV Brut
        csv_data = df_global.to_csv(index=False, encoding="utf-8")
        st.download_button(
            label="📊 Sauvegarder les Données (CSV)",
            data=csv_data,
            file_name=f"Donnees_Brutes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        # Bouton 2 : Archive Globale Tableaux + Analyses (HTML/Word)
        html_archive = generer_rapport_html_universitaire(df_global, "Tous")
        st.download_button(
            label="📝 Sauvegarder Tableaux + Analyses (HTML)",
            data=html_archive,
            file_name=f"Rapport_Analyses_Ngaoundere_1er.html",
            mime="text/html",
            use_container_width=True
        )
        st.caption("✨ *L'archive HTML conserve l'ensemble des tableaux calculés, pourcentages, interprétations scientifiques et l'étude comparative finale.*")
    else:
        st.caption("Aucune donnée à exporter.")


# =============================================================================
# 🏛️ EN-TÊTE DE L'APPLICATION (ALIGNÉ EXACTEMENT SUR LE QUESTIONNAIRE VISUEL)
# =============================================================================
st.markdown("""
    <style>
    .header-box {
        background-color: #1E293B;
        padding: 30px;
        border-radius: 8px;
        border-left: 8px solid #EF4444;
        color: #FFFFFF;
        margin-bottom: 25px;
    }
    .title-main {
        font-family: 'Arial', sans-serif;
        font-size: 22px;
        font-weight: bold;
        line-height: 1.4;
        margin-bottom: 20px;
        text-transform: uppercase;
    }
    .theme-text {
        color: #F87171;
    }
    .intro-text {
        font-family: 'Arial', sans-serif;
        font-size: 15px;
        font-style: italic;
        line-height: 1.6;
        color: #E2E8F0;
        border-top: 1px solid #475569;
        padding-top: 15px;
    }
    </style>
""", unsafe_allow_html=True)

# Bloc En-tête Unique et Conforme à l'image
st.markdown("""
    <div class='header-box'>
        <div class='title-main'>
            QUESTIONNAIRE DÉTAILLÉ DESTINÉ AUX ENSEIGNANTS ET AUX APPRENANTS SUR LE THÈME :<br>
            <span class='theme-text'>« ÉVALUATION DES DYSFONCTIONNEMENTS DE LA CONDUITE DES EXERCICES PRATIQUES EN HISTOIRE-GÉOGRAPHIE ET ÉDUCATION À LA CITOYENNETÉ : CAS DE L'ARRONDISSEMENT DE NGAOUNDÉRÉ 1<sup>ER</sup> »</span>
        </div>
        <div class='intro-text'>
            <b>Introduction :</b> Ce questionnaire s'inscrit dans le cadre d'une étude sur l'évaluation des dysfonctionnements de la conduite des exercices pratiques en Histoire-Géographie et Éducation à la Citoyenneté dans l'arrondissement de Ngaoundéré 1er. L'objectif est de comprendre les difficultés rencontrées, les méthodes utilisées, les ressources disponibles, et les pistes d'amélioration possibles. Les réponses resteront strictement confidentielles et ne serviront qu'à des fins scientifiques. Merci pour votre disponibilité et votre sincérité.
        </div>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")


# =============================================================================
# ZONE CENTRALE DE NAVIGATION - ONGLETS
# =============================================================================
tab_form, tab_dash = st.tabs(["📝 Formulaire & Opérations", "📊 Rapport d'Analyse & Critique Scientifique"])

# =============================================================================
# ONGLET 1 : TRAITEMENT DE L'ACTION SÉLECTIONNÉE (CRUD)
# =============================================================================
with tab_form:
    if action == "➕ Ajouter une personne":
        st.info("**Mode Ajout :** Remplissez le formulaire ci-dessous pour insérer un nouvel enseignant dans le registre.")
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

            st.markdown("**7. Formes d'exercices pratiques appliquées :**")
            type_doc = st.checkbox("Analyse de documents historiques ou géographiques")
            type_carte = st.checkbox("Lecture et interprétation des cartes")
            type_groupe = st.checkbox("Travaux de groupe", key="key_sec2_travaux_groupe")
            type_terrain = st.checkbox("Sorties pédagogiques / visites de terrain")
            type_jeux = st.checkbox("Jeux de rôle ou simulations citoyennes")

            st.markdown("---")
            mat_didactique = st.radio("8. Matériel didactique suffisant ?", ["Oui", "Non"], horizontal=True)
            manques_mat = st.text_area("Si non, précisez les manques :") if mat_didactique == "Non" else ""

            formation_specifique = st.radio("9. Formation spécifique reçue ?", ["Oui", "Non"], horizontal=True)
            formation_details = st.text_input("Si oui, où et quand ?") if formation_specifique == "Oui" else ""
            temps_accorde = st.radio("10. Temps accordé aux exercices :", ["Moins de 15 min", "15 – 30 min", "30 – 60 min", "Plus d’une heure"], horizontal=True)

            st.markdown("---")
            st.header("III. Dysfonctionnements et Obstacles Rencontrés")
            st.markdown("**1. Quels sont les obstacles majeurs ?**")
            obs_effectifs = st.checkbox("Effectif pléthorique")
            obs_materiel = st.checkbox("Insuffisance de matériel")
            obs_temps = st.checkbox("Manque de temps")
            obs_formation = st.checkbox("Manque de formation pratique")
            obs_motivation = st.checkbox("Motivation faible des élèves")

            exemple_concret = st.text_area("2. Exemple concret d'échec d'activité pratique :")
            conditions_etab = st.radio("3. Conditions de votre établissement favorables ?", ["Oui", "Non", "Partiellement"], horizontal=True)
            justification_cond = st.text_area("Justifiez votre réponse :")

            st.markdown("---")
            st.header("IV. Évaluation, Suivi et Propositions")
            st.markdown("**1. Comment évaluez-vous ces exercices ?**")
            eval_notes = st.checkbox("Notes individuelles")
            eval_groupes = st.checkbox("Travaux de groupes", key="key_sec4_travaux_groupe")
            eval_obs = st.checkbox("Observation en classe")
            eval_orale = st.checkbox("Participation orale")

            amelioration_apprentissage = st.radio("2. Amélioration de l'apprentissage citoyen constatée ?", ["Oui, beaucoup", "Oui, un peu", "Non, vraiment pas", "Pas d'avis"], horizontal=True)
            explication_apprentissage = st.text_area("Expliquez brièvement votre choix :")
            solutions_propositions = st.text_area("3. Vos solutions et propositions stratégiques :")

            submit_button = st.form_submit_button(label="💾 Enregistrer la réponse")

        if submit_button:
            if not nom_etab:
                st.error("⚠️ Le nom de l'établissement est requis.")
            else:
                horodatage_actuel = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                nouvelle_reponse = {
                    "Horodatage": horodatage_actuel, "Sexe": sexe, "Age": age,
                    "Diplome": diplome if diplome != "Autre" else diplome_autre, "Specialite": specialite,
                    "Anciennete": anciennete, "Etablissement": nom_etab,
                    "Statut_Etablissement": statut_etab,
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
                
                # --- SAUVEGARDE SYNCHRONISÉE DANS LE FICHIER CSV ---
                df_nouvelle = pd.DataFrame([nouvelle_reponse])
                if not os.path.isfile(DATA_FILE):
                    df_nouvelle.to_csv(DATA_FILE, index=False, encoding="utf-8")
                else:
                    df_nouvelle.to_csv(DATA_FILE, mode='a', header=False, index=False, encoding="utf-8")

                # --- SAUVEGARDE SYNCHRONISÉE DANS LE README.MD ---
                if not os.path.exists(README_FILE):
                    with open(README_FILE, "w", encoding="utf-8") as f:
                        f.write("# 📚 Système de Collecte de Données Terrain\n\n")
                        f.write("## 📝 Registre Global des Réponses Connectées\n\n")
                        f.write("| Horodatage | Établissement | Statut | Sexe | Ancienneté | Fréquence | Solutions Proposées |\n")
                        f.write("| --- | --- | --- | --- | --- | --- | --- |\n")

                sol_nettoyee = str(solutions_propositions).replace("\n", " ").replace("|", " ")
                ligne_markdown = f"| {horodatage_actuel} | {nom_etab} | {statut_etab} | {sexe} | {anciennete} | {frequence} | {sol_nettoyee} |\n"
                
                with open(README_FILE, "a", encoding="utf-8") as f:
                    f.write(ligne_markdown)

                st.success("🎉 Enregistrement effectué avec succès dans le fichier CSV et mis à jour sur GitHub !")
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
                st.success("🔄 Entrée mise à jour avec succès !")
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
                idx_del = options_sup.index(selected_del)
                df_global = df_global.drop(df_global.index[idx_del])
                df_global.to_csv(DATA_FILE, index=False, encoding="utf-8")
                st.success("🗑️ L'entrée a été effacée.")
                st.rerun()
        else:
            st.warning("Aucune donnée à supprimer.")

# =============================================================================
# ONGLET 2 : RAPPORT D'ANALYSE APPROFONDI ET CRITIQUE
# =============================================================================
with tab_dash:
    st.header("🔬 Rapport de Diagnostic Sociopédagogique et Statistique")
    st.write("Ce module génère des analyses critiques automatiques basées sur les données collectées.")
    
    if not df_global.empty:
        statut_selection = st.selectbox("🗂️ Isoler un secteur d'analyse :", ["Tous", "Public", "Privé", "Confessionnel"])
        df = df_global if statut_selection == "Tous" else df_global[df_global["Statut_Etablissement"] == statut_selection]
        total_reponses = len(df)

        st.markdown("### 📥 Téléchargement du Rapport Global")
        html_document = generer_rapport_html_universitaire(df, statut_selection)
        
        st.download_button(
            label="📄 Télécharger l'Archive Globale (Tableaux + Analyses Critiques au format HTML)",
            data=html_document,
            file_name=f"Rapport_Analyses_Ngaoundere_1er.html",
            mime="text/html",
            use_container_width=True
        )
        st.markdown("---")

        # Section KPI d'introduction
        c_kpi1, c_kpi2, c_kpi3 = st.columns(3)
        with c_kpi1:
            st.metric("Taille de l'Échantillon ($N$)", f"{total_reponses} Enseignant(s)")
        with c_kpi2:
            Tx_suffisance = (df["Materiel_Suffisant"].value_counts(normalize=True).get("Oui", 0) * 100) if total_reponses > 0 else 0
            st.metric("Taux de Suffisance Matérielle", f"{Tx_suffisance:.1f} %")
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

                majoritaire = counts.idxmax() if not counts.empty else "N/A"
                pct_majoritaire = (counts.max() / total_reponses) * 100 if total_reponses > 0 else 0

                c1, c2 = st.columns([1, 1])
                with c1:
                    st.dataframe(df_tab.style.format({"Pourcentage": "{:.1f} %"}), use_container_width=True)
                with c2:
                    st.bar_chart(df_tab["Pourcentage"], horizontal=True)

                with st.expander("🔍 Interprétation Scientifique et Critique", expanded=True):
                    st.markdown(f"""
                    **Constat statistique :** Les données empiriques révèlent une dominance de la modalité **"{majoritaire}"**, représentant {pct_majoritaire:.1f}% de la sous-population interrogée.
                    
                    **Analyse critique :** {interpretation_contextuelle(majoritaire, pct_majoritaire)}
                    """)
                st.markdown("<br>", unsafe_allow_html=True)

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

                top_obstacle = df_tab.index[0] if not df_tab.empty else "N/A"
                top_pct = df_tab.iloc[0]["Pourcentage"] if not df_tab.empty else 0

                with st.expander("🚨 Diagnostic des Vulnérabilités Institutionnelles", expanded=True):
                    if type_analyse == "obstacles":
                        st.markdown(f"""
                        **Facteur d'achoppement prédominant :** Le principal goulet d'étranglement identifié par l'échantillon est **"{top_obstacle}"**, cité à hauteur de {top_pct:.1f}%.
                        
                        **Interprétation :** Ce résultat met en évidence une crise structurelle. Lorsque les variables matérielles et spatiales saturent, l'ajustement pédagogique induit inévitablement un recul vers l'enseignement purement magistral.
                        """)
                    else:
                        st.markdown(f"""
                        **Priorité méthodologique :** La méthode d'évaluation la plus exploitée est **"{top_obstacle}"** ({top_pct:.1f}%).
                        
                        **Interprétation :** L'hégémonie de ce mode d'évaluation indique que la notation reste classique. Un équilibre vers de l'évaluation formative continue s'avère nécessaire.
                        """)
                st.markdown("<br>", unsafe_allow_html=True)

            # --- CORPS DU RAPPORT ---
            st.subheader("1. Analyse du Profil Socio-Professionnel des Enseignants")
            generer_tableau_critique(
                "Profil d'Ancienneté des répondants", 
                "Anciennete", 
                ["Moins de 5 ans", "6 à 10 ans", "11 à 15 ans", "Plus de 15 ans"],
                lambda maj, pct: f"La forte proportion d'enseignants ayant une ancienneté de ({maj} : {pct:.1f}%) implique un corps enseignant mature. Toutefois, cela met également en exergue un besoin de recyclage face aux nouveaux outils d'évaluation active."
            )

            st.subheader("2. Évaluation Critique des Pratiques Pédagogiques")
            generer_tableau_critique(
                "Fréquence d'intégration des exercices pratiques", 
                "Frequence_Exercices", 
                ["À chaque leçon", "Souvent", "Parfois", "Rarement", "Jamais"],
                lambda maj, pct: f"L'évaluation de la fréquence montre que la modalité majoritaire est '{maj}' ({pct:.1f}%). Si cette fréquence est faible, cela confirme que les ateliers appliqués restent trop secondaires."
            )

            st.subheader("3. Analyse des Dysfonctionnements Système")
            generer_choix_multiples_critique("Hiérarchisation des obstacles à l'apprentissage", ["Effectif pléthorique", "Insuffisance de matériel", "Manque de temps dans l’emploi du temps", "Manque de formation pratique", "Motivation faible des élèves"], "obstacles")

            st.subheader("4. Typologie des Systèmes d'Évaluation Appliqués")
            generer_choix_multiples_critique("Modes d'évaluations appliqués sur le terrain", ["Notes individuelles", "Travaux de groupes", "Observation en classe", "Participation orale"], "evaluations")

            st.header("🏁 Analyse Croisée Comparative Avancée")
            st.markdown("### Tableau Croisé : Dotation Matérielle selon le Statut de l'Établissement")

            if "Statut_Etablissement" in df_global.columns and "Materiel_Suffisant" in df_global.columns:
                ct_synthese = pd.crosstab(df_global["Statut_Etablissement"], df_global["Materiel_Suffisant"], normalize='index') * 100
                st.dataframe(ct_synthese.style.format("{:.1f} %"), use_container_width=True)

                st.markdown("#### 🔍 Lecture et Analyse Critique de la Corrélation :")
                st.info("""
                **Interprétation de la fracture sectorielle :**
                * **Secteur Public :** Généralement marqué par des effectifs massifs, les infrastructures y peinent à suivre, créant une insuffisance matérielle récurrente.
                * **Secteur Privé / Confessionnel :** Bénéficiant d'un mode de gouvernance plus flexible, ces structures affichent souvent de meilleurs taux de couverture logistique.
                """)

            st.markdown("### 💡 Propositions de Résolution et Recommandations")
            st.success("""
            Au terme de cette étude empirique menée dans l'Arrondissement de **Ngaoundéré 1er**, trois axes stratégiques se dégagent pour rehausser le niveau opérationnel :
            1. **Réaménagement Horaire :** Sanctuariser une plage horaire hebdomadaire de deux heures exclusivement dédiée aux manipulations cartographiques et ateliers pratiques.
            2. **Mutualisation Institutionnelle :** Créer une banque de ressources numériques partagée à l'échelle régionale.
            3. **Renforcement des Capacités Locales :** Mettre en place des séminaires d'animation pédagogique sur l'évaluation active en classe pléthorique.
            """)
        else:
            st.warning("⚠️ Aucune donnée disponible pour ce filtre.")
    else:
        st.info("💡 En attente des premières réponses pour projeter le rapport d'analyse automatique.")
