import streamlit as st
from PIL import Image

# ================== CONFIG ==================
st.set_page_config(page_title="Brandatta - Servicios", layout="wide")

# ================== STATE ==================
if "ingresado" not in st.session_state:
    st.session_state.ingresado = False

# ================== PANTALLA DE INICIO ==================
if not st.session_state.ingresado:
    # ----- Estilos de portada (fondo d4fbd7, logo titilante) -----
    st.markdown("""
    <style>
      html, body, [data-testid="stAppViewContainer"] {
        background: #d4fbd7 !important;
      }
      header {visibility: hidden;}
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}

      /* Titilado del logo */
      @keyframes blink {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.35; transform: scale(1.02); }
        100% { opacity: 1; transform: scale(1); }
      }
      /* Aplico animación y centro */
      .stImage img {
        animation: blink 1.6s ease-in-out infinite;
        display: block;
        margin: 0 auto;
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

    # ----- Contenido centrado -----
    st.write("")  # pequeño spacer
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        try:
            logo = Image.open("logo.png")
            # ⚠️ Fix deprecado: no usamos use_column_width; fijamos ancho
            st.image(logo, width=220)  # centrado por CSS arriba
        except Exception:
            st.markdown("<p style='text-align:center;font-weight:600;'>Colocá un archivo <code>logo.png</code> en la carpeta de la app.</p>", unsafe_allow_html=True)

        # Botón centrado
        st.markdown("<div class='ingresar' style='text-align:center;margin-top:1rem;'>", unsafe_allow_html=True)
        if st.button("Ingresar"):
            st.session_state.ingresado = True
        st.markdown("</div>", unsafe_allow_html=True)

# ================== PANTALLA DE SERVICIOS ==================
else:
    # ----- Estilos de servicios (fondo blanco, tarjetas blancas, borde d4fbd7) -----
    st.markdown("""
    <style>
      [data-testid="stAppViewContainer"] { background: #ffffff !important; }
      header {visibility: hidden;}
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}

      /* Tarjetas blancas con borde color d4fbd7 */
      .card {
        border: 1px solid #d4fbd7;
        border-radius: 18px;
        padding: 18px 16px;
        background: #ffffff;
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
        transition: transform .12s ease, box-shadow .12s ease;
        min-height: 120px;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
      }
      .card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 22px rgba(0,0,0,0.08);
      }
      .card h3 {
        margin: 0;
        font-size: 1.05rem;
        letter-spacing: .2px;
      }
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

    # 3 x 2 grid perfectamente alineada
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
