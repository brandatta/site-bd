import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# ================== CONFIG ==================
st.set_page_config(page_title="Brandatta - Servicios", layout="wide")

# ================== STATE ==================
if "ingresado" not in st.session_state:
    st.session_state.ingresado = False
if "nav" not in st.session_state:
    st.session_state.nav = "servicios"  # servicios | contacto | acerca | clientes

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

      /* Centrado vertical aproximado (sin romper layout) */
      .hero-wrap { padding: 12vh 0 8vh; }
    </style>
    """, unsafe_allow_html=True)

    # ---- Logo centrado con HTML (base64) para evitar desalineos de st.image ----
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

# ================== SERVICIOS + NAVEGACIÓN ==================
else:
    # ---- Estilos servicios y navegación (minimal, bordes rectos) ----
    st.markdown("""
    <style>
      [data-testid="stAppViewContainer"] { background: #ffffff !important; }
      header {visibility: hidden;}  #MainMenu {visibility: hidden;}  footer {visibility: hidden;}

      /* Contenedor centrado con ancho máximo */
      .wrap { max-width: 1120px; margin: 0 auto; padding: 8px 8px 40px; }

      /* NAV minimal con hairline y bordes rectos */
      .nav {
        border-top: 1px solid #e5e5e7;
        border-bottom: 1px solid #e5e5e7;
        padding: 8px 0;
        margin: 0 0 18px 0;
      }
      .nav .stButton>button {
        border: 1px solid #e5e5e7;
        background: #fff;
        border-radius: 0;           /* recto */
        height: 36px;
        padding: 0 14px;
        font-weight: 600;
      }
      .nav .stButton>button:hover {
        border-color: #d0d0d4;
        background: #f9f9fb;
      }
      .nav .active>button {
        background: #111827;
        color: #fff;
        border-color: #111827;
      }

      /* Tarjetas rectangulares minimal */
      .tile { width: 240px; margin: 0 auto; }
      @media (max-width: 900px)  { .tile { width: 220px; } }
      @media (max-width: 680px)  { .tile { width: 200px; } }

      .card {
        background: #ffffff;
        border: 1px solid #d4fbd7;
        border-radius: 0;            /* bordes rectos */
        height: 120px;               /* rectángulo */
        display: flex; align-items: center; justify-content: center; text-align: center;
        transition: border-color .12s ease, transform .12s ease;
      }
      .card:hover { border-color: #bff3c5; transform: translateY(-1px); }

      .card h3 {
        margin: 0;
        font-size: 1.0rem;
        font-weight: 600;
        letter-spacing: .15px;
        color: #111827;
      }

      .row-spacer { height: 44px; }
      .title { text-align:center; font-weight:700; font-size:1.25rem; margin: 0 0 14px 0; }

      /* Secciones de contenido */
      .section h3 { margin: 0 0 8px 0; font-size: 1.05rem; }
      .section p  { margin: 0 0 6px 0; color: #333; }
      .hairline   { border-top: 1px solid #e5e5e7; margin: 14px 0 18px 0; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='wrap'>", unsafe_allow_html=True)
    st.markdown("<div class='title'>Servicios</div>", unsafe_allow_html=True)

    # -------- NAV --------
    st.markdown("<div class='nav'>", unsafe_allow_html=True)
    n1, n2, n3, n4, n5 = st.columns([1,1,1,1,1])  # centrado visual
    with n2:
        cls = "active" if st.session_state.nav == "servicios" else ""
        with st.container():
            st.markdown(f"<div class='{cls}'>", unsafe_allow_html=True)
            if st.button("Servicios", key="nav_serv"):
                st.session_state.nav = "servicios"
            st.markdown("</div>", unsafe_allow_html=True)
    with n3:
        cls = "active" if st.session_state.nav == "contacto" else ""
        st.markdown(f"<div class='{cls}'>", unsafe_allow_html=True)
        if st.button("Contacto", key="nav_cont"):
            st.session_state.nav = "contacto"
        st.markdown("</div>", unsafe_allow_html=True)
    with n4:
        cls = "active" if st.session_state.nav == "acerca" else ""
        st.markdown(f"<div class='{cls}'>", unsafe_allow_html=True)
        if st.button("Acerca de nosotros", key="nav_about"):
            st.session_state.nav = "acerca"
        st.markdown("</div>", unsafe_allow_html=True)
    with n5:
        cls = "active" if st.session_state.nav == "clientes" else ""
        st.markdown(f"<div class='{cls}'>", unsafe_allow_html=True)
        if st.button("Clientes", key="nav_cli"):
            st.session_state.nav = "clientes"
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)  # cierre .nav

    # -------- CONTENIDO SEGÚN NAV --------
    if st.session_state.nav == "servicios":
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

    elif st.session_state.nav == "contacto":
        st.markdown("<div class='hairline'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section">
          <h3>Contacto</h3>
          <p>Email: contacto@brandatta.com</p>
          <p>Teléfono: +54 11 0000-0000</p>
          <p>Dirección: Buenos Aires, Argentina</p>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.nav == "acerca":
        st.markdown("<div class='hairline'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section">
          <h3>Acerca de nosotros</h3>
          <p>Construimos soluciones digitales a medida: integraciones con SAP y Ecommerce, tableros, automatizaciones y apps.</p>
          <p>Enfocados en performance, UX minimalista y resultados de negocio.</p>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.nav == "clientes":
        st.markdown("<div class='hairline'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section">
          <h3>Clientes</h3>
          <p>Trabajamos con compañías de retail, industria y servicios: Georgalos, Vicbor, ITPS, Biosidus, Glam, Espumas, Café Martínez, entre otros.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # cierre .wrap
