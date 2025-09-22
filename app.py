import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# ================== CONFIG ==================
st.set_page_config(page_title="Brandatta - Servicios", layout="wide")

# ================== STATE (seguro/defensivo) ==================
if "ingresado" not in st.session_state:
    st.session_state.ingresado = False

opciones_nav = ["Servicios", "Contacto", "Acerca de nosotros", "Clientes"]
if "nav" not in st.session_state or st.session_state.get("nav") not in opciones_nav:
    st.session_state.nav = "Servicios"

# ================== PORTADA ==================
if not st.session_state.ingresado:
    # Estilos portada: fondo d4fbd7 + animación de logo
    st.markdown("""
    <style>
      html, body, [data-testid="stAppViewContainer"] { background: #d4fbd7 !important; }
      header {visibility: hidden;}  #MainMenu {visibility: hidden;}  footer {visibility: hidden;}

      @keyframes blink {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: .35; transform: scale(1.02); }
        100% { opacity: 1; transform: scale(1); }
      }

      .hero-wrap { padding: 12vh 0 6vh; }
    </style>
    """, unsafe_allow_html=True)

    # Logo centrado con HTML (evita desalineos de st.image)
    try:
        logo = Image.open("logo.png")
        buf = BytesIO(); logo.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        logo_html = f"""
        <div style="display:flex;justify-content:center;">
          <img src="data:image/png;base64,{b64}" alt="logo"
               style="width:220px;max-width:220px;height:auto;animation:blink 1.6s ease-in-out infinite;" />
        </div>
        """
    except Exception:
        logo_html = "<p style='text-align:center;font-weight:600;'>Subí <code>logo.png</code> a la carpeta de la app.</p>"

    st.markdown(f"<div class='hero-wrap'>{logo_html}</div>", unsafe_allow_html=True)

    # Botón directamente debajo del logo, centrado
    c1, c2, c3 = st.columns([1,1,1])
    with c2:
        if st.button("Ingresar"):
            st.session_state.ingresado = True

# ================== CONTENIDO (con navegación por menú desplegable) ==================
else:
    # Estilos generales + tarjetas rectangulares minimal
    st.markdown("""
    <style>
      [data-testid="stAppViewContainer"] { background: #ffffff !important; }
      header {visibility: hidden;}  #MainMenu {visibility: hidden;}  footer {visibility: hidden;}

      .wrap { max-width: 1120px; margin: 0 auto; padding: 8px 8px 40px; }

      /* Dropdown minimal (bordes rectos) */
      .nav-select .stSelectbox > div > div {
        border-radius: 0 !important;
        border: 1px solid #e5e5e7 !important;
      }
      .nav-select label { font-weight: 600; }

      /* Tarjetas rectangulares minimal, bordes rectos con color d4fbd7 */
      .tile { width: 240px; margin: 0 auto; }
      @media (max-width: 900px){ .tile{ width:220px; } }
      @media (max-width: 680px){ .tile{ width:200px; } }

      .card {
        background: #ffffff;
        border: 1px solid #d4fbd7;
        border-radius: 0;
        height: 120px; /* rectángulo */
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

      .section h3 { margin: 0 0 8px 0; font-size: 1.05rem; }
      .section p  { margin: 0 0 6px 0; color: #333; }
      .hairline   { border-top: 1px solid #e5e5e7; margin: 14px 0 18px 0; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='wrap'>", unsafe_allow_html=True)

    # Menú desplegable centrado y robusto (sin ValueError)
    s1, s2, s3 = st.columns([1,2,1])
    with s2:
        st.markdown("### ", unsafe_allow_html=True)
        st.markdown("<div class='nav-select'>", unsafe_allow_html=True)
        nav_actual = st.session_state.get("nav", "Servicios")
        try:
            idx = opciones_nav.index(nav_actual)
        except ValueError:
            idx = 0
        seleccion = st.selectbox("Navegación", opciones_nav, index=idx, key="nav_select")
        st.session_state.nav = seleccion
        st.markdown("</div>", unsafe_allow_html=True)

    # Contenido según selección
    if st.session_state.nav == "Servicios":
        st.markdown("<div class='title'>Servicios</div>", unsafe_allow_html=True)
        servicios = [
            "Consultoría & Discovery",
            "Desarrollo de Aplicaciones",
            "Integraciones (SAP / Ecommerce)",
            "Tableros & Analytics",
            "Automatizaciones & RPA",
            "Soporte & Capacitación"
        ]

        cols = st.columns(3, gap="large")
        for i, col in enumerate(cols):
            with col:
                st.markdown(f"<div class='tile'><div class='card'><h3>{servicios[i]}</h3></div></div>", unsafe_allow_html=True)

        st.markdown("<div class='row-spacer'></div>", unsafe_allow_html=True)

        cols2 = st.columns(3, gap="large")
        for j, col in enumerate(cols2):
            idx2 = 3 + j
            with col:
                st.markdown(f"<div class='tile'><div class='card'><h3>{servicios[idx2]}</h3></div></div>", unsafe_allow_html=True)

    elif st.session_state.nav == "Contacto":
        st.markdown("<div class='hairline'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section">
          <h3>Contacto</h3>
          <p>Email: contacto@brandatta.com</p>
          <p>Teléfono: +54 11 0000-0000</p>
          <p>Dirección: Buenos Aires, Argentina</p>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.nav == "Acerca de nosotros":
        st.markdown("<div class='hairline'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section">
          <h3>Acerca de nosotros</h3>
          <p>Construimos soluciones digitales a medida: integraciones con SAP y Ecommerce, tableros, automatizaciones y apps.</p>
          <p>Enfocados en performance, UX minimalista y resultados de negocio.</p>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.nav == "Clientes":
        st.markdown("<div class='hairline'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section">
          <h3>Clientes</h3>
          <p>Trabajamos con compañías de retail, industria y servicios: Georgalos, Vicbor, ITPS, Biosidus, Glam, Espumas, Café Martínez, entre otros.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
