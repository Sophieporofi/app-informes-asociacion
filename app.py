import streamlit as st
from fpdf import FPDF
import os
import textwrap
import pandas as pd  
from datetime import datetime
import streamlit as st
from fpdf import FPDF
import os
import textwrap
import pandas as pd  
from datetime import datetime

# --- NUEVO: SISTEMA DE SEGURIDAD Y PRIVACIDAD (LOPD) ---
if "autenticado" not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("Plataforma de Seguimiento y Análisis")
    st.warning("🔒 Acceso Restringido - Plataforma de Uso Interno")
    st.info("Por favor, identifícate como profesional autorizado para acceder a los datos médicos y de seguimiento.")
    
    contrasena = st.text_input("Contraseña de acceso:", type="password")
    
    if st.button("Entrar"):
        if contrasena == "Mediacion2026":  # <-- ¡Cambia esta contraseña por la que tú quieras!
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Contraseña incorrecta. Acceso denegado.")
    
    # st.stop() hace que la aplicación se congele aquí y no muestre absolutamente nada de lo que hay debajo hasta que la contraseña sea correcta.
    st.stop() 

# --- A PARTIR DE AQUÍ, DEJA EL RESTO DE TU CÓDIGO EXACTAMENTE IGUAL ---
st.set_page_config(page_title="Gestión de Seguimiento", layout="wide")
# ... (resto de la aplicación)

st.set_page_config(page_title="Gestión de Seguimiento", layout="wide")
st.title("Plataforma de Seguimiento y Análisis")

# --- GESTIÓN DEL LOGO EN EL MENÚ LATERAL ---
st.sidebar.header("Configuración Institucional")
if os.path.exists("logo.png"):
    st.sidebar.image("logo.png", width=150)
    st.sidebar.success("Logo guardado en memoria.")
    if st.sidebar.button("Borrar y cambiar logo"):
        os.remove("logo.png")
        st.rerun()
else:
    st.sidebar.info("Sube el logo de la asociación.")
    archivo_subido = st.sidebar.file_uploader("Elige una imagen", type=["png", "jpg", "jpeg"])
    if archivo_subido is not None:
        with open("logo.png", "wb") as f:
            f.write(archivo_subido.getbuffer())
        st.sidebar.success("¡Logo guardado!")
        st.rerun()

# --- NUEVO: CREACIÓN DE PESTAÑAS ---
tab1, tab2 = st.tabs(["📝 Generar Nuevo Informe", "📊 Panel de Control y Estadísticas"])

