import streamlit as st
from PIL import Image

# ================== CONFIG ==================
st.set_page_config(page_title="Brandatta - Servicios", layout="wide")

# ================== STATE ==================
if "ingresado" not in st.session_state:
    st.session_state.ingresado = False

# ================== PORTADA ==================
if not st.session_state.ingresado:
    # Estilos SOLO para la portada: fondo verde y centrado absoluto del contenido
    st.markdown("""
    <style>
      /* Fondo portada */
      html, body, [data-testid="stAppViewContainer"] { background: #d4fbd7 !important; }
      header {visibility: hidden;}  #MainMenu {visibility: hidden;}  footer {visibility: hidden;}

      /* Centrado vertical/horizontal del contenido principal */
      /* Cubrimos distintas versiones de Streamlit */
      .block-container,
      [data-testid="block-container"],
      [data-testid="stVerticalBlock"] > div:has(> .stImage) {
        min-height: 100vh !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
      }

      /* Titilado del logo y tamaño */
      @keyframes blink {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: .35; transform: scale(1.02); }
        100% { opacity: 1; transform: scale(1); }
      }
      .stImage img {
        animation: blink 1.6s ease-in-out infinite;
        width: 220px !important;
        max-width: 220px !important;
        height: auto !important;
        display: block;
        margin: 0 auto 1rem auto;
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

    # Contenido
    try:
        logo = Image.open("logo.png")
        # No usamos use_column_width (deprecado). Fijamos ancho.
        st.image(logo, width=220)
    except Exception:
        st.markdown("<p style='text-align:center;font-weight:600;'>Subí <code>logo.png</code> a la carpeta de la app.</p>", unsafe_allow_html=True)

    st.markdown("<div class='ingresar' style='text-align:center;'>", unsafe_allow_html=True)
    if st.button("Ingresar"):
        st.session_state.ingresado = True
    st.markdown("</div>", unsafe_allow_html=True)

# ================== SERVICIOS ==================
else:
    # Estilos de la página de servicios: fondo blanco, tarjetas blancas con borde #d4fbd7
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
      .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(0,0,0,0.08);
      }
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

    # 3 x 2 grid alineada
    for fila in range(2):
        cols = st.columns(3, gap="large")
        for i, col in enumerate(cols):
            idx = fila*3 + i
            if idx >= len(servicios): 
                continue
            with col:
                st.markdown(f"<div class='card'><h3>{servicios[idx]}</h3></div>", unsafe_allow_html=True)

    st.write("")
    st.caption("Tip: cambiá los títulos en la lista `servicios` para personalizar las tarjetas.")
