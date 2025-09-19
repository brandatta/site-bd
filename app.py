import streamlit as st
from PIL import Image

# ================== CONFIG ==================
st.set_page_config(page_title="Brandatta - Servicios", layout="wide")

# ================== ESTILOS ==================
st.markdown("""
<style>
  html, body, [data-testid="stAppViewContainer"] { background: #d4fbd7 !important; }
  header {visibility: hidden;}  #MainMenu {visibility: hidden;}  footer {visibility: hidden;}

  /* Contenedor central propio */
  .center-screen {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;   /* ocupa toda la altura */
    text-align: center;
  }

  /* Logo titilante */
  @keyframes blink {
    0% { opacity: 1; transform: scale(1); }
    50% { opacity: .35; transform: scale(1.02); }
    100% { opacity: 1; transform: scale(1); }
  }
  .center-screen img {
    animation: blink 1.6s ease-in-out infinite;
    max-width: 220px !important;
    width: 220px !important;
    height: auto !important;
    margin-bottom: 1.5rem;
  }

  /* Botón Ingresar */
  .ingresar button {
    border-radius: 999px;
    padding: 0.7rem 1.2rem;
    font-weight: 600;
    border: 1px solid rgba(0,0,0,0.15);
    background: white;
  }

  /* Tarjetas */
  .card {
    border: 1px solid rgba(0,0,0,0.10);
    border-radius: 18px;
    padding: 18px 16px;
    background: white;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    transition: transform .12s ease, box-shadow .12s ease;
    min-height: 120px;
    display: flex; align-items: center; justify-content: center; text-align: center;
  }
  .card:hover { transform: translateY(-2px); box-shadow: 0 10px 22px rgba(0,0,0,0.08); }
  .card h3 { margin: 0; font-size: 1.05rem; letter-spacing: .2px; }
</style>
""", unsafe_allow_html=True)

# ================== STATE ==================
if "ingresado" not in st.session_state:
    st.session_state.ingresado = False

# ================== PORTADA ==================
if not st.session_state.ingresado:
    st.markdown("<div class='center-screen'>", unsafe_allow_html=True)

    try:
        logo = Image.open("logo.png")
        st.image(logo, use_container_width=False)
    except Exception:
        st.markdown("<p style='font-weight:600;'>Colocá un archivo <code>logo.png</code> en la carpeta de la app.</p>", unsafe_allow_html=True)

    st.markdown("<div class='ingresar'>", unsafe_allow_html=True)
    if st.button("Ingresar"):
        st.session_state.ingresado = True
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # cierre del contenedor

# ================== HOME (Tarjetas de servicios) ==================
else:
    st.markdown("<h2 style='margin:0 0 .6rem 0;text-align:center;'>Servicios</h2>", unsafe_allow_html=True)

    servicios = [
        "Consultoría & Discovery",
        "Desarrollo de Aplicaciones",
        "Integraciones (SAP / Ecommerce)",
        "Tableros & Analytics",
        "Automatizaciones & RPA",
        "Soporte & Capacitación",
    ]

    for fila in range(2):
        cols = st.columns(3, gap="large")
        for i, col in enumerate(cols):
            idx = fila*3 + i
            if idx >= len(servicios): continue
            with col:
                st.markdown(f"<div class='card'><h3>{servicios[idx]}</h3></div>", unsafe_allow_html=True)

    st.write("")
    st.caption("Tip: cambiá los títulos en la lista `servicios` para personalizar las tarjetas.")
