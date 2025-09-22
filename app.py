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

      .hero-wrap { padding: 12vh 0 8vh; }
    </style>
    """, unsafe_allow_html=True)

    # ---- Logo centrado con HTML (base64) ----
    logo_html = ""
    try:
        logo = Image.open("logo.png")
        buf = BytesIO(); logo.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        logo_html = f"""
        <div style="display:flex;justify-content:center;">
          <img src="data:image/png;base64,{b64}"
               alt="logo"
               style="width:220px;max-width:220px;height:auto;
                      animation: blink 1.6s ease-in-out infinite;" />
        </div>
        """
    except Exception:
        logo_html = "<p style='text-align:center;font-weight:600;'>Subí <code>logo.png</code> a la carpeta de la app.</p>"

    st.markdown(f"<div class='hero-wrap'>{logo_html}</div>", unsafe_allow_html=True)

    # ---- Botón centrado ----
    b1, b2, b3 = st.columns([1,1,1])
    with b2:
        if st.button("Ingresar"):
            st.session_state.ingresado = True

# ================== SERVICIOS ==================
else:
    # ---- Estilos: minimal, tarjetas CUADRADAS más chicas y con mayor separación ----
    st.markdown("""
    <style>
      [data-testid="stAppViewContainer"] { background: #ffffff !important; }
      header {visibility: hidden;}  #MainMenu {visibility: hidden;}  footer {visibility: hidden;}

      /* Contenedor de ancho máximo para centrar la grilla */
      .wrap { max-width: 1120px; margin: 0 auto; }

      /* Cada tile tiene ancho fijo (más chico) y se centra dentro de la columna */
      .tile {
        width: 160px;                /* tamaño del cuadrado (más chico) */
        margin: 0 auto;              /* centrar dentro de la columna */
      }
      @media (max-width: 820px) {
        .tile { width: 140px; }      /* un poco más chico en pantallas chicas */
      }

      /* Tarjeta cuadrada, minimal, bordes rectos */
      .card {
        background: #ffffff;
        border: 1px solid #d4fbd7;
        border-radius: 0;            /* bordes rectos */
        aspect-ratio: 1 / 1;         /* CUADRADO perfecto */
        width: 100%;
        display: flex; align-items: center; justify-content: center; text-align: center;
        transition: border-color .12s ease;
      }
      .card:hover { border-color: #bff3c5; }

      .card h3 {
        margin: 0;
        font-size: 0.95rem;          /* tipografía más sobria dentro del cuadrado */
        font-weight: 600;
        color: #111827;
      }

      /* Separación vertical marcada entre filas */
      .row-spacer { height: 36px; }  /* ↑ más separación entre arriba/abajo */
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='wrap'>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin:0 0 1.2rem 0; text-align:center; font-weight:700; font-size:1.25rem;'>Servicios</h2>", unsafe_allow_html=True)

    servicios = [
        "Consultoría & Discovery",
        "Desarrollo de Aplicaciones",
        "Integraciones (SAP / Ecommerce)",
        "Tableros & Analytics",
        "Automatizaciones & RPA",
        "Soporte & Capacitación"
    ]

    # Fila 1 (3 columnas)
    cols = st.columns(3, gap="large")
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"<div class='tile'><div class='card'><h3>{servicios[i]}</h3></div></div>", unsafe_allow_html=True)

    # Espaciador grande entre filas
    st.markdown("<div class='row-spacer'></div>", unsafe_allow_html=True)

    # Fila 2 (3 columnas)
    cols2 = st.columns(3, gap="large")
    for j, col in enumerate(cols2):
        idx = 3 + j
        with col:
            st.markdown(f"<div class='tile'><div class='card'><h3>{servicios[idx]}</h3></div></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.caption("Tip: cambiá los títulos en la lista `servicios` para personalizar las tarjetas.")