with tab1:
    # --- 1. DATOS DEL USUARIO ---
    st.header("1. Datos del Usuario")
    col1, col2 = st.columns(2)
    with col1:
        nombre_usuario = st.text_input("Nombre del usuario/a:")
    with col2:
        perfil_usuario = st.selectbox(
            "Perfil / Discapacidad:",
            ["Seleccionar...", "Sordoceguera", "Discapacidad intelectual", "Discapacidad motriz", "TEA", "Otro"]
        )
    
    # --- 2. MÓDULO DE COMUNICACIÓN ---
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

    # --- 3. REGISTRO DE LA JORNADA ---
    st.header("3. Registro de la jornada")
    fecha = st.date_input("Fecha del informe")
    nombre_limpio = nombre_usuario.lower().strip()
    es_jorge_noche = False
    turno_seleccionado = "General" 

    # --- LÓGICA ESPECIAL Y FISIOLOGÍA (Solo Jorge) ---
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
            
        st.markdown("**Rutinas específicas del turno**")
        
        if turno == "Mañana":
            col_des, col_des_notas = st.columns(2)
            with col_des: desayuno = st.text_input("¿Qué ha desayunado?")
            with col_des_notas: notas_desayuno = st.text_input("Notas extra (Desayuno):")
            col_alm, col_alm_notas = st.columns(2)
            with col_alm: almuerzo = st.text_input("¿Qué ha almorzado?")
            with col_alm_notas: notas_almuerzo = st.text_input("Notas extra (Almuerzo):")
                
        elif turno == "Tarde":
            col_com, col_com_notas = st.columns(2)
            with col_com: comida = st.text_input("¿Qué ha comido?")
            with col_com_notas: notas_comida = st.text_input("Notas extra (Comida):")
            col_mer, col_mer_notas = st.columns(2)
            with col_mer: merienda = st.text_input("¿Qué ha merendado?")
            with col_mer_notas: notas_merienda = st.text_input("Notas extra (Merienda):")
            col_cen, col_cen_notas = st.columns(2)
            with col_cen: cena = st.text_input("¿Qué ha cenado?")
            with col_cen_notas: notas_cena = st.text_input("Notas extra (Cena):")
                
        elif turno == "Noche":
            with st.expander("Detalles del Sueño y Observaciones", expanded=True):
                horas_sueno = st.number_input("Horas de sueño:", min_value=0.0, step=0.5, format="%.1f")
                calidad_sueno = st.selectbox("¿Cómo ha sido el sueño?", ["Seleccionar...", "Tranquilo", "Cansado / Inquieto", "Otro"])
                st.markdown("*Observaciones:*")
                col_noche1, col_noche2 = st.columns(2)
                with col_noche1:
                    gases = st.radio("¿Tiene gases?", ["No", "Sí"])
                    frota_cabeza = st.radio("¿Se frota la cabeza?", ["No", "Sí"])
                with col_noche2:
                    frota_cuerpo = st.radio("¿Se frota partes del cuerpo?", ["No", "Sí"])
                    mueve_mucho = st.radio("¿Se mueve mucho?", ["No", "Sí"])
                
        with st.expander("Fisiología y Cuidados Básicos", expanded=True):
            estiramientos = st.slider("Nivel de estiramientos (0 - 5)", 0, 5, 0)
            aleteo = st.radio("¿Se han observado aleteos?", ["No", "Sí"])
            if aleteo == "Sí": contexto_aleteo = st.text_input("Especifica el contexto del aleteo:")
            agua_ml = st.number_input("Cantidad de agua bebida (en ml):", min_value=0, step=50)
            medicacion = st.radio("¿Se ha administrado medicación?", ["No", "Sí"])
            if medicacion == "Sí": detalles_med = st.text_input("Indica cuál, cantidad y dosis:")
            pis_cantidad = st.number_input("Número de veces que ha hecho pis:", min_value=0, step=1)
            hizo_bano = st.radio("¿Ha hecho deposición (baño)?", ["No", "Sí"])
            if hizo_bano == "Sí":
                col_textura, col_cantidad = st.columns(2)
                with col_textura: textura_bano = st.selectbox("Textura:", ["Seleccionar...", "Normales", "Blandas", "Duras"])
                with col_cantidad: cantidad_bano = st.selectbox("Cantidad:", ["Seleccionar...", "Normal", "Abundantes", "Pocas"])
            
        st.markdown("---")

    # --- ASPECTOS GENERALES (Para todos) ---
    if es_jorge_noche == False:
        st.subheader("Actividades y Estado General")
        actividades_generales = st.text_area("Descripción de las actividades realizadas:")
        estado_animo = st.selectbox(
            "Estado de ánimo general:", 
            ["Seleccionar...", "Tranquilo y colaborador", "Apatía / Cansancio", "Nerviosismo / Agitación", "Tristeza", "Otro"]
        )
        nivel_participacion = st.radio(
            "Nivel de participación en las rutinas:", 
            ["Alta (iniciativa propia)", "Media (requiere algo de apoyo)", "Baja (poca respuesta o rechazo)"]
        )
    else:
        estado_animo = "Durmiendo"

    st.subheader("Conducta (General)")
    picos_conducta = st.radio("¿Hubo picos de conducta (se muerde, golpea, espasmos...)?", ["No", "Sí"])
    if picos_conducta == "Sí":
        detalles_conducta = st.text_input("Describe brevemente el pico de conducta (qué, intensidad, motivo):")

    st.markdown("---")
    st.subheader("Observaciones Finales")
    notas_extra = st.text_area("Notas extra / Observaciones adicionales:")

    # --- GENERACIÓN DEL INFORME ---
    if st.button("Generar Informe Oficial", type="primary"):
        
        if nombre_usuario == "" or perfil_usuario == "Seleccionar...":
            st.warning("⚠️ Escribe el nombre del usuario y su perfil antes de generar el informe.")
        else:
            # --- SISTEMA DE ALERTAS AUTOMÁTICAS ---
            alerta_roja = False
            if picos_conducta == "Sí" or (es_jorge_noche and calidad_sueno == "Cansado / Inquieto"):
                alerta_roja = True
            
            # --- GUARDADO EN BASE DE DATOS ---
            nuevo_registro = pd.DataFrame([{
                "Fecha": fecha,
                "Usuario": nombre_limpio.title(),
                "Perfil": perfil_usuario,
                "Turno": turno_seleccionado,
                "Sistema Comunicacion": sistema_com if sistema_com != "Seleccionar..." else "No especificado",
                "Estado Animo": estado_animo,
                "Pico Conducta": picos_conducta
            }])
            
            if os.path.exists("historial_informes.csv"):
                df_historial = pd.read_csv("historial_informes.csv")
                df_historial = pd.concat([df_historial, nuevo_registro], ignore_index=True)
            else:
                df_historial = nuevo_registro
            df_historial.to_csv("historial_informes.csv", index=False)
            
            st.success("✅ Informe generado y guardado en la base de datos.")

            # --- REDACCIÓN ---
            informe = "" 
            
            if perfil_usuario == "Sordoceguera" and nombre_limpio in ["jorge", "jorge españa"]:
                informe += f"INFORME DE SEGUIMIENTO DIARIO\n"
                informe += f"Fecha: {fecha}\n"
                informe += f"Usuario/a: {nombre_usuario.title()}\n"
                informe += f"Perfil: {perfil_usuario}\n\n"
                nombre_med_mostrar = nombre_mediadora.title() if 'nombre_mediadora' in locals() and nombre_mediadora else "No especificado"
                informe += f"Mediadora: {nombre_med_mostrar}\n\n"
                
                informe += f"# Comunicación:\n"
                informe += f"* Sistema: {sistema_com}\n* Intención (0-5): {intencion_com}\n* Comprensión: {comprension}\n"
                if notas_com: informe += f"* Notas: {notas_com}\n"
                informe += "\n"
                
                if turno == "Noche":
                    informe += f"@{turno}: {fecha}\n"
                    informe += f"# Baño:\n* {hizo_bano.lower()}"
                    if hizo_bano == "Sí": informe += f" ({cantidad_bano.lower()} y {textura_bano.lower()})"
                    informe += f"\n# Pis: {'Sí' if pis_cantidad > 0 else 'No'}\n* Nr. {pis_cantidad}\n"
                    informe += f"# Agua:\n* {agua_ml} ml.\n"
                    informe += f"# Sueño:\n* Nr. {horas_sueno} horas\n* {calidad_sueno.lower()}\n"
                    informe += f"* Tiene gases: ({gases.lower()})\n* Se frota la cabeza: ({frota_cabeza.lower()})\n"
                    informe += f"* Se frota partes del cuerpo: ({frota_cuerpo.lower()})\n* Se mueve mucho: ({mueve_mucho.lower()})\n"
                    informe += f"# Estiramientos (0-5)\n* Nr. {estiramientos}\n"
                    informe += f"# Picos de conducta: ({picos_conducta.lower()})\n"
                    if picos_conducta == "Sí": informe += f"* Detalle: {detalles_conducta}\n"
                    else: informe += "* Nr. 0\n"
                    informe += f"# Medicación:\n"
                    if medicacion == "Sí": informe += f"{detalles_med}\n"
                    else: informe += "Ninguna\n"
                    informe += f"# Observación: {notas_extra}\n"
                    
                elif turno in ["Mañana", "Tarde"]:
                    informe += f"@{turno}: {fecha}\n"
                    informe += f"# Baño:\n* {hizo_bano.lower()}"
                    if hizo_bano == "Sí": informe += f" ({cantidad_bano.lower()} y {textura_bano.lower()})"
                    informe += f"\n# Pis: {'Sí' if pis_cantidad > 0 else 'No'}\n* Nr. {pis_cantidad}\n"
                    informe += f"# Agua:\n* {agua_ml} ml.\n"
                    informe += "# Comidas:\n"
                    if turno == "Mañana":
                        informe += f"* Desayuno: {desayuno}\n"
                        if notas_desayuno: informe += f"  - Notas: {notas_desayuno}\n"
                        informe += f"* Almuerzo: {almuerzo}\n"
                        if notas_almuerzo: informe += f"  - Notas: {notas_almuerzo}\n"
                    elif turno == "Tarde":
                        informe += f"* Comida: {comida}\n"
                        if notas_comida: informe += f"  - Notas: {notas_comida}\n"
                        informe += f"* Merienda: {merienda}\n"
                        if notas_merienda: informe += f"  - Notas: {notas_merienda}\n"
                        informe += f"* Cena: {cena}\n"
                        if notas_cena: informe += f"  - Notas: {notas_cena}\n"
                    informe += f"# Estiramientos (0-5)\n* Nr. {estiramientos}\n"
                    informe += f"# Aleteo: ({aleteo.lower()})\n"
                    if aleteo == "Sí": informe += f"* Contexto: {contexto_aleteo}\n"
                    informe += f"# Picos de conducta: ({picos_conducta.lower()})\n"
                    if picos_conducta == "Sí": informe += f"* Detalle: {detalles_conducta}\n"
                    else: informe += "* Nr. 0\n"
                    informe += f"# Medicación:\n"
                    if medicacion == "Sí": informe += f"{detalles_med}\n"
                    else: informe += "Ninguna\n"
                    informe += f"# Observación: {notas_extra}\n"
                    
            else:
                estado_mostrar = estado_animo.lower() if estado_animo != "Seleccionar..." else "no especificado"
                sistema_mostrar = sistema_com if sistema_com != "Seleccionar..." else "sistemas habituales"
                
                informe += f"INFORME TÉCNICO DE SEGUIMIENTO DIARIO\n\n"
                
                informe += f"1. DATOS DE IDENTIFICACIÓN\n"
                informe += f"El presente documento detalla el seguimiento y evolución de {nombre_usuario.title()}, perfil {perfil_usuario}. Jornada del {fecha}.\n\n"
                
                informe += f"2. ACCESIBILIDAD Y COMUNICACIÓN\n"
                informe += f"Para garantizar la accesibilidad cognitiva, se ha priorizado el uso de {sistema_mostrar}. La comprensión de rutinas se evalúa como '{comprension.lower()}', mostrando un nivel de intención comunicativa de {intencion_com} sobre 5. "
                if notas_com: informe += f"Notas de intervención: {notas_com}."
                informe += "\n\n"

                informe += f"3. ESTADO GENERAL Y PARTICIPACIÓN\n"
                informe += f"El/la usuario/a ha presentado un estado de ánimo {estado_mostrar}, con un nivel de participación {nivel_participacion.lower()}.\n\n"
                
                informe += f"4. DESARROLLO DE ACTIVIDADES\n"
                if actividades_generales:
                    informe += f"Actividades y dinámicas de intervención ejecutadas:\n{actividades_generales}\n\n"
                else:
                    informe += f"No se han registrado actividades específicas fuera de la rutina habitual.\n\n"
                    
                informe += f"5. ÁREA CONDUCTUAL\n"
                if picos_conducta == "Sí":
                    informe += f"Se ha documentado una alteración o pico de conducta. Descripción: {detalles_conducta}\n\n"
                else:
                    informe += f"No se han registrado picos de conducta. Actitud estable.\n\n"
                    
                informe += f"6. OBSERVACIONES ADICIONALES\n"
                if notas_extra:
                    informe += f"{notas_extra}\n\n"
                else:
                    informe += f"Sin observaciones adicionales.\n\n"
                
                informe += f"Fin del informe.\n"

            col_txt, col_pdf = st.columns(2)
            
            with col_txt:
                st.download_button("📄 Descargar en Texto (.txt)", data=informe, file_name=f"Informe_{nombre_limpio}_{fecha}.txt")
                
            with col_pdf:
                pdf = FPDF()
                pdf.set_margins(left=15, top=15, right=15)
                pdf.add_page()
                
                if os.path.exists("logo.png"):
                    pdf.image("logo.png", x=15, y=10, w=30)
                    pdf.set_y(45) 
                else:
                    pdf.set_y(20)
                
                # LA CORRECCIÓN: SIN EMOJI PARA QUE NO SE ROMPA LA FUENTE DEL PDF
                if alerta_roja:
                    pdf.set_text_color(220, 53, 69) # Rojo
                    pdf.set_font("helvetica", "B", 12)
                    pdf.cell(0, 8, "!!! ATENCION REQUERIDA: Seguimiento conductual/fisiologico necesario !!!", ln=1)
                    pdf.set_text_color(0, 0, 0) # Volver a negro
                    pdf.ln(5)

                for linea in informe.split('\n'):
                    linea = linea.strip() 
                    if linea == "":
                        pdf.ln(5) 
                        continue
                    
                    if linea.isupper() or linea.startswith('#') or linea.startswith('@') or (len(linea)>1 and linea[0].isdigit() and linea[1]=='.'):
                        pdf.set_font("helvetica", "B", 11) 
                    else:
                        pdf.set_font("helvetica", "", 11)  
                    
                    fragmentos_seguros = textwrap.wrap(linea, width=95)
                    for fragmento in fragmentos_seguros:
                        pdf.cell(w=0, h=6, text=fragmento, ln=1)
                
                pdf_bytes = pdf.output()
                st.download_button("📕 Descargar Informe Oficial en PDF", data=bytes(pdf_bytes), file_name=f"Informe_{nombre_limpio}_{fecha}.pdf", mime="application/pdf")

