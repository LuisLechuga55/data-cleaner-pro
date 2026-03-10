import streamlit as st
import pandas as pd

st.set_page_config(page_title="Data Cleaner", page_icon="💎", layout="wide")

st.sidebar.title("⚙️ Configuración")
st.title("💎 Data Cleaner & Analyst")

archivo_subido = st.file_uploader("Sube tu archivo Excel", type=['xlsx'])

if archivo_subido is not None:
    try:
        df_raw = pd.read_excel(archivo_subido)
        
        # 1. Limpieza inicial
        for col in df_raw.select_dtypes(include=['object']).columns:
            df_raw[col] = df_raw[col].astype(str).str.strip().str.title()
        
        df_filtrado = df_raw.copy()

        # 2. Filtros en Sidebar
        st.sidebar.subheader("🎯 Filtros de Datos")
        if 'gender' in df_filtrado.columns:
            opciones = df_filtrado['gender'].unique().tolist()
            generos = st.sidebar.multiselect("Género:", opciones, default=opciones)
            df_filtrado = df_filtrado[df_filtrado['gender'].isin(generos)]

        if 'price' in df_filtrado.columns:
            df_filtrado['price'] = pd.to_numeric(df_filtrado['price'].replace('[\$,]', '', regex=True), errors='coerce')
            df_filtrado = df_filtrado.dropna(subset=['price'])
            if not df_filtrado.empty:
                min_p, max_p = float(df_filtrado['price'].min()), float(df_filtrado['price'].max())
                if min_p < max_p:
                    rango = st.sidebar.slider("Rango de Precio:", min_p, max_p, (min_p, max_p))
                    df_filtrado = df_filtrado[(df_filtrado['price'] >= rango[0]) & (df_filtrado['price'] <= rango[1])]

        # 3. Mostrar Resultados Principales
        if df_filtrado.empty:
            st.warning("⚠️ No hay datos con esos filtros.")
        else:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader("📋 Datos Filtrados")
                st.dataframe(df_filtrado, height=400)
            with col2:
                st.subheader("📈 Resumen")
                st.metric("Registros", len(df_filtrado))
                if 'price' in df_filtrado.columns:
                    st.metric("Total", f"${df_filtrado['price'].sum():,.2f}")

            # 4. Alerta de Anomalías
            if 'price' in df_filtrado.columns:
                st.divider()
                st.subheader("⚠️ Alerta de Anomalías")
                promedio = df_filtrado['price'].mean()
                anomalias = df_filtrado[df_filtrado['price'] > promedio * 3]
                if not anomalias.empty:
                    st.warning(f"Se detectaron {len(anomalias)} registros sospechosos.")
                    st.dataframe(anomalias)
                else:
                    st.success("✅ Todo parece normal.")

            # 5. Visualización (Fuera de los "ifs" anteriores para que siempre intente mostrarse)
            st.divider()
            st.subheader("📊 Visualización Rápida")
            c1, c2 = st.columns(2)
            if 'gender' in df_filtrado.columns:
                with c1:
                    st.bar_chart(df_filtrado['gender'].value_counts())
            if 'price' in df_filtrado.columns:
                with c2:
                    st.line_chart(df_filtrado['price'])

            # 6. Botón de Descarga (Siempre al final)
            st.divider()
            df_filtrado.to_excel("reporte_limpio.xlsx", index=False)
            with open("reporte_limpio.xlsx", "rb") as f:
                st.download_button("📥 Descargar Resultado", f, "reporte.xlsx")

    except Exception as e:
        st.error(f"❌ Error: {e}")
else:
    st.info("👋 Sube un archivo para comenzar.")
