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
    st.info("Por favor, identifícate para acceder a los datos de seguimiento.")
    
    contrasena = st.text_input("Contraseña de acceso:", type="password")
    
    if st.button("Entrar"):
        if contrasena == "Mediacion2026": 
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta.")
    st.stop() 

# --- 2. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Gestión de Seguimiento", layout="wide")

# --- 3. GESTIÓN INTELIGENTE DEL LOGO ---
if "logo_path" not in st.session_state:
    st.session_state.logo_path = None

# Detectar si ya hay un logo guardado físicamente
for ext in ["png", "jpg", "jpeg"]:
    if os.path.exists(f"logo_institucional.{ext}"):
        st.session_state.logo_path = f"logo_institucional.{ext}"

st.sidebar.header("Configuración")
if st.session_state.logo_path and os.path.exists(st.session_state.logo_path):
    st.sidebar.image(st.session_state.logo_path, width=150)
    if st.sidebar.button("Borrar y cambiar logo"):
        os.remove(st.session_state.logo_path)
        st.session_state.logo_path = None
        st.rerun()
else:
    archivo_subido = st.sidebar.file_uploader("Sube el logo de la asociación", type=["png", "jpg", "jpeg"])
    if archivo_subido is not None:
        extension = archivo_subido.name.split(".")[-1].lower()
        nombre_archivo = f"logo_institucional.{extension}"
        with open(nombre_archivo, "wb") as f:
            f.write(archivo_subido.getbuffer())
        st.session_state.logo_path = nombre_archivo
        st.rerun()

st.title("Plataforma de Seguimiento y Análisis")

# --- 4. PESTAÑAS ---
tab1, tab2 = st.tabs(["📝 Generar Nuevo Informe", "📊 Panel de Control y Estadísticas"])