# --- PESTAÑA 2 - PANEL DE CONTROL ---
with tab2:
    st.header("📊 Panel de Dirección y Análisis de Datos")
    
    if os.path.exists("historial_informes.csv"):
        df = pd.read_csv("historial_informes.csv")
        
        st.subheader("Resumen General")
        col_stat1, col_stat2, col_stat3 = st.columns(3)
        col_stat1.metric("Informes Generados", len(df))
        col_stat2.metric("Usuarios Atendidos", df['Usuario'].nunique())
        alertas = len(df[df['Pico Conducta'] == 'Sí'])
        col_stat3.metric("Picos de Conducta Registrados", alertas)
        
        st.markdown("---")
        
        col_graf1, col_graf2 = st.columns(2)
        with col_graf1:
            st.write("**Frecuencia de Uso de Sistemas de Comunicación**")
            st.bar_chart(df['Sistema Comunicacion'].value_counts())
            
        with col_graf2:
            st.write("**Distribución de Estados de Ánimo**")
            st.bar_chart(df['Estado Animo'].value_counts())
            
        st.markdown("---")
        st.subheader("Buscador Histórico de Informes")
        st.dataframe(df, use_container_width=True)
        
        if st.button("Borrar Historial de Datos", type="secondary"):
            os.remove("historial_informes.csv")
            st.rerun()
    else:
        st.info("Aún no hay datos. Genera tu primer informe en la pestaña anterior para empezar a ver estadísticas automáticas.")