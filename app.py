import streamlit as st
import pandas as pd
import io
from datetime import datetime

st.set_page_config(page_title="Smart Data Audit Pro", page_icon="📈", layout="wide")

if "file_key" not in st.session_state:
    st.session_state.file_key = 0

# 1. FUNCIÓN DE REINICIO
def reiniciar_app():
    # Cambiamos la llave para que el widget sea "nuevo" para Streamlit
    st.session_state.file_key += 1
    
    # Limpiamos todo el estado de la sesión
    for key in st.session_state.keys():
        if key != "file_key": # Mantenemos solo la llave para que no se resetee a 0
            del st.session_state[key]
    
    st.rerun()


# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    /* Configuración Global */
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span {
        font-family: 'Inter', sans-serif;
    }
    
    /* Fondo y contenedores */
    .stApp {
        background-color: #0E1117;
    }

    /* Tarjetas de Métricas (Glassmorphism) */
    [data-testid="stMetric"] {
        background-color: rgba(38, 39, 48, 0.5);
        padding: 25px;
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        transition: transform 0.3s ease;
    }
    
    /* BOTÓN REINICIAR (Color Rojo sutil en el sidebar) */
    [data-testid="stSidebar"] .stButton button {
        border: 1px solid rgba(255, 75, 75, 0.3) !important;
        background-color: rgba(255, 75, 75, 0.05) !important;
        color: #FF4B4B !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] .stButton button:hover {
        background-color: #FF4B4B !important;
        color: white !important;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-5px);
        border-color: #1E90FF;
    }

    /* Títulos y Etiquetas */
    [data-testid="stMetricLabel"] {
        color: #808495 !important;
        font-weight: 600 !important;
        letter-spacing: 1.5px !important;
    }
    
    /* Botón de Descarga Custom */
    .stDownloadButton button {
        background-color: #1E90FF !important;
        color: white !important;
        border-radius: 12px !important;
        border: none !important;
        padding: 0.6rem 2rem !important;
        font-weight: 700 !important;
        width: 100%;
        box-shadow: 0 4px 15px rgba(30, 144, 255, 0.3);
    }
    .stDownloadButton button:hover {
        background-color: #00BFFF !important;
        box-shadow: 0 6px 20px rgba(0, 191, 255, 0.4);
    }

    /* Tabs (Pestañas) */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 10px 10px 0 0;
        padding: 0 20px;
        background-color: #161B22;
        border: 1px solid rgba(255,255,255,0.05);
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E90FF !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.sidebar.title("⚙️ Panel de Control")

st.title("Smart Data Audit Pro")
st.caption("Transforma tus datos sucios en decisiones inteligentes en segundos.")

placeholder = st.empty() 

with placeholder.container():
    archivo_subido = st.file_uploader(
        "Sube tu archivo Excel", 
        type=['xlsx'], 
        key=f"cargador_{st.session_state.file_key}" 
    )

