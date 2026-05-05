import streamlit as st
from fpdf import FPDF
import os
import textwrap
import pandas as pd  
from datetime import datetime

# --- 1. SISTEMA DE SEGURIDAD (LOPD) ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("Plataforma de Seguimiento y Análisis")
    st.warning("🔒 Acceso Restringido - Uso Interno")
    st.info("Por favor, identifícate para acceder a la plataforma.")
    
    contrasena = st.text_input("Contraseña de acceso:", type="password")
    
    if st.button("Entrar"):
        if contrasena == "Mediacion2026": 
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta.")
    st.stop() 

# --- 2. CONFIGURACIÓN ---
st.set_page_config(page_title="Gestión de Seguimiento", layout="wide")

# --- 3. GESTIÓN DEL LOGO ---
if "logo_path" not in st.session_state:
    st.session_state.logo_path = None

# Buscar si ya hay un logo en la carpeta
for ext in ["png", "jpg", "jpeg"]:
    if os.path.exists(f"logo_institucional.{ext}"):
        st.session_state.logo_path = f"logo_institucional.{ext}"

st.sidebar.header("Configuración Institucional")
if st.session_state.logo_path and os.path.exists(st.session_state.logo_path):
    st.sidebar.image(st.session_state.logo_path, width=150)
    st.sidebar.success("Logo guardado.")
    if st.sidebar.button("Borrar y cambiar logo"):
        os.remove(st.session_state.logo_path)
        st.session_state.logo_path = None
        st.rerun()
else:
    archivo_subido = st.sidebar.file_uploader("Sube el logo (.png, .jpg)", type=["png", "jpg", "jpeg"])
    if archivo_subido is not None:
        extension = archivo_subido.name.split(".")[-1].lower()
        nombre_archivo = f"logo_institucional.{extension}"
        with open(nombre_archivo, "wb") as f:
            f.write(archivo_subido.getbuffer())
        st.session_state.logo_path = nombre_archivo
        st.rerun()

st.title("Plataforma de Seguimiento y Análisis")

# --- 4. PESTAÑAS ---
tab1, tab2 = st.tabs(["📝 Generar Nuevo Informe", "📊 Panel de Control"])

