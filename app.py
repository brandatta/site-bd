import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# ================== CONFIG ==================
st.set_page_config(page_title="Brandatta - Servicios", layout="wide")

# ================== STATE ==================
if "ingresado" not in st.session_state:
    st.session_state.ingresado = False

opciones_nav = ["Servicios", "Contacto", "Acerca de nosotros", "Clientes"]
if "nav" not in st.session_state or st.session_state.get("nav") not in opciones_nav:
    st.session_state.nav = "Servicios"

# ===== Helper: logo a <img> base64 =====
def logo_html_src(path="logo.png", width_px=200):
    try:
        img = Image.open(path)
        buf = BytesIO(); img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f'<img src="data:image/png;base64,{b64}" alt="logo" style="width:{width_px}px;max-width:{width_px}px;height:auto;display:block;margin:0 auto;" />'
    except Exception:
        return "<p style='text-align:center;font-weight:600;margin:0;'>Subí <code>logo.png</code> a la carpeta de la app.</p>"

# ================== PORTADA ==================
if not st.session_state.ingresado:
    st.markdown("""
    <style>
      /* Manjari */
      @import url('https://fonts.googleapis.com/css2?family=Manjari:wght@100;400;700&display=swap');

      html, body, [data-testid="stAppViewContainer"] {
        background: #d4fbd7 !important;
        font-family: 'Manjari', system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif !important;
      }
      header {visibility: hidden;}  #MainMenu {visibility: hidden;}  footer {visibility: hidden;}

      /* contenedor full alto y centrado */
      .block-container, [data-testid="block-container"] {
        min-height: 100vh !important;
        display: flex !important;
        flex-direction: column !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
      }
      [data-testid="stVerticalBlock"]:first-of-type {
        flex: 1 0 auto !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 14px !important;
        width: 100% !important;
      }

      /* botón ingresar */
      [data-testid="stVerticalBlock"]:first-of-type .stButton > button {
        display: block !important;
        margin: 28px auto 0 auto !important;
        border-radius: 0 !important;
        border: 1px solid rgba(0,0,0,0.15) !important;
        background: #fff !important;
        font-weight: 700 !important;
        font-family: 'Manjari', system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif !important;
        padding: 10px 18px !important;
        cursor: pointer;
      }

      /* logo titilando */
      @keyframes blink { 0%{opacity:1;transform:scale(1);} 50%{opacity:.35;transform:scale(1.02);} 100%{opacity:1;transform:scale(1);} }
      .hero-logo { animation: blink 1.6s ease-in-out infinite; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(logo_html_src(width_px=200).replace("<img ", "<img class='hero-logo' "), unsafe_allow_html=True)
    if st.button("Ingresar", key="ingresar_btn"):
        st.session_state.ingresado = True

# ================== CONTENIDO ==================
else:
    st.markdown("""
    <style>
      /* Manjari */
      @import url('https://fonts.googleapis.com/css2?family=Manjari:wght@100;400;700&display=swap');

      [data-testid="stAppViewContainer"] {
        background: #ffffff !important;
        font-family: 'Manjari', system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif !important;
      }
      header {visibility: hidden;}  #MainMenu {visibility: hidden;}  footer {visibility: hidden;}
      .block-container, [data-testid="block-container"] { padding-top: 0 !important; padding-bottom: 0 !important; }

      /* contenedor ancho para 3 columnas grandes */
      .wrap { max-width: 1440px; margin: 0 auto; padding: 0 8px 16px; }

      /* Dropdown minimal */
      .nav-select .stSelectbox > div > div {
        border-radius: 0 !important;
        border: 1px solid #e5e5e7 !important;
      }
      .nav-select [data-baseweb="select"] * {
        font-family: 'Manjari', system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif !important;
      }

      /* Tarjetas (dobles) con más separación */
      .tile { width: 440px; margin: 0 auto 28px; }
      @media (max-width: 1200px){ .tile{ width: 400px; } }
      @media (max-width: 900px){  .tile{ width: 360px; } }

      .card-wrap { position: relative; } /* para posicionar el hovercard */

      .card {
        background: #ffffff;
        border: 1px solid #d4fbd7;
        border-radius: 0;
        height: 220px;
        display: flex; align-items: center; justify-content: center; text-align: center;
        transition: border-color .12s ease, transform .12s ease, box-shadow .12s ease;
      }
      .card:hover { border-color: #bff3c5; transform: translateY(-1px); box-shadow: 0 12px 24px rgba(0,0,0,.06); }

      /* Forzar Manjari dentro de la tarjeta */
      .card, .card * {
        font-family: 'Manjari', system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif !important;
      }

      .card h3 {
        margin: 0;
        font-size: 1.05rem;
        font-weight: 700;
        letter-spacing: .15px;
        color: #111827;
        line-height: 1.25;
        padding: 0 12px;
      }

      .row-spacer { height: 36px; }
      .title {
        text-align:center; font-weight:700; font-size:1.2rem; margin: 0 0 10px 0;
        font-family: 'Manjari', system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif !important;
      }
      .hairline   { border-top: 1px solid #e5e5e7; margin: 10px 0 14px 0; }
      .section h3 { margin: 0 0 6px 0; font-size: 1.05rem; font-weight:700; }
      .section p  { margin: 0 0 4px 0; color: #333; font-size: 0.98rem; font-weight:400; }

      /* ===== Hovercard (popup al pasar el mouse) ===== */
      .hovercard {
        position: absolute;
        left: 50%;
        bottom: calc(100% + 12px);    /* aparece arriba de la tarjeta */
        transform: translateX(-50%) translateY(6px);
        width: min(420px, 90vw);
        background: rgba(255,255,255,0.72);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        border: 1px solid #e5e5e7;
        border-radius: 12px;
        padding: 12px 14px;
        box-shadow: 0 18px 38px rgba(0,0,0,.14);
        opacity: 0; visibility: hidden;
        transition: opacity .14s ease, transform .14s ease, visibility .14s;
        z-index: 50;
        pointer-events: none; /* no roba foco */
      }
      .card-wrap:hover .hovercard {
        opacity: 1; visibility: visible;
        transform: translateX(-50%) translateY(0);
      }
      .hovercard h4 { margin: 0 0 6px 0; font-size: 1.02rem; font-weight: 700; color: #0f172a; }
      .hovercard p  { margin: 0 0 4px 0; font-size: .95rem; color: #111827; }
      .hovercard .cta {
        display: inline-block; margin-top: 8px; padding: 6px 10px;
        border: 1px solid #e5e5e7; border-radius: 999px; text-decoration: none;
        color: #0f172a; font-weight: 700; font-size: .92rem; background: #fff;
      }
      .hovercard .cta:hover { background: #f5f5f7; }

      /* flechita */
      .hovercard::after {
        content: ""; position: absolute; top: 100%; left: 50%; transform: translateX(-50%);
        border-width: 8px; border-style: solid;
        border-color: #e5e5e7 transparent transparent transparent;
        filter: drop-shadow(0 2px 2px rgba(0,0,0,.05));
      }
      .hovercard::before {
        content: ""; position: absolute; top: calc(100% - 1px); left: 50%; transform: translateX(-50%);
        border-width: 7px; border-style: solid;
        border-color: #ffffff transparent transparent transparent;
      }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='wrap'>", unsafe_allow_html=True)

    # Dropdown centrado sin label
    s1, s2, s3 = st.columns([1,2,1])
    with s2:
        st.markdown("<div class='nav-select'>", unsafe_allow_html=True)
        nav_actual = st.session_state.get("nav", "Servicios")
        try:
            idx = opciones_nav.index(nav_actual)
        except ValueError:
            idx = 0
        seleccion = st.selectbox("Navegación", opciones_nav, index=idx, key="nav_select", label_visibility="collapsed")
        st.session_state.nav = seleccion
        st.markdown("</div>", unsafe_allow_html=True)

    # -------- Contenido según selección --------
    if st.session_state.nav == "Servicios":
        st.markdown("<div class='title'>Servicios</div>", unsafe_allow_html=True)

        servicios = [
            {"titulo": "APIs", "desc1": "Diseño y desarrollo de APIs escalables.", "desc2": "Autenticación, rate limiting y monitoreo."},
            {"titulo": "Software para Industrias", "desc1": "Sistemas a medida para planta/producción.", "desc2": "Integración con ERP y tableros."},
            {"titulo": "Tracking de Pedidos", "desc1": "Trazabilidad punta a punta.", "desc2": "Notificaciones y SLA visibles."},
            {"titulo": "Ecommerce", "desc1": "Tiendas headless / integradas.", "desc2": "Pagos, logística y analytics."},
            {"titulo": "Finanzas", "desc1": "Forecasting y conciliaciones automáticas.", "desc2": "Reportes y auditoría."},
            {"titulo": "Gestión de Stock", "desc1": "Inventario en tiempo real.", "desc2": "Alertas, valuación y KPIs."},
        ]

        # 3 x 2 con mayor separación lateral
        cols = st.columns(3, gap="large")
        for i, col in enumerate(cols):
            with col:
                svc = servicios[i]
                st.markdown(
                    f"""
                    <div class='tile'>
                      <div class='card-wrap'>
                        <div class='card'><h3>{svc["titulo"]}</h3></div>
                        <div class='hovercard'>
                          <h4>{svc["titulo"]}</h4>
                          <p>• {svc["desc1"]}</p>
                          <p>• {svc["desc2"]}</p>
                          <a class="cta" href="mailto:contacto@brandatta.com?subject={svc["titulo"]}%20-%20Consulta" target="_blank" rel="noopener">Escribinos</a>
                        </div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        st.markdown("<div class='row-spacer'></div>", unsafe_allow_html=True)

        cols2 = st.columns(3, gap="large")
        for j, col in enumerate(cols2):
            idx2 = 3 + j
            with col:
                svc = servicios[idx2]
                st.markdown(
                    f"""
                    <div class='tile'>
                      <div class='card-wrap'>
                        <div class='card'><h3>{svc["titulo"]}</h3></div>
                        <div class='hovercard'>
                          <h4>{svc["titulo"]}</h4>
                          <p>• {svc["desc1"]}</p>
                          <p>• {svc["desc2"]}</p>
                          <a class="cta" href="mailto:contacto@brandatta.com?subject={svc["titulo"]}%20-%20Consulta" target="_blank" rel="noopener">Escribinos</a>
                        </div>
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

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