with tab1:
    st.header("1. Datos del Usuario")
    col1, col2 = st.columns(2)
    with col1:
        nombre_usuario = st.text_input("Nombre del usuario/a:")
    with col2:
        perfil_usuario = st.selectbox(
            "Perfil / Discapacidad:",
            ["Seleccionar...", "Sordoceguera", "Discapacidad intelectual", "Discapacidad motriz", "TEA", "Otro"]
        )
    
    st.header("2. Sistemas de Comunicación y Accesibilidad")
    with st.expander("Desplegar evaluación comunicativa", expanded=True):
        col_com1, col_com2 = st.columns(2)
        with col_com1:
            sistema_com = st.selectbox("Sistema principal utilizado:", 
                ["Seleccionar...", "LSE", "LSE Táctil", "Dactilológico en palma", "Pictogramas", "Bimodal", "Lenguaje Oral", "Otro"])
            comprension = st.radio("Comprensión de rutinas/anticipación:", 
                ["Adecuada", "Requiere apoyo constante", "Dificultad evidente / Desconexión"])
        with col_com2:
            intencion_com = st.slider("Nivel de intención comunicativa (0-5):", 0, 5, 3)
            notas_com = st.text_input("Observaciones comunicativas específicas:")

    st.markdown("---")

    st.header("3. Registro de la jornada")
    fecha = st.date_input("Fecha del informe")
    nombre_limpio = nombre_usuario.lower().strip()
    es_jorge_noche = False
    turno_seleccionado = "General" 

    if perfil_usuario == "Sordoceguera" and nombre_limpio in ["jorge", "jorge españa"]:
        st.subheader("Rastreo y Fisiología (Jorge)")
        col_turno, col_mediador = st.columns(2)
        with col_turno:
            turno = st.selectbox("Turno:", ["Seleccionar...", "Mañana", "Tarde", "Noche"])
            turno_seleccionado = turno
        with col_mediador:
            nombre_mediadora = st.text_input("Nombre de la mediadora:")
        
        if turno == "Noche":
            es_jorge_noche = True
            
        if turno == "Mañana":
            col_des, col_des_notas = st.columns(2)
            with col_des: desayuno = st.text_input("¿Qué ha desayunado?")
            with col_des_notas: notas_desayuno = st.text_input("Notas (Desayuno):")
            col_alm, col_alm_notas = st.columns(2)
            with col_alm: almuerzo = st.text_input("¿Qué ha almorzado?")
            with col_alm_notas: notas_almuerzo = st.text_input("Notas (Almuerzo):")
                
        elif turno == "Tarde":
            col_com, col_com_notas = st.columns(2)
            with col_com: comida = st.text_input("¿Qué ha comido?")
            with col_com_notas: notas_comida = st.text_input("Notas (Comida):")
            col_mer, col_mer_notas = st.columns(2)
            with col_mer: merienda = st.text_input("¿Qué ha merendado?")
            with col_mer_notas: notas_merienda = st.text_input("Notas (Merienda):")
            col_cen, col_cen_notas = st.columns(2)
            with col_cen: cena = st.text_input("¿Qué ha cenado?")
            with col_cen_notas: notas_cena = st.text_input("Notas (Cena):")
                
        elif turno == "Noche":
            with st.expander("Detalles del Sueño", expanded=True):
                horas_sueno = st.number_input("Horas de sueño:", min_value=0.0, step=0.5)
                calidad_sueno = st.selectbox("Calidad:", ["Seleccionar...", "Tranquilo", "Cansado / Inquieto", "Otro"])
                c1, c2 = st.columns(2)
                with c1:
                    gases = st.radio("¿Gases?", ["No", "Sí"])
                    frota_cabeza = st.radio("¿Frota cabeza?", ["No", "Sí"])
                with c2:
                    frota_cuerpo = st.radio("¿Frota cuerpo?", ["No", "Sí"])
                    mueve_mucho = st.radio("¿Se mueve mucho?", ["No", "Sí"])
                
        with st.expander("Fisiología y Cuidados", expanded=True):
            estiramientos = st.slider("Estiramientos (0-5)", 0, 5, 0)
            aleteo = st.radio("¿Aleteos?", ["No", "Sí"])
            if aleteo == "Sí": contexto_aleteo = st.text_input("Contexto aleteo:")
            agua_ml = st.number_input("Agua (ml):", min_value=0, step=50)
            medicacion = st.radio("¿Medicación?", ["No", "Sí"])
            if medicacion == "Sí": detalles_med = st.text_input("Dosis/Medicamento:")
            pis_cantidad = st.number_input("Nº de micciones:", min_value=0, step=1)
            hizo_bano = st.radio("¿Deposición?", ["No", "Sí"])
            if hizo_bano == "Sí":
                ct1, ct2 = st.columns(2)
                with ct1: textura_bano = st.selectbox("Textura:", ["Seleccionar...", "Normales", "Blandas", "Duras"])
                with ct2: cantidad_bano = st.selectbox("Cantidad:", ["Seleccionar...", "Normal", "Abundantes", "Pocas"])

    if not es_jorge_noche:
        st.subheader("Actividades y Estado General")
        actividades_generales = st.text_area("Descripción de actividades:")
        estado_animo = st.selectbox("Ánimo:", ["Seleccionar...", "Tranquilo", "Apático", "Agitado", "Triste", "Otro"])
        nivel_participacion = st.radio("Participación:", ["Alta", "Media", "Baja"])
    else:
        estado_animo = "Durmiendo"

    st.subheader("Conducta")
    picos_conducta = st.radio("¿Picos de conducta?", ["No", "Sí"])
    if picos_conducta == "Sí":
        detalles_conducta = st.text_input("Detalles conducta:")

    notas_extra = st.text_area("Observaciones Finales:")

    if st.button("Generar Informe Oficial", type="primary"):
        if nombre_usuario == "" or perfil_usuario == "Seleccionar...":
            st.warning("⚠️ Completa los datos básicos.")
        else:
            alerta_roja = (picos_conducta == "Sí" or (es_jorge_noche and calidad_sueno == "Cansado / Inquieto"))
            
            # Guardar en CSV
            nuevo_registro = pd.DataFrame([{"Fecha": fecha, "Usuario": nombre_limpio.title(), "Perfil": perfil_usuario, 
                                           "Turno": turno_seleccionado, "Sistema": sistema_com, "Animo": estado_animo, "Pico": picos_conducta}])
            if os.path.exists("historial_informes.csv"):
                df_h = pd.read_csv("historial_informes.csv")
                df_h = pd.concat([df_h, nuevo_registro], ignore_index=True)
            else:
                df_h = nuevo_registro
            df_h.to_csv("historial_informes.csv", index=False)
            
            # Redactar Informe
            informe = f"INFORME DE SEGUIMIENTO - {fecha}\nUsuario: {nombre_usuario.title()}\nPerfil: {perfil_usuario}\n\n"
            informe += f"Comunicación: {sistema_com} | Intención: {intencion_com}/5\n"
            if es_jorge_noche:
                informe += f"Sueño: {horas_sueno}h ({calidad_sueno})\nFisiología: {pis_cantidad} pis, Baño: {hizo_bano}\n"
            else:
                informe += f"Ánimo: {estado_animo}\nActividades: {actividades_generales}\n"
            informe += f"Conducta: {picos_conducta}\nNotas: {notas_extra}"

            st.success("✅ Informe generado.")
            st.download_button("📄 Descargar .txt", data=informe, file_name=f"Informe_{nombre_limpio}.txt")
            
            # Crear PDF
            pdf = FPDF()
            pdf.add_page()
            
            # USO DEL LOGO DINÁMICO (Aquí estaba el error)
            if st.session_state.logo_path and os.path.exists(st.session_state.logo_path):
                pdf.image(st.session_state.logo_path, x=15, y=10, w=30)
                pdf.set_y(45)
            else:
                pdf.set_y(20)

            if alerta_roja:
                pdf.set_text_color(220, 53, 69)
                pdf.set_font("helvetica", "B", 12)
                pdf.cell(0, 8, "!!! ATENCION: Seguimiento conductual/fisiologico necesario !!!", ln=1)
                pdf.set_text_color(0, 0, 0)
                pdf.ln(5)

            pdf.set_font("helvetica", "", 11)
            for linea in informe.split('\n'):
                pdf.multi_cell(0, 6, txt=linea)
            
            pdf_bytes = pdf.output()
            st.download_button("📕 Descargar PDF", data=bytes(pdf_bytes), file_name=f"Informe_{nombre_limpio}.pdf", mime="application/pdf")

with tab2:
    st.header("📊 Análisis de Datos")
    if os.path.exists("historial_informes.csv"):
        df = pd.read_csv("historial_informes.csv")
        c1, c2, c3 = st.columns(3)
        c1.metric("Informes", len(df))
        c2.metric("Usuarios", df['Usuario'].nunique())
        c3.metric("Alertas", len(df[df['Pico'] == 'Sí']))
        st.bar_chart(df['Animo'].value_counts())
        st.dataframe(df, use_container_width=True)
        if st.button("Limpiar Datos"):
            os.remove("historial_informes.csv")
            st.rerun()
    else:
        st.info("Sin datos registrados.")