with tab1:
    st.header("1. Datos del Usuario")
    col1, col2 = st.columns(2)
    with col1:
        nombre_usuario = st.text_input("Nombre del usuario/a:")
    with col2:
        perfil_usuario = st.selectbox("Perfil:", ["Seleccionar...", "Sordoceguera", "TEA", "Discapacidad intelectual", "Otro"])
    
    st.header("2. Sistemas de Comunicación")
    with st.expander("Evaluación comunicativa", expanded=True):
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            sistema_com = st.selectbox("Sistema principal:", ["LSE", "LSE Táctil", "Dactilológico", "Pictogramas", "Bimodal", "Oral"])
            comprension = st.radio("Anticipación/Rutinas:", ["Adecuada", "Apoyo constante", "Dificultad"])
        with col_c2:
            intencion_com = st.slider("Intención comunicativa (0-5):", 0, 5, 3)
            notas_com = st.text_input("Notas específicas:")

    st.header("3. Registro de la jornada")
    fecha = st.date_input("Fecha", datetime.now())
    nombre_limpio = nombre_usuario.lower().strip() if nombre_usuario else "usuario"
    
    # Lógica Jorge
    es_jorge = (perfil_usuario == "Sordoceguera" and "jorge" in nombre_limpio)
    turno = "General"
    calidad_sueno = "N/A"
    picos_conducta = "No"

    if es_jorge:
        st.subheader("Rastreo y Fisiología (Jorge)")
        col_t, col_m = st.columns(2)
        with col_t: turno = st.selectbox("Turno:", ["Mañana", "Tarde", "Noche"])
        with col_m: nombre_mediadora = st.text_input("Mediadora:")
        
        if turno == "Noche":
            with st.expander("Detalles Sueño", expanded=True):
                horas_sueno = st.number_input("Horas de sueño:", 0.0, 24.0, 8.0, 0.5)
                calidad_sueno = st.selectbox("Calidad:", ["Tranquilo", "Inquieto", "Otro"])
        
        with st.expander("Fisiología", expanded=True):
            agua = st.number_input("Agua (ml):", 0, 5000, 500)
            pis = st.number_input("Micciones:", 0, 20, 1)
            hizo_bano = st.radio("¿Deposición?", ["No", "Sí"])

    st.subheader("Conducta y Observaciones")
    picos_conducta = st.radio("¿Picos de conducta?", ["No", "Sí"])
    detalles_conducta = st.text_input("Detalles conducta:") if picos_conducta == "Sí" else ""
    notas_extra = st.text_area("Observaciones finales:")

    if st.button("Generar Informe Oficial", type="primary"):
        if not nombre_usuario or perfil_usuario == "Seleccionar...":
            st.error("Por favor, rellena el nombre y el perfil.")
        else:
            # Guardar datos
            nuevo = pd.DataFrame([{"Fecha": fecha, "Usuario": nombre_limpio.capitalize(), "Perfil": perfil_usuario, "Pico": picos_conducta}])
            if os.path.exists("historial.csv"):
                df_h = pd.read_csv("historial.csv")
                df_h = pd.concat([df_h, nuevo], ignore_index=True)
            else:
                df_h = nuevo
            df_h.to_csv("historial.csv", index=False)

            # Crear contenido del informe
            texto_informe = f"INFORME DIARIO - {fecha}\n"
            texto_informe += f"Usuario: {nombre_usuario.upper()}\nPerfil: {perfil_usuario}\n"
            texto_informe += f"Comunicación: {sistema_com} (Nivel: {intencion_com}/5)\n"
            texto_informe += f"Conducta: {picos_conducta}\n"
            if picos_conducta == "Sí": texto_informe += f"Detalle: {detalles_conducta}\n"
            texto_informe += f"Observaciones: {notas_extra}"

            st.success("¡Informe listo!")
            
            # --- GENERACIÓN DE PDF ---
            pdf = FPDF()
            pdf.add_page()
            
            # Logo
            if st.session_state.logo_path and os.path.exists(st.session_state.logo_path):
                pdf.image(st.session_state.logo_path, x=15, y=10, w=30)
                pdf.set_y(45)
            else:
                pdf.set_y(20)

            # Alerta
            if picos_conducta == "Sí" or calidad_sueno == "Inquieto":
                pdf.set_text_color(200, 0, 0)
                pdf.set_font("Arial", "B", 12)
                pdf.cell(0, 10, "ATENCION: Se requiere revision de conducta/sueno", ln=1)
                pdf.set_text_color(0, 0, 0)

            pdf.set_font("Arial", "", 11)
            for linea in texto_informe.split('\n'):
                pdf.multi_cell(0, 8, txt=linea)

            # Exportar a Bytes (Solución al TypeError)
            # El parámetro dest='S' devuelve el PDF como una cadena de caracteres
            # .encode('latin-1') lo convierte en los bytes que Streamlit necesita
            pdf_output = pdf.output(dest='S').encode('latin-1')
            
            col_d1, col_d2 = st.columns(2)
            with col_d1:
                st.download_button("📄 Descargar Texto", data=texto_informe, file_name=f"Informe_{nombre_limpio}.txt")
            with col_d2:
                st.download_button("📕 Descargar PDF", data=pdf_output, file_name=f"Informe_{nombre_limpio}.pdf", mime="application/pdf")

with tab2:
    st.header("📊 Estadísticas")
    if os.path.exists("historial.csv"):
        df = pd.read_csv("historial.csv")
        st.metric("Total Informes", len(df))
        st.dataframe(df, use_container_width=True)
        if st.button("Borrar historial"):
            os.remove("historial.csv")
            st.rerun()
    else:
        st.info("No hay datos todavía.")