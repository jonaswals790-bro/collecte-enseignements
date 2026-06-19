import streamlit as st
import pandas as pd
import os
import subprocess
from datetime import datetime
import plotly.express as px  # Pour les camemberts interactifs dans Streamlit

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

# Fonction pour synchroniser automatiquement les fichiers modifiés vers GitHub
def synchroniser_vers_github(nom_etab):
    try:
        subprocess.run(["git", "config", "--global", "user.email", "jonasboulmo@gmail.com"], check=True)
        subprocess.run(["git", "config", "--global", "user.name", "Boulmo Jonas (Wals)"], check=True)
        
        subprocess.run(["git", "add", DATA_FILE, README_FILE], check=True)
        commit_message = f"Data: nouvel enregistrement automatique - {nom_etab}"
        subprocess.run(["git", "commit", "-m", commit_message], check=True)
        subprocess.run(["git", "push", "origin", "main"], check=True)
    except Exception as e:
        pass

if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
    df_global = pd.read_csv(DATA_FILE)
else:
    df_global = pd.DataFrame(columns=COLUMNS_BLOC)

# --- FONCTION DE GÉNÉRATION DU RAPPORT HTML AVEC CAMEMBERTS 3D INTÉGRÉS ---
def generer_rapport_html_universitaire(df_source, statut_filtre):
    total_r = len(df_source)
    
    def clean_js_str(text):
        return str(text).replace("'", " ").replace("’", " ").replace("\n", " ").replace("\r", " ").strip()
    
    # 1. Données Ancienneté (Camembert 3D)
    c_anc = df_source["Anciennete"].value_counts() if "Anciennete" in df_source.columns else pd.Series()
    data_anc_js = []
    if total_r > 0 and not c_anc.empty:
        max_val = c_anc.max()
        for k, v in c_anc.items():
            pct = float(v / total_r * 100)
            sliced = "true" if v == max_val else "false"
            data_anc_js.append(f"{{ name: '{clean_js_str(k)}', y: {pct:.1f}, sliced: {sliced}, selected: {sliced} }}")
    data_anc_str = "[" + ", ".join(data_anc_js) + "]" if data_anc_js else "[]"

    # 2. Données Fréquence (Camembert 3D)
    c_frq = df_source["Frequence_Exercices"].value_counts() if "Frequence_Exercices" in df_source.columns else pd.Series()
    data_frq_js = []
    if total_r > 0 and not c_frq.empty:
        max_val = c_frq.max()
        for k, v in c_frq.items():
            pct = float(v / total_r * 100)
            sliced = "true" if v == max_val else "false"
            data_frq_js.append(f"{{ name: '{clean_js_str(k)}', y: {pct:.1f}, sliced: {sliced}, selected: {sliced} }}")
    data_frq_str = "[" + ", ".join(data_frq_js) + "]" if data_frq_js else "[]"

    # 3. Données Suffisance Matérielle (Le fameux Camembert 3D Oui/Non demandé)
    c_mat = df_source["Materiel_Suffisant"].value_counts() if "Materiel_Suffisant" in df_source.columns else pd.Series()
    data_mat_js = []
    if total_r > 0 and not c_mat.empty:
        max_val = c_mat.max()
        for k, v in c_mat.items():
            pct = float(v / total_r * 100)
            sliced = "true" if v == max_val else "false"
            data_mat_js.append(f"{{ name: '{clean_js_str(k)}', y: {pct:.1f}, sliced: {sliced}, selected: {sliced} }}")
    data_mat_str = "[" + ", ".join(data_mat_js) + "]" if data_mat_js else "[]"

    # 4. Obstacles (Histogramme 3D)
    list_obs = ["Effectif pléthorique", "Insuffisance de matériel", "Manque de temps dans l’emploi du temps", "Manque de formation pratique", "Motivation faible des élèves"]
    clean_labels_obs = str([clean_js_str(x) for x in list_obs])
    data_obs = [float(df_source[col].sum() / total_r * 100) if col in df_source.columns and total_r > 0 else 0 for col in list_obs]

    # 5. Évaluations (Donut/Anneau 3D)
    list_ev = ["Notes individuelles", "Travaux de groupes", "Observation en classe", "Participation orale"]
    data_ev_js = []
    if total_r > 0:
        for col in list_ev:
            pct = float(df_source[col].sum() / total_r * 100) if col in df_source.columns else 0
            data_ev_js.append(f"{{ name: '{clean_js_str(col)}', y: {pct:.1f} }}")
    data_ev_str = "[" + ", ".join(data_ev_js) + "]" if data_ev_js else "[]"

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Rapport d'Analyse Scientifique et Critique</title>
        <script src="https://code.highcharts.com/highcharts.js"></script>
        <script src="https://code.highcharts.com/highcharts-3d.js"></script>
        <style>
            body {{ font-family: 'Times New Roman', Times, serif; line-height: 1.6; color: #111; margin: 50px; font-size: 15px; }}
            .header {{ text-align: center; margin-bottom: 35px; border-bottom: 3px double #1E3A8A; padding-bottom: 15px; }}
            .title {{ color: #1E3A8A; font-size: 18px; font-weight: bold; margin-top: 25px; text-transform: uppercase; }}
            .subtitle {{ font-style: italic; font-size: 14px; color: #444; margin-bottom: 15px; font-weight: bold; }}
            .meta-box {{ background-color: #F9FAFB; padding: 20px; border: 1px solid #D1D5DB; border-radius: 4px; margin-bottom: 30px; }}
            h2 {{ color: #1E3A8A; border-bottom: 1px solid #1E3A8A; padding-bottom: 5px; margin-top: 35px; font-size: 16px; text-transform: uppercase; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 15px; margin-bottom: 15px; font-family: Arial, sans-serif; font-size: 13px; }}
            th, td {{ border: 1px solid #9CA3AF; padding: 8px; text-align: center; }}
            th {{ background-color: #F3F4F6; color: #111; }}
            .interpretation {{ background-color: #F0F4F8; border-left: 4px solid #1E3A8A; padding: 15px; margin-top: 12px; font-style: italic; margin-bottom: 20px; }}
            .chart-container {{ width: 85%; margin: 25px auto; height: 380px; background: #fff; padding: 15px; border: 1px solid #E5E7EB; border-radius: 6px; }}
            .footer {{ text-align: center; margin-top: 60px; font-size: 13px; border-top: 1px solid #9CA3AF; padding-top: 15px; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">EVALUATION DES DYSFONCTIONNEMENTS DE LA CONDUITE DES EXERCICES PRATIQUES EN HISTOIRE-GEOGRAPHIE ET EDUCATION A LA CITOYENNETE</div>
            <div class="subtitle">CAS DE L'ARRONDISSEMENT DE NGAOUNDÉRÉ 1ER</div>
        </div>
        
        <div class="meta-box">
            <strong>Filtre d'analyse :</strong> Secteur {statut_filtre}<br>
            <strong>Taille de l'échantillon ($N$) :</strong> {total_r} Enseignant(s)<br>
            <strong>Généré le :</strong> {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
        </div>
    """

    if total_r > 0:
        # Section 1
        html += "<h2>1. Analyse du Profil Socio-Professionnel</h2>"
        if not c_anc.empty:
            html += "<h3>Distribution de l'ancienneté</h3>" + pd.DataFrame(c_anc).to_html()
            html += '<div id="chartAnciennete3D" class="chart-container"></div>'

        # Section 2
        html += "<h2>2. Évaluation des Pratiques Pédagogiques</h2>"
        if not c_frq.empty:
            html += "<h3>Fréquence d'intégration des exercices</h3>" + pd.DataFrame(c_frq).to_html()
            html += '<div id="chartFrequence3D" class="chart-container"></div>'

        # Section NOUVELLE : Matériel Suffisant (Camembert de l'image)
        html += "<h2>3. Analyse de la Dotation en Matériel Didactique</h2>"
        if not c_mat.empty:
            html += "<h3>Disponibilité et suffisance du matériel</h3>" + pd.DataFrame(c_mat).to_html()
            html += '<div id="chartMateriel3D" class="chart-container"></div>'

        # Section Obstacles
        html += "<h2>4. Hiérarchisation des Obstacles Rencontrés</h2>"
        html += '<div id="chartObstacles3D" class="chart-container"></div>'

        # Section Évaluations
        html += "<h2>5. Typologie des Modes d'Évaluation</h2>"
        html += '<div id="chartEvaluations3D" class="chart-container"></div>'
        
        # Section Analyse Croisée
        if "Statut_Etablissement" in df_global.columns and "Materiel_Suffisant" in df_global.columns:
            html += "<h2>6. Étude Comparative Croisée (%)</h2>"
            ct = pd.crosstab(df_global["Statut_Etablissement"], df_global["Materiel_Suffisant"], normalize='index') * 100
            html += ct.to_html(float_format=lambda x: f"{x:.1f} %")
    else:
        html += "<p>Aucune donnée disponible.</p>"

    html += f"""
        <div class="footer">Document Officiel - Arrondissement de Ngaoundéré 1er</div>

        <script>
            document.addEventListener("DOMContentLoaded", function() {{
                const op3d = {{ enabled: true, alpha: 45, beta: 0 }};

                if ({data_anc_str}.length > 0) {{
                    Highcharts.chart('chartAnciennete3D', {{
                        chart: {{ type: 'pie', options3d: op3d }},
                        title: {{ text: 'Ancienneté des répondants' }},
                        plotOptions: {{ pie: {{ depth: 40, dataLabels: {{ enabled: true, format: '{'{point.name}'}: {'{point.percentage:.1f}'} %' }} }} }},
                        series: [{{ name: 'Proportion', data: {data_anc_str} }}]
                    }});
                }}

                if ({data_frq_str}.length > 0) {{
                    Highcharts.chart('chartFrequence3D', {{
                        chart: {{ type: 'pie', options3d: op3d }},
                        title: {{ text: 'Fréquence des exercices pratiques' }},
                        plotOptions: {{ pie: {{ depth: 40, dataLabels: {{ enabled: true, format: '{'{point.name}'}: {'{point.percentage:.1f}'} %' }} }} }},
                        series: [{{ name: 'Part', data: {data_frq_str} }}]
                    }});
                }}

                if ({data_mat_str}.length > 0) {{
                    Highcharts.chart('chartMateriel3D', {{
                        chart: {{ type: 'pie', options3d: op3d }},
                        title: {{ text: 'Pourcentage de suffisance matérielle (Oui / Non)' }},
                        plotOptions: {{ pie: {{ depth: 45, dataLabels: {{ enabled: true, format: '<b>{'{point.name}'}</b>: {'{point.percentage:.1f}'} %' }} }} }},
                        series: [{{ name: 'Réponses', data: {data_mat_str} }}]
                    }});
                }}

                if (document.getElementById('chartObstacles3D')) {{
                    Highcharts.chart('chartObstacles3D', {{
                        chart: {{ type: 'column', options3d: {{ enabled: true, alpha: 15, beta: 15, depth: 50 }} }},
                        title: {{ text: 'Obstacles structurels identifiés (%)' }},
                        xAxis: {{ categories: {clean_labels_obs} }},
                        series: [{{ name: 'Taux de citation', data: {data_obs}, color: '#EF4444' }}]
                    }});
                }}

                if ({data_ev_str}.length > 0) {{
                    Highcharts.chart('chartEvaluations3D', {{
                        chart: {{ type: 'pie', options3d: op3d }},
                        title: {{ text: 'Modes d’évaluations appliqués' }},
                        plotOptions: {{ pie: {{ innerSize: 100, depth: 40, dataLabels: {{ enabled: true, format: '{'{point.name}'}: {'{point.y:.1f}'} %' }} }} }},
                        series: [{{ name: 'Pénétration', data: {data_ev_str} }}]
                    }});
                }}
            }});
        </script>
    </body>
    </html>
    """
    return html


# =============================================================================
# PANNEAU DE CONTRÔLE (SIDEBAR)
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
        csv_data = df_global.to_csv(index=False, encoding="utf-8")
        st.download_button(
            label="📊 Sauvegarder les Données (CSV)",
            data=csv_data,
            file_name=f"Donnees_Brutes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            use_container_width=True
        )
        
        html_archive = generer_rapport_html_universitaire(df_global, "Tous")
        st.download_button(
            label="💾 Sauvegarder Tableaux + Camemberts 3D (HTML)",
            data=html_archive,
            file_name=f"Rapport_Analyses_Ngaoundere_1er.html",
            mime="text/html",
            use_container_width=True
        )
    else:
        st.caption("Aucune donnée à exporter.")


# =============================================================================
# EN-TÊTE PRINCIPAL
# =============================================================================
st.markdown("""
    <style>
    .header-box { background-color: #1E293B; padding: 30px; border-radius: 8px; border-left: 8px solid #EF4444; color: #FFFFFF; margin-bottom: 25px; }
    .title-main { font-family: 'Arial', sans-serif; font-size: 20px; font-weight: bold; line-height: 1.4; text-transform: uppercase; }
    .theme-text { color: #F87171; }
    </style>
    <div class='header-box'>
        <div class='title-main'>
            QUESTIONNAIRE DÉTAILLÉ DESTINÉ AUX ENSEIGNANTS ET AUX APPRENANTS SUR LE THÈME :<br>
            <span class='theme-text'>« ÉVALUATION DES DYSFONCTIONNEMENTS DE LA CONDUITE DES EXERCICES PRATIQUES EN HISTOIRE-GÉOGRAPHIE ET ÉDUCATION À LA CITOYENNETÉ : CAS DE L'ARRONDISSEMENT DE NGAOUNDÉRÉ 1<sup>ER</sup> »</span>
        </div>
    </div>
""", unsafe_allow_html=True)

tab_form, tab_dash = st.tabs(["📝 Formulaire & Opérations", "📊 Rapport d'Analyse & Critique Scientifique"])

# =============================================================================
# ONGLET 1 : FORMULAIRE ET OPERATIONS (CRUD)
# =============================================================================
with tab_form:
    if action == "➕ Ajouter une personne":
        with st.form("form_evaluation"):
            st.header("I. Informations Personnelles et Professionnelles")
            col1, col2 = st.columns(2)
            with col1:
                sexe = st.radio("1. Sexe :", ["Masculin", "Féminin"], horizontal=True)
                age = st.radio("2. Âge :", ["Moins de 30 ans", "30 – 40 ans", "41 – 50 ans", "Plus de 50 ans"], horizontal=True)
                diplome = st.selectbox("3. Diplôme obtenu :", ["DIPES I", "DIPES II", "Licence", "Master", "Autre"])
                diplome_autre = st.text_input("Précisez :") if diplome == "Autre" else ""
            with col2:
                specialite = st.radio("Spécialité dominane :", ["Histoire", "Géographie"], horizontal=True)
                anciennete = st.radio("4. Ancienneté :", ["Moins de 5 ans", "6 à 10 ans", "11 à 15 ans", "Plus de 15 ans"], horizontal=True)
                nom_etab = st.text_input("5. Nom de l'établissement :")
                statut_etab = st.radio("Statut :", ["Public", "Privé", "Confessionnel"], horizontal=True)

            st.header("II. Pratiques Pédagogiques")
            frequence = st.select_slider("6. Fréquence d'intégration :", options=["Jamais", "Rarement", "Parfois", "Souvent", "À chaque leçon"])
            
            type_doc = st.checkbox("Analyse de documents historiques ou géographiques")
            type_carte = st.checkbox("Lecture et interprétation des cartes")
            type_groupe = st.checkbox("Travaux de groupe", key="k1")
            type_terrain = st.checkbox("Sorties pédagogiques / visites de terrain")
            type_jeux = st.checkbox("Jeux de rôle ou simulations citoyennes")

            mat_didactique = st.radio("8. Matériel didactique suffisant ?", ["Oui", "Non"], horizontal=True)
            manques_mat = st.text_area("Si non, précisez :") if mat_didactique == "Non" else ""

            formation_specifique = st.radio("9. Formation spécifique reçue ?", ["Oui", "Non"], horizontal=True)
            formation_details = st.text_input("Si oui, détails :") if formation_specifique == "Oui" else ""
            temps_accorde = st.radio("10. Temps accordé :", ["Moins de 15 min", "15 – 30 min", "30 – 60 min", "Plus d’une heure"], horizontal=True)

            st.header("III. Dysfonctionnements rencontrés")
            obs_effectifs = st.checkbox("Effectif pléthorique")
            obs_materiel = st.checkbox("Insuffisance de matériel")
            obs_temps = st.checkbox("Manque de temps")
            obs_formation = st.checkbox("Manque de formation pratique")
            obs_motivation = st.checkbox("Motivation faible des élèves")

            exemple_concret = st.text_area("2. Exemple concret d'échec :")
            conditions_etab = st.radio("3. Conditions favorables ?", ["Oui", "Non", "Partiellement"], horizontal=True)
            justification_cond = st.text_area("Justifiez :")

            st.header("IV. Évaluation et Suivi")
            eval_notes = st.checkbox("Notes individuelles")
            eval_groupes = st.checkbox("Travaux de groupes", key="k2")
            eval_obs = st.checkbox("Observation en classe")
            eval_orale = st.checkbox("Participation orale")

            amelioration_apprentissage = st.radio("2. Amélioration constatée ?", ["Oui, beaucoup", "Oui, un peu", "Non, vraiment pas", "Pas d'avis"], horizontal=True)
            explication_apprentissage = st.text_area("Expliquez :")
            solutions_propositions = st.text_area("3. Vos solutions stratégiques :")

            submit_button = st.form_submit_button(label="💾 Enregistrer la réponse")

        if submit_button and nom_etab:
            horodatage_actuel = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            nouvelle_reponse = {
                "Horodatage": horodatage_actuel, "Sexe": sexe, "Age": age,
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

            with open(README_FILE, "a", encoding="utf-8") as f:
                f.write(f"| {horodatage_actuel} | {nom_etab} | {statut_etab} | {solutions_propositions} |\n")

            synchroniser_vers_github(nom_etab)
            st.success("🎉 Enregistrement effectué !")
            st.rerun()

    elif action == "✏️ Modifier une entrée" and not df_global.empty:
        options_mod = df_global.apply(lambda r: f"{r['Etablissement']} ({r['Horodatage']})", axis=1).tolist()
        selected_edit = st.selectbox("Ligne à modifier :", options_mod)
        idx_edit = options_mod.index(selected_edit)
        
        new_etab = st.text_input("Établissement :", value=df_global.at[idx_edit, 'Etablissement'])
        new_sol = st.text_area("Propositions :", value=df_global.at[idx_edit, 'Propositions_Solutions'])
        
        if st.button("💾 Sauvegarder"):
            df_global.at[idx_edit, 'Etablissement'] = new_etab
            df_global.at[idx_edit, 'Propositions_Solutions'] = new_sol
            df_global.to_csv(DATA_FILE, index=False, encoding="utf-8")
            synchroniser_vers_github(new_etab)
            st.rerun()

    elif action == "❌ Supprimer une entrée" and not df_global.empty:
        options_sup = df_global.apply(lambda r: f"{r['Etablissement']} ({r['Horodatage']})", axis=1).tolist()
        selected_del = st.selectbox("Ligne à détruire :", options_sup)
        if st.button("🔥 Confirmer"):
            idx_del = options_sup.index(selected_del)
            df_global = df_global.drop(df_global.index[idx_del])
            df_global.to_csv(DATA_FILE, index=False, encoding="utf-8")
            synchroniser_vers_github("Suppression")
            st.rerun()


# =============================================================================
# ONGLET 2 : RAPPORT D'ANALYSE (VISUALISATION DANS L'APP)
# =============================================================================
with tab_dash:
    st.header("🔬 Diagnostic Statistique et Sociopédagogique")
    if not df_global.empty:
        statut_selection = st.selectbox("🗂️ Secteur d'analyse :", ["Tous", "Public", "Privé", "Confessionnel"])
        df = df_global if statut_selection == "Tous" else df_global[df_global["Statut_Etablissement"] == statut_selection]
        total_reponses = len(df)

        c_kpi1, c_kpi2, c_kpi3 = st.columns(3)
        with c_kpi1: st.metric("Taille de l'Échantillon ($N$)", f"{total_reponses} Enseignant(s)")
        with c_kpi2:
            tx_suf = (df["Materiel_Suffisant"].value_counts(normalize=True).get("Oui", 0) * 100) if total_reponses > 0 else 0
            st.metric("Taux de Suffisance Matérielle", f"{tx_suf:.1f} %")
        with c_kpi3:
            tx_form = (df["Formation_Specifique"].value_counts(normalize=True).get("Oui", 0) * 100) if total_reponses > 0 else 0
            st.metric("Enseignants Formés Pratiquement", f"{tx_form:.1f} %")

        st.markdown("---")

        if total_reponses > 0:
            # 1. Ancienneté
            st.markdown("### 📊 Distribution du profil d'ancienneté")
            c_anc = df["Anciennete"].value_counts()
            df_anc = pd.DataFrame({"Effectifs": c_anc.values, "Pourcentage": (c_anc.values / total_reponses * 100)}, index=c_anc.index)
            
            col_t1, col_g1 = st.columns(2)
            with col_t1: st.dataframe(df_anc.style.format({"Pourcentage": "{:.1f} %"}))
            with col_g1:
                fig1 = px.pie(df_anc, names=df_anc.index, values='Pourcentage', hole=0.2, color_discrete_sequence=px.colors.qualitative.Pastel)
                fig1.update_layout(height=230, margin=dict(t=0,b=0,l=0,r=0))
                st.plotly_chart(fig1, use_container_width=True)

            # 2. Fréquence
            st.markdown("### 📊 Fréquence d'intégration des exercices")
            c_frq = df["Frequence_Exercices"].value_counts()
            df_frq = pd.DataFrame({"Effectifs": c_frq.values, "Pourcentage": (c_frq.values / total_reponses * 100)}, index=c_frq.index)
            
            col_t2, col_g2 = st.columns(2)
            with col_t2: st.dataframe(df_frq.style.format({"Pourcentage": "{:.1f} %"}))
            with col_g2:
                fig2 = px.pie(df_frq, names=df_frq.index, values='Pourcentage', hole=0.2)
                fig2.update_layout(height=230, margin=dict(t=0,b=0,l=0,r=0))
                st.plotly_chart(fig2, use_container_width=True)

            # 3. Obstacles Structurels
            st.markdown("### ⚠️ Hiérarchisation des obstacles à l'apprentissage")
            list_obs = ["Effectif pléthorique", "Insuffisance de matériel", "Manque de temps dans l’emploi du temps", "Manque de formation pratique", "Motivation faible des élèves"]
            eff_obs = [df[c].sum() for c in list_obs]
            df_obs = pd.DataFrame({"Effectifs": eff_obs, "Pourcentage": [(e/total_reponses*100) for e in eff_obs]}, index=list_obs).sort_values(by="Effectifs", ascending=False)
            
            col_t3, col_g3 = st.columns(2)
            with col_t3: st.dataframe(df_obs.style.format({"Pourcentage": "{:.1f} %"}))
            with col_g3: st.bar_chart(df_obs["Pourcentage"], horizontal=True)

            with st.expander("🚨 Diagnostic des Vulnerabilités Institutionnelles", expanded=True):
                st.markdown(f"**Facteur d'achoppement prédominant :** {df_obs.index[0] if not df_obs.empty else 'N/A'}")
                st.markdown("Lorsque les variables matérielles et spatiales saturent, l'ajustement pédagogique induit inévitablement un recul vers l'enseignement pur magistral.")

            # 4. Évaluations
            st.markdown("### 📊 Modes d'évaluations appliqués")
            list_ev = ["Notes individuelles", "Travaux de groupes", "Observation en classe", "Participation orale"]
            eff_ev = [df[c].sum() for c in list_ev]
            df_ev = pd.DataFrame({"Effectifs": eff_ev, "Pourcentage": [(e/total_reponses*100) for e in eff_ev]}, index=list_ev).sort_values(by="Effectifs", ascending=False)
            st.dataframe(df_ev.style.format({"Pourcentage": "{:.1f} %"}))

            # 5. Analyse Croisée Comparative Avancée
            st.markdown("---")
            st.subheader("🏁 5. Analyse Croisée Comparative Avancée")
            st.markdown("#### 📑 Tableau Croisé : Dotation Matérielle selon le Statut de l'Établissement")
            if "Statut_Etablissement" in df_global.columns and "Materiel_Suffisant" in df_global.columns:
                ct_synthese = pd.crosstab(df_global["Statut_Etablissement"], df_global["Materiel_Suffisant"], normalize='index') * 100
                st.dataframe(ct_synthese.style.format("{:.1f} %"), use_container_width=True)
            
            st.info("""
            **Interprétation de la fracture sectorielle :**
            * **Secteur Public :** Généralement marqué par des effectifs massifs, infrastructures insuffisantes.
            * **Secteur Privé / Confessionnel :** Flexibilité de gouvernance, meilleur taux de couverture logistique.
            """)
            
            st.markdown("### 💡 Propositions de Résolution et Recommandations")
            st.success("""
            Au terme de cette étude empirique menée dans l'**Arrondissement de Ngaoundéré 1er**, trois axes stratégiques se dégagent :
            1. **Modernisation logistique :** Dotation prioritaire des établissements en cartes murales modernes, globes terrestres et outils numériques de projection.
            2. **Allègement des effectifs :** Implantation de sections d'apprentissage dédoublées lors des phases de travaux dirigés en Histoire-Géographie.
            3. **Renforcement des capacités :** Organisation de séminaires d'imprégnation pédagogique centrés exclusivement sur l'administration des exercices pratiques conformes à l'APC.
            """)
    else:
        st.info("💡 En attente des premières données saisies.")
