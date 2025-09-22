import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# ================== CONFIG ==================
st.set_page_config(page_title="Brandatta - Servicios", layout="wide")

# ================== STATE ==================
if "ingresado" not in st.session_state:
    st.session_state.ingresado = False

# ================== PORTADA ==================
if not st.session_state.ingresado:
    # ---- Estilos portada: fondo d4fbd7 + animación ----
    st.markdown("""
    <style>
      html, body, [data-testid="stAppViewContainer"] { background: #d4fbd7 !important; }
      header {visibility: hidden;}  #MainMenu {visibility: hidden;}  footer {visibility: hidden;}

      @keyframes blink {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: .35; transform: scale(1.02); }
        100% { opacity: 1; transform: scale(1); }
      }

      /* Contenedor central */
      .hero-wrap {
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        text-align: center;
      }

      .hero-wrap img {
        width: 220px;
        max-width: 220px;
        height: auto;
        animation: blink 1.6s ease-in-out infinite;
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
    </style>
    """, unsafe_allow_html=True)

    # ---- Logo + botón centrados en un único bloque ----
    logo_html = ""
    try:
        logo = Image.open("logo.png")
        buf = BytesIO(); logo.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        logo_html = f"<img src='data:image/png;base64,{b64}' alt='logo'/>"
    except Exception:
        logo_html = "<p style='font-weight:600;'>Subí <code>logo.png</code> a la carpeta de la app.</p>"

    st.markdown(f"<div class='hero-wrap'>{logo_html}", unsafe_allow_html=True)
    # Botón justo debajo del logo
    st.markdown("<div class='ingresar'>", unsafe_allow_html=True)
    if st.button("Ingresar"):
        st.session_state.ingresado = True
    st.markdown("</div></div>", unsafe_allow_html=True)

# ================== SERVICIOS ==================
else:
    # ---- Estilos servicios: fondo blanco + tarjetas blancas con borde d4fbd7 ----
    st.markdown("""
    <style>
      [data-testid="stAppViewContainer"] { background: #ffffff !important; }
      header {visibility: hidden;}  #MainMenu {visibility: hidden;}  footer {visibility: hidden;}

      .card {
        border: 1px solid #d4fbd7;
        border-radius: 18px;
        padding: 18px 16px;
        background: #ffffff;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        transition: transform .12s ease, box-shadow .12s ease;
        min-height: 120px;
        display: flex; align-items: center; justify-content: center; text-align: center;
      }
      .card:hover { transform: translateY(-2px); box-shadow: 0 10px 22px rgba(0,0,0,0.08); }
      .card h3 { margin: 0; font-size: 1.05rem; letter-spacing: .2px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<h2 style='margin:0 0 .8rem 0; text-align:center;'>Servicios</h2>", unsafe_allow_html=True)

    servicios = [
        "Consultoría & Discovery",
        "Desarrollo de Aplicaciones",
        "Integraciones (SAP / Ecommerce)",
        "Tableros & Analytics",
        "Automatizaciones & RPA",
        "Soporte & Capacitación"
    ]

    # 3 x 2 grid
    for fila in range(2):
        cols = st.columns(3, gap="large")
        for i, col in enumerate(cols):
            idx = fila*3 + i
            if idx >= len(servicios): continue
            with col:
                st.markdown(f"<div class='card'><h3>{servicios[idx]}</h3></div>", unsafe_allow_html=True)

    st.write("")
    st.caption("Tip: cambiá los títulos en la lista `servicios` para personalizar las tarjetas.")
