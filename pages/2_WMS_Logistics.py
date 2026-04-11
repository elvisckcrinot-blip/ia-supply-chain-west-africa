import streamlit as st
import pandas as pd
from models.mit_calculations import calcul_wilson_eoq, analyse_pareto_abc
import io

# --- CONFIG ET STYLE ---
st.set_page_config(page_title="WMS Intelligence · Bénin", layout="wide")

st.markdown("""
<style>
    @import url('https://googleapis.com');
    .main-title { font-family: 'Syne', sans-serif; color: #ffad1f; font-size: 38px; font-weight: 800; }
    .wms-card { background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.1); border-radius: 12px; padding: 20px; text-align: center; }
    .wms-val { font-family: 'Syne', sans-serif; font-size: 32px; font-weight: 800; color: #ffad1f; }
</style>
""", unsafe_allow_html=True)

# --- FONCTION EXPORT EXCEL ---
def to_excel_plan_achat(df_alertes):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_alertes.to_excel(writer, index=False, sheet_name='Plan_Achat_Urgent')
    return output.getvalue()

st.markdown('<h1 class="main-title">📦 WMS Intelligence : Stocks & Alertes</h1>', unsafe_allow_html=True)
st.markdown("---")

tab1, tab2 = st.tabs(["📊 Analyse & Plan d'Achat", "⚙️ Optimisation Wilson"])

with tab1:
    st.sidebar.header("📁 Importation")
    uploaded_file = st.sidebar.file_uploader("Fichier Stock (Référence, Valeur, Quantité, ROP_Seuil)", type=["csv", "xlsx"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        cols_requises = ['Référence', 'Valeur', 'Quantité', 'ROP_Seuil']
        
        if all(col in df.columns for col in cols_requises):
            df_abc = analyse_pareto_abc(df, 'Valeur')
            
            def definir_statut(row):
                if row['Quantité'] <= row['ROP_Seuil']: return "🔴 RUPTURE"
                if row['Quantité'] <= row['ROP_Seuil'] * 1.2: return "🟠 STOCK FAIBLE"
                return "🟢 OPTIMAL"
            
            df_abc['Statut'] = df_abc.apply(definir_statut, axis=1)
            
            # --- KPIs ---
            c1, c2, c3 = st.columns(3)
            nb_alertes = len(df_abc[df_abc['Statut'].str.contains("🔴|🟠")])
            val_total = f"{df['Valeur'].sum():,.0f}".replace(",", " ")
            
            c1.markdown(f'<div class="wms-card"><div style="color:#7a92b0; font-size:12px;">VALEUR DU STOCK</div><div class="wms-val">{val_total} FCFA</div></div>', unsafe_allow_html=True)
            c2.markdown(f'<div class="wms-card"><div style="color:#7a92b0; font-size:12px;">ARTICLES À COMMANDER</div><div class="wms-val" style="color:#ff4b4b;">{nb_alertes}</div></div>', unsafe_allow_html=True)
            c3.markdown(f'<div class="wms-card"><div style="color:#7a92b0; font-size:12px;">RÉFÉRENCES GÉRÉES</div><div class="wms-val">{len(df)}</div></div>', unsafe_allow_html=True)

            # --- BOUTON D'EXPORTATION DU PLAN D'ACHAT ---
            df_achat = df_abc[df_abc['Statut'].str.contains("🔴|🟠")].copy()
            if not df_achat.empty:
                st.warning(f"⚠️ {len(df_achat)} articles nécessitent une action d'approvisionnement.")
                excel_data = to_excel_plan_achat(df_achat[['Référence', 'Quantité', 'ROP_Seuil', 'Statut']])
                st.download_button(
                    label="📥 Télécharger le Plan d'Achat (Excel)",
                    data=excel_data,
                    file_name="plan_achat_urgent.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
            
            st.write("### 📋 Rapport d'Inventaire Complet")
            st.dataframe(df_abc[['Référence', 'Valeur', 'Classe_ABC', 'Quantité', 'Statut']], use_container_width=True)
        else:
            st.error("Colonnes manquantes dans votre fichier.")
    else:
        st.info("Veuillez charger votre fichier Excel pour activer l'analyse et le plan d'achat.")

with tab2:
    st.write("### Optimisation Wilson")
    d = st.number_input("Demande annuelle", value=1200)
    res = calcul_wilson_eoq(d, 5000, 250)
    st.markdown(f'<div class="wms-card"><div class="wms-val">{res} Unités</div></div>', unsafe_allow_html=True)

st.sidebar.info("WMS Intelligent · Axe GDIZ")
                
