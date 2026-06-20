import streamlit as st
import pandas as pd
import os
import subprocess
from datetime import datetime
import plotly.express as px

# Configuration de la page pour un rendu professionnel et large
st.set_page_config(
    page_title="Analyse Académique - Histoire-Géo & EC",
    page_icon="📚",
    layout="wide"
)

# Fichier de stockage CSV et Markdown pour GitHub
DATA_FILE = "reponses_questionnaire.csv"
README_FILE = "README.md"

# --- INITIALISATION ET SÉCURISATION DU CSV (Les 14 variables clés + métadonnées) ---
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

# --- FONCTION DE GÉNÉRATION DU RAPPORT HTML UNIFIÉ POUR EXTRACTION ---
def generer_rapport_html_universitaire(df_source, statut_filtre):
    total_r = len(df_source)
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Rapport d'Analyse Statistique - Ngaoundéré 1er</title>
        <style>
            body {{ font-family: 'Times New Roman', Times, serif; margin: 40px; line-height: 1.6; color: #111; }}
            .header {{ text-align: center; border-bottom: 3px double #1E3A8A; padding-bottom: 15px; margin-bottom: 25px; }}
            .title {{ color: #1E3A8A; font-size: 18px; font-weight: bold; text-transform: uppercase; }}
            .meta-box {{ background-color: #F3F4F6; padding: 15px; border: 1px solid #D1D5DB; margin-bottom: 25px; }}
            h2 {{ color: #1E3A8A; border-bottom: 1px solid #1E3A8A; padding-bottom: 5px; margin-top: 30px; text-transform: uppercase; font-size: 14px; }}
            h3 {{ color: #2563EB; font-size: 13px; margin-top: 15px; }}
            table {{ width: 100%; border-collapse: collapse; margin: 15px 0; font-family: Arial, sans-serif; font-size: 12px; }}
            th, td {{ border: 1px solid #9CA3AF; padding: 8px; text-align: center; }}
            th {{ background-color: #E5E7EB; }}
            .interpretation {{ background-color: #F0F4F8; border-left: 4px solid #1E3A8A; padding: 12px; margin: 10px 0; font-style: italic; }}
        </style>
    </head>
    <body>
        <div class="header">
            <div class="title">ÉVALUATION DES DYSFONCTIONNEMENTS DE LA CONDUITE DES EXERCICES PRATIQUES EN HISTOIRE-GÉOGRAPHIE ET ÉDUCATION À LA CITOYENNETÉ</div>
            <div style="font-style: italic; font-weight: bold;">CAS DE L'ARRONDISSEMENT DE NGAOUNDÉRÉ 1ER</div>
        </div>
        <div class="meta-box">
            <strong>Filtre sectoriel :</strong> {statut_filtre}<br>
            <strong>Échantillon analysé ($N$) :</strong> {total_r} Enseignant(s)<br>
            <strong>Date d'extraction :</strong> {datetime.now().strftime('%d/%m/%Y à %H:%M:%S')}
        </div>
    """
    if total_r > 0:
        def table_html(col_name, label, desc):
            c = df_source[col_name].value_counts() if col_name in df_source.columns else pd.Series()
            df_t = pd.DataFrame({"Effectifs": c.values, "Pourcentage": (c.values / total_r * 100)}, index=c.index)
            return f"<h2>{label}</h2>" + df_t.to_html(float_format=lambda x: f"{x:.1f} %") + f"<div class='interpretation'><strong>Analyse & Interprétation :</strong> {desc}</div><br>"

        # Section 1
        html += table_html("Sexe", "Tableau 1 : Répartition des répondants par Sexe", "Met en évidence la structure de genre au sein du personnel enseignant.")
        html += table_html("Age", "Tableau 2 : Structure démographique par Tranches d'Âge", "Permet d'évaluer la maturité et la répartition générationnelle des enseignants.")
        html += table_html("Diplome", "Tableau 3 : Profil de Qualification Académique et Professionnelle", "Révèle le niveau de certification professionnelle (DIPES, Licences, Masters) par rapport aux exigences de l'APC.")
        html += table_html("Specialite", "Tableau 4 : Spécialisation Disciplinaire Dominante", "Indique l'équilibre interne entre les profils d'historiens et de géographes.")
        html += table_html("Anciennete", "Tableau 5 : Distribution de l'Expérience Professionnelle (Ancienneté)", "Témoigne de la maîtrise des routines d'évaluation et de la réceptivité face aux réformes.")
        html += table_html("Statut_Etablissement", "Tableau 6 : Profil Typologique des Établissements Rattachés", "Cartographie la provenance institutionnelle des données.")

        # Section 2
        html += table_html("Frequence_Exercices", "Tableau 7 : Fréquence d'Administration des Exercices Pratiques", "Mesure le taux d'application effective de la manipulation face aux cours magistraux théoriques.")
        html += table_html("Materiel_Suffisant", "Tableau 8 : Appréciation Quantitative de la Dotation Matérielle", "Souligne la crise ou la suffisance des ressources didactiques indispensables sur le terrain.")
        html += table_html("Formation_Specifique", "Tableau 9 : Diagnostic d'Accès à une Formation Pratique APC", "Quantifie le besoin d'accompagnement andragogique institutionnel continue.")
        html += table_html("Temps_Accorde", "Tableau 10 : Évaluation de la Chronographie Horaire Dédiée", "Analyse si l'enveloppe temporelle choisie par l'enseignant au cours d'une leçon permet la réalisation complète des TP.")

        # Section 3
        html += table_html("Conditions_Etab_Favorables", "Tableau 11 : Perception Globale de la Viabilité Environnementale", "Détermine si le cadre spatial et managérial de l'établissement favorise les exercices pratiques.")

        # Pour les obstacles (Tableau 12) et Évaluations (Tableau 13)
        list_obs = ["Effectif pléthorique", "Insuffisance de matériel", "Manque de temps dans l’emploi du temps", "Manque de formation pratique", "Motivation faible des élèves"]
        df_obs = pd.DataFrame({"Effectifs": [df_source[c].sum() for c in list_obs if c in df_source.columns]}, index=list_obs)
        html += "<h2>Tableau 12 : Hiérarchisation des Obstacles Systémiques Majeurs</h2>" + df_obs.to_html() + "<br>"

        list_ev = ["Notes individuelles", "Travaux de groupes", "Observation en classe", "Participation orale"]
        df_ev = pd.DataFrame({"Effectifs": [df_source[c].sum() for c in list_ev if c in df_source.columns]}, index=list_ev)
        html += "<h2>Tableau 13 : Typologie des Modes d'Évaluation Appliqués</h2>" + df_ev.to_html() + "<br>"

        # Tableau 14
        html += table_html("Amelioration_Citoyennete", "Tableau 14 : Impact Perçu sur l'Éveil des Compétences Citoyennes", "Mesure le retour concret sur investissement pédagogique pour le civisme des élèves.")

        # Analyse Croisée
        if "Statut_Etablissement" in df_source.columns and "Materiel_Suffisant" in df_source.columns:
            html += "<h2>5. Analyse Croisée Comparative Avancée</h2>"
            html += "<h3>Tableau Croisé : Dotation Matérielle selon le Statut de l'Établissement</h3>"
            ct = pd.crosstab(df_source["Statut_Etablissement"], df_source["Materiel_Suffisant"], normalize='index') * 100
            html += ct.to_html(float_format=lambda x: f"{x:.1f} %")
    else:
        html += "<p>Aucune donnée disponible pour générer les matrices.</p>"
    
    html += "</body></html>"
    return html

# =============================================================================
# PANNEAU DE CONTRÔLE (SIDEBAR)
# =============================================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluent/96/000000/database.png", width=80)
    st.title("🎛️ Panneau de Contrôle")
    st.markdown("---")
    action = st.radio("Sélectionnez une action opérationnelle :", ["➕ Ajouter une personne", "✏️ Modifier une entrée", "❌ Supprimer une entrée"])
    st.markdown("---")
    st.subheader("📥 Extractions Disponibles")
    if not df_global.empty:
        st.download_button(label="📊 Sauvegarder les Données (CSV)", data=df_global.to_csv(index=False, encoding="utf-8"), file_name=f"Donnees_Brutes_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv", use_container_width=True)
        st.download_button(label="💾 Sauvegarder les 14 Tableaux (HTML)", data=generer_rapport_html_universitaire(df_global, "Tous"), file_name="Rapport_Analyses_14_Tableaux.html", mime="text/html", use_container_width=True)

# =============================================================================
# EN-TÊTE PRINCIPAL
# =============================================================================
st.markdown("""
    <style>
    .header-box { background-color: #1E293B; padding: 25px; border-radius: 8px; border-left: 8px solid #EF4444; color: #FFFFFF; margin-bottom: 25px; }
    .title-main { font-family: 'Arial', sans-serif; font-size: 19px; font-weight: bold; line-height: 1.4; text-transform: uppercase; }
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
                specialite = st.radio("Spécialité dominante :", ["Histoire", "Géographie"], horizontal=True)
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
            pd.DataFrame([nouvelle_reponse]).to_csv(DATA_FILE, mode='a', header=not os.path.isfile(DATA_FILE), index=False, encoding="utf-8")
            with open(README_FILE, "a", encoding="utf-8") as f:
                f.write(f"| {horodatage_actuel} | {nom_etab} | {statut_etab} |\n")
            synchroniser_vers_github(nom_etab)
            st.success("🎉 Données enregistrées avec succès !")
            st.rerun()

    elif action == "✏️ Modifier une entrée" and not df_global.empty:
        options_mod = df_global.apply(lambda r: f"{r['Etablissement']} ({r['Horodatage']})", axis=1).tolist()
        selected_edit = st.selectbox("Ligne à modifier :", options_mod)
        idx_edit = options_mod.index(selected_edit)
        new_etab = st.text_input("Nom Établissement :", value=df_global.at[idx_edit, 'Etablissement'])
        if st.button("💾 Mettre à jour"):
            df_global.at[idx_edit, 'Etablissement'] = new_etab
            df_global.to_csv(DATA_FILE, index=False, encoding="utf-8")
            synchroniser_vers_github(new_etab)
            st.rerun()

    elif action == "❌ Supprimer une entrée" and not df_global.empty:
        options_sup = df_global.apply(lambda r: f"{r['Etablissement']} ({r['Horodatage']})", axis=1).tolist()
        selected_del = st.selectbox("Ligne à supprimer :", options_sup)
        if st.button("🔥 Confirmer la suppression"):
            df_global.drop(df_global.index[options_sup.index(selected_del)]).to_csv(DATA_FILE, index=False, encoding="utf-8")
            synchroniser_vers_github("Suppression")
            st.rerun()

# =============================================================================
# ONGLET 2 : DIAGNOSTIC INTÉGRAL DE 14 TABLEAUX AVEC CAMEMBERTS INDIVIDUELS
# =============================================================================
with tab_dash:
    st.header("🔬 Diagnostic Statistique et Sociopédagogique Élaboré")
    if not df_global.empty:
        statut_selection = st.selectbox("🗂️ Filtrer l'analyse par secteur :", ["Tous", "Public", "Privé", "Confessionnel"])
        df = df_global if statut_selection == "Tous" else df_global[df_global["Statut_Etablissement"] == statut_selection]
        total_reponses = len(df)

        # Cartes d'indicateurs globaux (KPIs)
        col_k1, col_k2, col_k3 = st.columns(3)
        col_k1.metric("Taille globale de l'échantillon ($N$)", f"{total_reponses} Enseignant(s)")
        col_k2.metric("Indice de Carence Logistique", f"{(df['Materiel_Suffisant'].value_counts(normalize=True).get('Non', 0)*100):.1f} %")
        col_k3.metric("Besoin en Renforcement Imprégnation", f"{(df['Formation_Specifique'].value_counts(normalize=True).get('Non', 0)*100):.1f} %")
        st.markdown("---")

        if total_reponses > 0:
            # Fonction d'affichage dynamique automatisée pour l'harmonie des blocs
            def afficher_bloc_statistique(colonne_df, titre_tableau, description_critique, palette_couleur=None):
                st.subheader(titre_tableau)
                c_data = df[colonne_df].value_counts()
                df_table = pd.DataFrame({"Effectifs": c_data.values, "Pourcentage": (c_data.values / total_reponses * 100)}, index=c_data.index)
                
                col_tab, col_graph = st.columns(2)
                with col_tab:
                    st.dataframe(df_table.style.format({"Pourcentage": "{:.1f} %"}), use_container_width=True)
                with col_graph:
                    fig = px.pie(df_table, names=df_table.index, values='Effectifs', hole=0.15,
                                 color_discrete_sequence=palette_couleur if palette_couleur else px.colors.qualitative.Safe)
                    fig.update_layout(height=210, margin=dict(t=10,b=10,l=10,r=10))
                    st.plotly_chart(fig, use_container_width=True)
                with st.expander("🔍 Lecture, interprétation critique & cohérence sociopédagogique"):
                    st.markdown(description_critique)
                st.markdown("<br>", unsafe_allow_html=True)

            # --- SECTION I : PROFIL SOCIO-PROFESSIONNEL (6 Tableaux) ---
            st.markdown("## 1️⃣ Section I : Analyse Micro-Structurelle du Corps Enseignant")
            
            afficher_bloc_statistique("Sexe", "Tableau 1 : Répartition des répondants par Sexe", 
                "**Interprétation :** Met en lumière la distribution de genre au sein de l'enseignement des sciences humaines. Cela permet d'évaluer la représentativité et l'équilibre homme-femme dans l'arrondissement.")
            
            afficher_bloc_statistique("Age", "Tableau 2 : Structure démographique par Tranches d'Âge", 
                "**Interprétation :** Révèle la structure d'âge de l'échantillon. Une population majoritairement jeune implique un dynamisme potentiel, tandis qu'une tranche mature indique une forte assise empirique mais potentiellement plus résistante aux nouvelles directives technologiques.")
            
            afficher_bloc_statistique("Diplome", "Tableau 3 : Profil de Qualification Académique et Professionnelle", 
                "**Interprétation :** Examine l'adéquation entre les diplômes professionnels obtenus (DIPES, Master, etc.) et le niveau d'exigence scientifique requis pour appliquer l'Approche Par Compétences (APC).")
            
            afficher_bloc_statistique("Specialite", "Tableau 4 : Spécialisation Disciplinaire Dominante", 
                "**Interprétation :** L'analyse du ratio Historiciens / Géographes permet de comprendre certaines prédispositions dans la conduite des TP (ex: aisance avec le fonds cartographique ou l'exégèse documentaire).")
            
            afficher_bloc_statistique("Anciennete", "Tableau 5 : Distribution de l'Expérience Professionnelle (Ancienneté)", 
                "**Interprétation :** L'expérience professionnelle garantit une bonne assise des routines de gestion de classe, mais peut soulever la nécessité de séminaires de recyclage méthodologique réguliers face aux réformes.")
            
            afficher_bloc_statistique("Statut_Etablissement", "Tableau 6 : Profil Typologique des Établissements Rattachés", 
                "**Interprétation :** Permet de segmenter l'origine institutionnelle de l'échantillon pour déceler si les dysfonctionnements varient significativement d'un sous-système juridique à l'autre (Public vs Privé).")

            # --- SECTION II : DIAGNOSTIC DES PRATIQUES ET OUTILS (4 Tableaux) ---
            st.markdown("## 2️⃣ Section II : Diagnostic Opérationnel des Pratiques de Classe et Dotations")
            
            afficher_bloc_statistique("Frequence_Exercices", "Tableau 7 : Fréquence d'Administration des Exercices Pratiques", 
                "**Interprétation :** Évalue le degré de pénétration des activités de manipulation réelles en classe. Une fréquence faible valide l'hypothèse de la persistance du cours magistral dicté traditionnel.")
            
            afficher_bloc_statistique("Materiel_Suffisant", "Tableau 8 : Appréciation Quantitative de la Dotation Matérielle (Oui / Non)", 
                "**Interprétation :** Indique clairement le niveau de pénurie infrastructurelle. L'absence de cartes physiques, globes et outils numériques constitue un goulet d'étranglement majeur pour l'apprentissage actif.", palette_couleur=['#F87171', '#34D399'])
            
            afficher_bloc_statistique("Formation_Specifique", "Tableau 9 : Diagnostic d'Accès à une Formation Pratique Spécifique APC", 
                "**Interprétation :** Mesure le déficit d'encadrement pédagogique continue. Sans formation andragogique pratique, l'enseignant tend à reproduire des modèles d'évaluation purement théoriques.", palette_couleur=['#F59E0B', '#3B82F6'])
            
            afficher_bloc_statistique("Temps_Accorde", "Tableau 10 : Évaluation de la Chronographie Horaire Dédiée", 
                "**Interprétation :** Permet de juger si l'allocation temporelle interne au cours d'une leçon (ex: moins de 15 min) suffit techniquement à mener à bien une démarche d'investigation ou de cartographie.")

            # --- SECTION III : ENVIRONNEMENT ET OBSTACLES SYSTEMIQUES (2 Tableaux) ---
            st.markdown("## 3️⃣ Section III : Analyse des Variables Restrictives Environnementales")
            
            afficher_bloc_statistique("Conditions_Etab_Favorables", "Tableau 11 : Perception Globale de la Viabilité Environnementale de l'Établissement", 
                "**Interprétation :** Détermine si l'écosystème global de l'établissement (management, locaux, émulation) offre une conjoncture saine pour sortir des sentiers battus de la théorie.")

            # Tableau 12 : Multi-réponses pour les Obstacles Majeurs
            st.subheader("Tableau 12 : Hiérarchisation des Obstacles Systémiques Majeurs")
            list_obs = ["Effectif pléthorique", "Insuffisance de matériel", "Manque de temps dans l’emploi du temps", "Manque de formation pratique", "Motivation faible des élèves"]
            df_obs = pd.DataFrame({"Effectifs": [df[c].sum() for c in list_obs if c in df.columns]}, index=list_obs).sort_values(by="Effectifs", ascending=False)
            df_obs["Pourcentage"] = (df_obs["Effectifs"] / total_reponses * 100)
            
            col_t3, col_g3 = st.columns(2)
            with col_t3: st.dataframe(df_obs.style.format({"Pourcentage": "{:.1f} %"}), use_container_width=True)
            with col_g3: 
                st.plotly_chart(px.pie(df_obs, names=df_obs.index, values='Effectifs', color_discrete_sequence=px.colors.sequential.Reds_r).update_layout(height=210, margin=dict(t=10,b=10,l=10,r=10)), use_container_width=True)
            with st.expander("🔍 Lecture & Interprétation critique"):
                st.markdown(f"**Interprétation :** Ce classement met à nu l'entrave hégémonique majeure. La forte dominance de l'obstacle **{df_obs.index[0]}** démontre que la massification des classes ou le manque d'infrastructures étouffe l'individualisation des apprentissages.")
            st.markdown("<br>", unsafe_allow_html=True)

            # --- SECTION IV : EVALUATIONS ET IMPACT CITOYEN (2 Tableaux) ---
            st.markdown("## 4️⃣ Section IV : Typologie Docimologique et Rendement Citoyen")
            
            # Tableau 13 : Multi-réponses pour les Modes d'Évaluations
            st.subheader("Tableau 13 : Typologie des Modes d'Évaluation Appliqués sur le Terrain")
            list_ev = ["Notes individuelles", "Travaux de groupes", "Observation en classe", "Participation orale"]
            df_ev = pd.DataFrame({"Effectifs": [df[c].sum() for c in list_ev if c in df.columns]}, index=list_ev).sort_values(by="Effectifs", ascending=False)
            df_ev["Pourcentage"] = (df_ev["Effectifs"] / total_reponses * 100)
            
            col_t4, col_g4 = st.columns(2)
            with col_t4: st.dataframe(df_ev.style.format({"Pourcentage": "{:.1f} %"}), use_container_width=True)
            with col_g4: 
                st.plotly_chart(px.pie(df_ev, names=df_ev.index, values='Effectifs', hole=0.25).update_layout(height=210, margin=dict(t=10,b=10,l=10,r=10)), use_container_width=True)
            with st.expander("🔍 Lecture & Interprétation critique"):
                st.markdown("**Interprétation :** La prévalence des évaluations individuelles classiques basées sur la note chiffrée démontre la nécessité d'opérer une transition vers l'évaluation formative continue basée sur l'acquisition de réelles compétences citoyennes et transversales.")
            st.markdown("<br>", unsafe_allow_html=True)

            # Tableau 14
            afficher_bloc_statistique("Amelioration_Citoyennete", "Tableau 14 : Impact Perçu sur l'Éveil des Compétences Citoyennes", 
                "**Interprétation :** Mesure finale de l'efficience didactique. Établit le niveau de confiance des acteurs quant à l'impact des cours sur le comportement civique concret des apprenants en dehors de la classe.")

            # =============================================================================
            # COMPOSANTE COMPLÈTE FINALE : ANALYSE CROISÉE COMPARATIVE AVANCÉE
            # =============================================================================
            st.markdown("---")
            st.header("🏁 5️⃣ Analyse Croisée Comparative Avancée")
            st.markdown("#### 📑 Tableau Croisé : Dotation Matérielle selon le Statut de l'Établissement")
            
            if "Statut_Etablissement" in df_global.columns and "Materiel_Suffisant" in df_global.columns:
                ct_synthese = pd.crosstab(df_global["Statut_Etablissement"], df_global["Materiel_Suffisant"], normalize='index') * 100
                st.dataframe(ct_synthese.style.format("{:.1f} %"), use_container_width=True)
            
            st.subheader("🔍 Lecture, Cohérence et Analyse Critique de la Corrélation Matrix :")
            st.info("""
            **Interprétation analytique approfondie de la fracture sectorielle :**
            * **Secteur Public :** Globalement grevé par une massification des effectifs d'apprenants, la couverture en matériel y accuse un retard structurel et une lourdeur bureaucratique. Le taux d'insuffisance y est généralement corrélé au sous-financement des infrastructures de base.
            * **Secteur Privé / Confessionnel :** Présente une flexibilité de gouvernance logistique supérieure, lui permettant d'acquérir plus promptement du matériel didactique ciblé en fonction de la taille contrôlée de ses effectifs de classe.
            """)
            
            st.subheader("💡 Propositions Fondées de Résolution et Recommandations Institutionnelles")
            st.success("""
            Au vu de cette étude empirique systématique menée au cœur de l'**Arrondissement de Ngaoundéré 1er**, trois directives cruciales émergent pour pallier les dysfonctionnements :
            1. **Modernisation Logistique Urgente :** Dotation impérative des structures en mallettes pédagogiques APC standardisées (cartes murales modernes, globes terrestres interactifs, projecteurs mobiles).
            2. **Ajustement Spatial & Aménagement :** Allègement ou dédoublement systématique des divisions d'élèves lors des phases critiques de Travaux Pratiques en Histoire-Géographie.
            3. **Ingénierie de la Formation Continue :** Institutionnalisation de séminaires d'imrégnation docimologique trimestriels pilotés localement par les inspections d'arrondissement.
            """)
    else:
        st.info("💡 En attente de la saisie des premières réponses dans le Formulaire pour initialiser l'intégralité des 14 matrices statistiques.")
