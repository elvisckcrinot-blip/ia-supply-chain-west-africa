
‎import streamlit as stimport pandas as pdimport plotly.express as px
‎# 1. CONFIGURATION ÉLÉGANTE (Standard MIT CTL)
‎st.set_page_config(page_title="WMS Logistics - Expertise MIT", layout="wide", page_icon="📦")
‎# Style CSS pour une interface pro
‎st.markdown("""
‎    <style>
‎    .main { background-color: #f8f9fa; }
‎    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; border: 1px solid #e0e0e0; }
‎    </style>
‎    """, unsafe_allow_html=True)
‎
‎st.title("📦 WMS Logistics : Intelligence & Gestion de Stock")
‎st.info("Méthodologie MIT CTL : Optimisation du cycle de commande et gestion des risques de rupture.")
‎st.markdown("---")
‎# 2. IMPORTATION DES DONNÉES
‎st.sidebar.header("📂 Entrées de l'Entrepôt")uploaded_file = st.sidebar.file_uploader("Charger l'inventaire Excel", type=["xlsx", "csv"])
‎if uploaded_file is not None:
‎    df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)else:
‎    # Simulation automatique de 500 articles (Base MIT)
‎    data = {
‎        'ref_sku': [f'SKU-REF-{i}' for i in range(1, 501)],
‎        'designation': [f'Article Logistique {i}' for i in range(1, 501)],
‎        'prix_usine': [150000 if i % 10 == 0 else 12000 for i in range(1, 501)],
‎        'vol_unitaire_cbm': [0.15 if i % 10 == 0 else 0.01 for i in range(1, 501)],
‎        'vente_moy_jour': [2 if i % 10 == 0 else 5 for i in range(1, 501)],
‎        'lead_time_jours': [60] * 500,
‎        'stock_physique': [145 if i % 10 == 0 else 350 for i in range(1, 501)],
‎        'stock_securite': [30] * 500
‎    }
‎    df = pd.DataFrame(data)
‎# 3. 🕹️ SIMULATEUR DE SCÉNARIOS (Cerveau Décisionnel)
‎st.sidebar.markdown("---")
‎st.sidebar.header("🕹️ Simulation de Risques")hausse_demande = st.sidebar.slider("Pic de demande (%)", 0, 100, 0) / 100retard_logistique = st.sidebar.number_input("Retard livraison (jours)", 0, 90, 0)
‎# CALCULS LOGIQUES MIT CTL (Point de Commande ROP)# Formule : (Demande Journalière * Lead Time) + Stock de Sécurité
‎df['Vente_Simulee'] = df['vente_moy_jour'] * (1 + hausse_demande)
‎df['LeadTime_Simule'] = df['lead_time_jours'] + retard_logistique
‎df['ROP_MIT'] = (df['Vente_Simulee'] * df['LeadTime_Simule']) + df['stock_securite']
‎# Détermination du Statut du Stockdef check_status(row):
‎    if row['stock_physique'] <= 0: return "🚫 RUPTURE"
‎    if row['stock_physique'] <= row['ROP_MIT']: return "🔴 CRITIQUE (Commander)"
‎    if row['stock_physique'] <= row['ROP_MIT'] * 1.2: return "🟡 PRÉVENTIF (Surveiller)"
‎    return "🟢 OPTIMAL"
‎
‎df['Statut_Stock'] = df.apply(check_status, axis=1)
‎# 4. DASHBOARD DE PILOTAGE (Vue Direction)
‎st.header("📊 Tableau de Bord de l'Entrepôt")k1, k2, k3, k4 = st.columns(4)
‎with k1:
‎    total_val = (df['stock_physique'] * df['prix_usine']).sum()
‎    st.metric("Valeur du Stock", f"{total_val:,.0f} FCFA")with k2:
‎    nb_critiques = len(df[df['Statut_Stock'].str.contains("🔴")])
‎    st.metric("Articles Critiques", nb_critiques, delta="À commander", delta_color="inverse")with k3:
‎    nb_ruptures = len(df[df['Statut_Stock'].str.contains("🚫")])
‎    st.metric("Ruptures Fermes", nb_ruptures, delta_color="inverse")with k4:
‎    rotation = df['Vente_Simulee'].sum() / (df['stock_physique'].sum() / 365)
‎    st.metric("Taux de Rotation", f"{rotation:.1f}x")
‎# 5. ANALYSE GRAPHIQUE (Visualisation du Risque)
‎st.subheader("💡 Analyse de Résilience du Stock (Top 50)")fig = px.bar(df.head(50), x='ref_sku', y=['stock_physique', 'ROP_MIT'], 
‎             barmode='group', title="Stock Réel vs Seuil Critique (ROP MIT)",
‎             color_discrete_sequence=['#2ecc71', '#e74c3c'])
‎st.plotly_chart(fig, use_container_width=True)
‎# 6. INVENTAIRE DÉTAILLÉ (WMS Output)
‎st.subheader("📋 Inventaire Détaillé & Statuts")search = st.text_input("🔍 Rechercher une référence ou une désignation")if search:
‎    df_filtered = df[df['ref_sku'].str.contains(search) | df['designation'].str.contains(search)]else:
‎    df_filtered = df
‎# Style du tableau pour une lecture rapidedef style_statut(val):
‎    if "🚫" in val: return 'background-color: #ffd7d7; color: #d00000; font-weight: bold'
‎    if "🔴" in val: return 'background-color: #fff0f0; color: #e74c3c; font-weight: bold'
‎    if "🟡" in val: return 'background-color: #fff9e6; color: #f1c40f; font-weight: bold'
‎    return 'background-color: #f0fff4; color: #2ecc71; font-weight: bold'
‎
‎st.dataframe(
‎    df_filtered[['ref_sku', 'designation', 'stock_physique', 'ROP_MIT', 'Statut_Stock']].style.applymap(style_statut, subset=['Statut_Stock']),
‎    use_container_width=True
‎)
‎# 7. RÉAPPROVISIONNEMENT AUTOMATIQUE
‎st.markdown("---")
‎st.subheader("📝 Plan de Réapprovisionnement Suggéré")df_reap = df[df['Statut_Stock'].str.contains("🔴") | df['Statut_Stock'].str.contains("🚫")].copy()
‎if not df_reap.empty:
‎    # Calcul de la quantité à commander (Cible : Couvrir 30 jours après livraison)
‎    df_reap['Qte_A_Commander'] = (df_reap['ROP_MIT'] - df_reap['stock_physique'] + (df_reap['Vente_Simulee'] * 30)).astype(int)
‎    
‎    col_v1, col_v2 = st.columns(2)
‎    with col_v1:
‎        total_vol = (df_reap['Qte_A_Commander'] * df_reap['vol_unitaire_cbm']).sum()
‎        st.info(f"🚢 **Volume Global : {total_vol:.2f} m³** ({int((total_vol/33)*100)}% d'un conteneur 20ft)")
‎    with col_v2:
‎        csv = df_reap[['ref_sku', 'designation', 'Qte_A_Commander']].to_csv(index=False).encode('utf-8')
‎        st.download_button("📥 Télécharger l'Ordre d'Achat", csv, "wms_commande.csv", "text/csv")
‎
‎    st.table(df_reap[['ref_sku', 'designation', 'Qte_A_Commander']])else:
‎    st.success("✅ Aucun besoin de réapprovisionnement immédiat.")
‎
‎st.success("🎯 WMS Logistics : Analyse MIT CTL opérationnelle.")
‎
