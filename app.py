import streamlit as st
import time
import pandas as pd
import io
from datetime import datetime

st.set_page_config(
    page_title="Smart Data Audit Pro", 
    page_icon="📈", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LÓGICA DE REINICIO ---
if "file_key" not in st.session_state:
    st.session_state.file_key = 0

def reiniciar_app():
    st.session_state.file_key += 1
    for key in list(st.session_state.keys()):
        if key != "file_key":
            del st.session_state[key]
    st.rerun()


# --- ESTILO CSS ---
st.markdown("""
<style>
    /* --- 1. IMPORTACIÓN Y CONFIGURACIÓN GLOBAL --- */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
    
    html, body, [class*="css"], .stMarkdown, p, h1, h2, h3, span {
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background-color: #0E1117;
    }

    /* --- 2. TÍTULOS Y TEXTOS --- */
    .main-title {
        background: linear-gradient(90deg, #1E90FF, #00BFFF);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        font-size: 3.5rem;
        margin-bottom: 0px;
    }

    .sub-title {
        color: #808495;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }

    /* --- 3. MÉTRICAS (GLASSMORPHISM) --- */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        padding: 20px !important;
        border-radius: 15px !important;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37) !important;
        transition: all 0.3s ease !important;
    }

    [data-testid="stMetric"]:hover {
        border-color: #1E90FF !important;
        transform: translateY(-5px);
        background: rgba(255, 255, 255, 0.08) !important;
    }

    [data-testid="stMetricLabel"] {
        color: #808495 !important;
        font-weight: 600 !important;
        letter-spacing: 1.2px !important;
        text-transform: uppercase;
    }
    
    /* --- 4. BOTONES GENERALES --- */
    .stButton button {
        border-radius: 12px !important;
        font-weight: 600 !important;
        transition: all 0.2s ease !important;
    }

/* --- 5. INTERFAZ DE LA SIDEBAR (VERSION FINAL PULIDA) --- */
    
    /* Contenedor principal del Expander y Botones */
    [data-testid="stSidebar"] button, 
    [data-testid="stSidebar"] .stExpander {
        border: 1px solid rgba(255, 255, 255, 0.05) !important; /* Más sutil por defecto */
        background-color: transparent !important;
        border-radius: 12px !important;
        transition: all 0.3s ease-in-out !important;
    }

    /* HOVER: Brillo azul eléctrico y fondo sutil */
    [data-testid="stSidebar"] button:hover, 
    [data-testid="stSidebar"] .stExpander:hover {
        border-color: #1E90FF !important;
        background-color: rgba(30, 144, 255, 0.1) !important; 
        box-shadow: 0 0 15px rgba(30, 144, 255, 0.2) !important;
    }

    /* LIMPIEZA INTERNA: Forzamos el fondo oscuro dentro del expander */
    [data-testid="stSidebar"] .stExpander div[data-testid="stExpanderDetails"] {
        background-color: #0E1117 !important; 
        border-radius: 0 0 12px 12px !important;
        padding: 1rem !important;
    }

    /* Estilo del texto en los Filtros e internal widgets */
    [data-testid="stWidgetLabel"] p {
        color: #cbd5e1 !important; /* Gris claro más suave para mejor lectura */
        font-size: 0.95rem !important;
    }

    /* --- 6. NAVEGACIÓN Y SELECTORES --- */
    
    /* Tabs (Pestañas) */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        border-radius: 10px 10px 0 0;
        padding: 0 20px;
        background-color: #161B22;
        border: 1px solid rgba(255,255,255,0.05);
        color: #808495;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E90FF !important;
        color: white !important;
    }

    /* Dropdowns (Select) */
    div[data-baseweb="select"] {
        background-color: #161B22 !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 10px !important;
    }   
    div[data-baseweb="select"]:hover {
        border-color: #1E90FF !important;
    }
</style>
    """, unsafe_allow_html=True)

st.sidebar.markdown("# Workstation")
st.sidebar.caption("Configuración de flujo de trabajo")
st.sidebar.divider()

st.markdown('<p class="main-title">Smart Data Audit Pro</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">Intelligence & Precision for Professional Databases</p>', unsafe_allow_html=True)

placeholder = st.empty() 

with placeholder.container():
    archivo_subido = st.file_uploader(
        "Sube tu archivo Excel", 
        type=['xlsx'], 
        key=f"cargador_{st.session_state.file_key}" 
    )

if archivo_subido is not None:
    try:
        progress_placeholder = st.empty()
        status_text = st.empty()
        bar = progress_placeholder.progress(0)

        for i in range(1, 101):
            # ACTUALIZACIÓN DE LA BARRA
            bar.progress(i)
            
            # ACTUALIZACIÓN DEL TEXTO
            if i < 30:
                status_text.caption("🔍 Escaneando estructura de celdas...")
            elif i < 60:
                status_text.caption("🛡️ Aplicando filtros de limpieza profunda...")
            elif i < 90:
                status_text.caption("📊 Generando matrices de auditoría...")
            else:
                status_text.caption("✨ Finalizando optimización...")
            
            time.sleep(0.008) # Un poco más rápido para que no sea tedioso

        # 2. IMPORTANTE: Solo borramos los placeholders DESPUÉS del bucle
        time.sleep(0.5) # Pausa dramática final
        progress_placeholder.empty()
        status_text.empty()

        # 3. CARGA REAL DE DATOS
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
# --- SECCIÓN: HERRAMIENTAS DE LIMPIEZA ---
        with st.sidebar.expander("Herramientas de Limpieza", expanded=True):
            check_duplicados = st.checkbox("Eliminar Duplicados")
            modo_perfecto = st.checkbox("Modo Datos Perfectos")

            # Lógica A: Duplicados (Se ejecuta sobre el raw)
            if check_duplicados:
                antes_dup = len(df_raw)
                df_raw = df_raw.drop_duplicates()
                diferencia = antes_dup - len(df_raw)
                if diferencia > 0:
                    st.success(f"👯 Se eliminaron {diferencia} filas.")
                else:
                    st.info("✨ Sin duplicados.")

            # Lógica B: Modo Perfecto (Movido aquí adentro para el feedback visual)
            # Nota: Esta lógica se aplicará después sobre el df_filtrado más abajo
            # pero ponemos el aviso aquí para que aparezca dentro de la caja.
            if modo_perfecto:
                # Calculamos rápido la diferencia solo para mostrar el mensaje
                nulos_count = df_raw.astype(str).apply(lambda col: col.str.contains("Sin Datos|None|nan", case=False)).any(axis=1).sum()
                precios_cero = (df_raw[COL_PRECIO] <= 0).sum() if COL_PRECIO in df_raw.columns else 0
                
                total_ocultos = nulos_count + precios_cero
                if total_ocultos > 0:
                    st.success(f"✅ Ocultos {total_ocultos} registros.")

        st.sidebar.divider()

        # --- CONTENEDOR DE FILTROS ---
        st.sidebar.subheader("Filtros Inteligentes")
        
        with st.sidebar.container():
            df_filtrado = df_raw.copy()
        
            # Filtro A: Género
            if COL_GENERO in df_raw.columns:
                opciones = sorted(df_raw[COL_GENERO].unique().tolist())
                generos_sel = st.multiselect(f"Filtrar por {COL_GENERO}:", options=opciones, default=[], placeholder="Todos los géneros")
                if generos_sel:
                    df_filtrado = df_filtrado[df_filtrado[COL_GENERO].isin(generos_sel)]

            st.markdown("<br>", unsafe_allow_html=True)

            # Filtro B: Precio
            if COL_PRECIO in df_raw.columns:
                min_p, max_p = float(df_raw[COL_PRECIO].min()), float(df_raw[COL_PRECIO].max())
                if min_p < max_p:
                    rango = st.slider("Rango de Precio:", min_p, max_p, (min_p, max_p))
                    df_filtrado = df_filtrado[(df_filtrado[COL_PRECIO] >= rango[0]) & (df_filtrado[COL_PRECIO] <= rango[1])]

            # APLICACIÓN REAL DE MODO PERFECTO (Sobre los datos ya filtrados)
            if modo_perfecto:
                if COL_PRECIO in df_filtrado.columns:
                    df_filtrado = df_filtrado[df_filtrado[COL_PRECIO] > 0]
                
                mascara_nulos = df_filtrado.astype(str).apply(lambda col: col.str.contains("Sin Datos|None|nan", case=False)).any(axis=1)
                df_filtrado = df_filtrado[~mascara_nulos]

        st.sidebar.divider()

        # Botón de Reinicio al final
        if st.sidebar.button("Reiniciar / Nuevo Archivo", use_container_width=True):
            reiniciar_app()

        # --- 4. TABS ---
        tab1, tab2, tab3 = st.tabs([" ☰ Explorador", " ⚠ Auditoría", " 📊 Visualización"])

        with tab1:
                # Todo el contenido de la pestaña 1 debe ir aquí adentro
                st.write("Vista previa de tus datos:")
                if len(df_filtrado) == 0:
                    st.warning("⚠️ No hay registros con estos filtros.")

                c1, c2, c3 = st.columns(3)
                c1.metric("Registros", len(df_filtrado))
                if COL_PRECIO in df_filtrado.columns:
                    c2.metric("Inversión Total", f"$ {df_filtrado[COL_PRECIO].sum():,.2f}")
                    c3.metric("Promedio", f"$ {(df_filtrado[COL_PRECIO].mean() if len(df_filtrado)>0 else 0):,.2f}")

                st.divider()
                busqueda = st.text_input(
                    "🔍 Buscar...",
                    placeholder="Filtra por cualquier texto...",
                    key="search_bar",
                    label_visibility="collapsed",
                    )
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
                    # Usamos el filtro de nulos que ya tenías
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
                    # Lógica de agrupación para el gráfico de pie
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

                    if not df_res.empty:
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
            label="Descargar Reporte Limpio",
            data=buffer.getvalue(),
            file_name=nombre_archivo,
            use_container_width=True,
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            on_click=lambda: st.toast("Reporte generado con éxito", icon="✅")
        )

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("📂 Sube un archivo Excel para comenzar.")

st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #808495; font-size: 0.9rem;'>
        Smart Data Audit Pro v1.0 | Desarrollado por <b>Luis Lechuga</b>
    </div>
    """, 
    unsafe_allow_html=True
)