if archivo_subido is not None:
    if st.sidebar.button("🔄 Reiniciar / Nuevo Archivo", use_container_width=True):
        reiniciar_app()

    st.sidebar.divider()

    try:
        df_raw = pd.read_excel(archivo_subido)
        
        # --- 1. LIMPIEZA DE CABECERAS ---
        df_raw.columns = [str(col).strip().replace('_', ' ').title() for col in df_raw.columns]
        COL_PRECIO = 'Price'
        COL_GENERO = 'Gender'

        # --- 2. LIMPIEZA PROFUNDA DE DATOS ---
        for col in df_raw.columns:
            if df_raw[col].dtype == 'object':
                df_raw[col] = df_raw[col].fillna("Sin Datos").astype(str).str.strip().str.title()
        
        if COL_PRECIO in df_raw.columns:
            df_raw[COL_PRECIO] = (
                df_raw[COL_PRECIO].astype(str).str.replace(r'[^\d.]', '', regex=True)
            )
            df_raw[COL_PRECIO] = pd.to_numeric(df_raw[COL_PRECIO], errors='coerce').fillna(0)

        # --- 3. PANEL DE CONTROL (LOGICA DE LIMPIEZA) ---
        check_duplicados = st.sidebar.checkbox("Eliminar Duplicados Automáticamente")
        if check_duplicados:
            antes_dup = len(df_raw)
            df_raw = df_raw.drop_duplicates()
            diferencia = antes_dup - len(df_raw)
            if diferencia > 0:
                st.sidebar.success(f"👯 ¡Listo! Se eliminaron {diferencia} filas.")
            else:
                st.sidebar.info("✨ No hay duplicados.")

        modo_perfecto = st.sidebar.toggle("✨ Modo Datos Perfectos")

        st.sidebar.divider()
        st.sidebar.subheader("Filtros Inteligentes")
        
        df_filtrado = df_raw.copy()

        # Filtro A: Género
        if COL_GENERO in df_raw.columns:
            opciones = sorted(df_raw[COL_GENERO].unique().tolist())
            generos_sel = st.sidebar.multiselect(f"Filtrar por {COL_GENERO}:", options=opciones, default=[], placeholder="Todos los géneros")
            if generos_sel:
                df_filtrado = df_filtrado[df_filtrado[COL_GENERO].isin(generos_sel)]

        # Filtro B: Precio
        if COL_PRECIO in df_raw.columns:
            min_p, max_p = float(df_raw[COL_PRECIO].min()), float(df_raw[COL_PRECIO].max())
            if min_p < max_p:
                rango = st.sidebar.slider("Rango de Precio:", min_p, max_p, (min_p, max_p))
                df_filtrado = df_filtrado[(df_filtrado[COL_PRECIO] >= rango[0]) & (df_filtrado[COL_PRECIO] <= rango[1])]

        # Filtro C: Modo Perfecto
        if modo_perfecto:
            antes_perf = len(df_filtrado)
            df_filtrado = df_filtrado[df_filtrado[COL_PRECIO] > 0]
            mascara_nulos = df_filtrado.astype(str).apply(lambda col: col.str.contains("Sin Datos|None|nan", case=False)).any(axis=1)
            df_filtrado = df_filtrado[~mascara_nulos]
            st.sidebar.caption(f"✅ Ocultos {antes_perf - len(df_filtrado)} registros de esta selección.")

        # --- 4. TABS ---
        tab1, tab2, tab3 = st.tabs([" ☰ Explorador", " ⚠ Auditoría", " 📊 Visualización"])

        with tab1:
            if len(df_filtrado) == 0:
                st.warning("⚠️ No hay registros con estos filtros.")
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Registros", len(df_filtrado))
            if COL_PRECIO in df_filtrado.columns:
                c2.metric("Inversión Total", f"$ {df_filtrado[COL_PRECIO].sum():,.2f}")
                c3.metric("Promedio", f"$ {(df_filtrado[COL_PRECIO].mean() if len(df_filtrado)>0 else 0):,.2f}")

            st.divider()
            busqueda = st.text_input("🔍 Buscar...", placeholder="Filtra por cualquier texto...")
            if busqueda:
                df_filtrado = df_filtrado[df_filtrado.astype(str).apply(lambda x: x.str.contains(busqueda, case=False)).any(axis=1)]
            st.dataframe(df_filtrado, use_container_width=True, height=400)

        with tab2:
            st.subheader("Detección de Anomalías")
            if modo_perfecto:
                st.success("✨ **¡Modo Datos Perfectos Activado!**")
                st.info("Los errores han sido filtrados. Apaga el modo en el panel lateral para ver el detalle de anomalías.")
            else:
                en_cero_audit = df_filtrado[df_filtrado[COL_PRECIO] == 0]
                mascara_nulos_audit = df_filtrado.astype(str).apply(lambda col: col.str.contains("Sin Datos|None|nan", case=False)).any(axis=1)
                con_nulos_audit = df_filtrado[mascara_nulos_audit]
                
                if not en_cero_audit.empty or not con_nulos_audit.empty:
                    col_a, col_b = st.columns(2)
                    with col_a:
                        if not en_cero_audit.empty:
                            st.warning(f"🚩 {len(en_cero_audit)} registros con Precio $0")
                            st.dataframe(en_cero_audit, use_container_width=True, height=250)
                    with col_b:
                        if not con_nulos_audit.empty:
                            st.info(f"ℹ️ {len(con_nulos_audit)} registros con datos faltantes")
                            st.dataframe(con_nulos_audit, use_container_width=True, height=250)
                else:
                    st.success("✅ Tu selección actual no tiene anomalías.")

        with tab3:
            st.subheader("Análisis Visual Avanzado")
            if not df_filtrado.empty:
                df_pie = df_filtrado.groupby(COL_GENERO)[COL_PRECIO].sum().sort_values(ascending=False).reset_index()
                if len(df_pie) > 6:
                    top_5 = df_pie.iloc[:5]
                    otros_v = df_pie.iloc[5:][COL_PRECIO].sum()
                    otros_df = pd.DataFrame({COL_GENERO: ['Otros'], COL_PRECIO: [otros_v]})
                    df_pie = pd.concat([top_5, otros_df], ignore_index=True)

                col_izq, col_der = st.columns(2)
                with col_izq:
                    st.markdown("##### 💰 Inversión por Género (%)")
                    import altair as alt
                    grafica_pie = alt.Chart(df_pie).mark_arc().encode(
                        theta=alt.Theta(field=COL_PRECIO, type="quantitative"),
                        color=alt.Color(field=COL_GENERO, type="nominal"),
                        tooltip=[COL_GENERO, alt.Tooltip(COL_PRECIO, format="$,.2f")]
                    ).properties(height=300)
                    st.altair_chart(grafica_pie, use_container_width=True)
                
                with col_der:
                    st.markdown("##### 📈 Curva de Valor (Precios)")
                    df_linea = df_filtrado[COL_PRECIO].sort_values().reset_index(drop=True)
                    st.line_chart(df_linea)

                st.divider()
                st.markdown("##### 📝 Resumen Inteligente")
                df_res = df_filtrado.groupby(COL_GENERO)[COL_PRECIO].sum().sort_values(ascending=False)
                lider_nombre = df_res.index[0]
                lider_valor = df_res.iloc[0]
                total_actual = df_filtrado[COL_PRECIO].sum()
                porcentaje_impacto = (lider_valor / total_actual) * 100 if total_actual > 0 else 0
                
                c1, c2 = st.columns(2)
                c1.info(f"🏆 **Líder:** {lider_nombre} (${lider_valor:,.2f})")
                c2.success(f"📊 **Impacto:** {lider_nombre} representa el {porcentaje_impacto:.1f}% de lo filtrado.")
            else:
                st.warning("⚠️ No hay datos para visualizar.")

        # --- BOTÓN DE DESCARGA FINAL (Fuera de las pestañas) ---
        st.divider()
        fecha_hoy = datetime.now().strftime("%Y-%m-%d")
        nombre_archivo = f"Reporte_Limpio_{fecha_hoy}.xlsx"
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df_filtrado.to_excel(writer, index=False)
        
        st.download_button(
            label="📥 Descargar Reporte Limpio",
            data=buffer.getvalue(),
            file_name=nombre_archivo,
            use_container_width=True,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            on_click=lambda: st.toast("🚀 ¡Reporte generado con éxito!", icon="✅")
        )

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("📂 Sube un archivo Excel para comenzar.")
