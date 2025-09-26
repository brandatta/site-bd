import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# ================== CONFIG ==================
st.set_page_config(page_title="Brandatta - Servicios", layout="wide")

# ================== STATE ==================
if "ingresado" not in st.session_state:
    st.session_state.ingresado = False
if "modal_open" not in st.session_state:
    st.session_state.modal_open = False
if "modal_idx" not in st.session_state:
    st.session_state.modal_idx = None

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

      /* contenedor full alto */
      .block-container, [data-testid="block-container"] {
        min-height: 100vh !important;
        display: flex !important;
        flex-direction: column !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
      }
      /* primer bloque centrado */
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

      /* Tarjetas grandes con más separación */
      .tile { width: 440px; margin: 0 auto 28px; }
      @media (max-width: 1200px){ .tile{ width: 400px; } }
      @media (max-width: 900px){  .tile{ width: 360px; } }

      /* Estilo de botón como tarjeta */
      .svc .stButton > button {
        width: 100% !important;
        height: 220px !important;
        border: 1px solid #d4fbd7 !important;
        border-radius: 0 !important;
        background: #ffffff !important;
        box-shadow: none !important;
        transition: border-color .12s ease, transform .12s ease !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;
        padding: 0 12px !important;
      }
      .svc .stButton > button:hover { border-color: #bff3c5 !important; transform: translateY(-1px); }
      .svc .stButton > button span, .svc .stButton > button p {
        font-family: 'Manjari', system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif !important;
        font-weight: 700 !important;
        font-size: 1.05rem !important;
        color: #111827 !important;
      }

      .row-spacer { height: 36px; }
      .title {
        text-align:center; font-weight:700; font-size:1.2rem; margin: 0 0 10px 0;
        font-family: 'Manjari', system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif !important;
      }
      .hairline   { border-top: 1px solid #e5e5e7; margin: 10px 0 14px 0; }
      .section h3 { margin: 0 0 6px 0; font-size: 1.05rem; font-weight:700; }
      .section p  { margin: 0 0 4px 0; color: #333; font-size: 0.98rem; font-weight:400; }

      /* ===== Modal / Popup ===== */
      .modal-backdrop {
        position: fixed; inset: 0; background: rgba(0,0,0,.35);
        display: flex; align-items: center; justify-content: center;
        animation: fadeIn .15s ease-out;
        z-index: 9999;
      }
      .modal-card {
        width: min(720px, 92vw);
        background: #ffffff; border: 1px solid #e5e5e7; border-radius: 12px;
        padding: 18px 16px;
        animation: popIn .14s ease-out;
        box-shadow: 0 10px 30px rgba(0,0,0,.12);
      }
      .modal-header { display:flex; align-items:center; justify-content: space-between; margin-bottom: 8px; }
      .modal-title { font-weight: 700; font-size: 1.15rem; }
      .modal-close {
        border: 1px solid #e5e5e7; background: #fff; padding: 6px 10px; border-radius: 999px; cursor: pointer;
      }
      .modal-close:hover { background: #f5f5f7; }
      .modal-body p { margin: 6px 0; line-height: 1.45; }

      @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
      @keyframes popIn  { from { transform: translateY(6px) scale(.98); opacity: 0; } to { transform: translateY(0) scale(1); opacity: 1; } }

      /* permite click en overlay para cerrar: cursor */
      .modal-backdrop { cursor: pointer; }
      .modal-card { cursor: default; }
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
            "APIs",
            "Software para Industrias",
            "Tracking de Pedidos",
            "Ecommerce",
            "Finanzas",
            "Gestión de Stock"
        ]

        # 3 x 2 con más separación lateral
        cols = st.columns(3, gap="large")
        for i, col in enumerate(cols):
            with col:
                st.markdown("<div class='tile svc'>", unsafe_allow_html=True)
                if st.button(servicios[i], key=f"svc_{i}"):
                    st.session_state.modal_open = True
                    st.session_state.modal_idx = i
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("<div class='row-spacer'></div>", unsafe_allow_html=True)

        cols2 = st.columns(3, gap="large")
        for j, col in enumerate(cols2):
            idx2 = 3 + j
            with col:
                st.markdown("<div class='tile svc'>", unsafe_allow_html=True)
                if st.button(servicios[idx2], key=f"svc_{idx2}"):
                    st.session_state.modal_open = True
                    st.session_state.modal_idx = idx2
                st.markdown("</div>", unsafe_allow_html=True)

        # ===== Modal (si está abierto) =====
        if st.session_state.modal_open and st.session_state.modal_idx is not None:
            svc = servicios[st.session_state.modal_idx]
            # Overlay + card (clic en fondo cierra)
            st.markdown(f"""
            <div class="modal-backdrop" onclick="window.parent.postMessage({{'closeModal': true}}, '*')">
              <div class="modal-card" onclick="event.stopPropagation()">
                <div class="modal-header">
                  <div class="modal-title">{svc}</div>
                  <button class="modal-close" onclick="window.parent.postMessage({{'closeModal': true}}, '*')">✕ Cerrar</button>
                </div>
                <div class="modal-body">
                  <p><b>¿Qué incluye?</b></p>
                  <p>• Roadmap rápido, entregables claros y foco en impacto.</p>
                  <p>• Integración con sistemas existentes (SAP, ecommerce, ERPs).</p>
                  <p>• Métricas y tableros para seguir el valor en tiempo real.</p>
                  <p>• Soporte y mejoras continuas.</p>
                </div>
              </div>
            </div>
            """, unsafe_allow_html=True)

            # Pequeño "listener" para cerrar desde JS (click en overlay o botón)
            # y un botón real para fallback sin JS
            close_cols = st.columns([1,1,1])
            with close_cols[1]:
                if st.button("Cerrar", key="modal_close_fallback"):
                    st.session_state.modal_open = False
                    st.session_state.modal_idx = None

            # Script para capturar postMessage y cerrar
            st.markdown("""
            <script>
              window.addEventListener('message', (event) => {
                if (event.data && event.data.closeModal) {
                  const streamlitDoc = window.parent;
                  if (streamlitDoc) {
                    // Simulamos un "click" programático al botón de fallback para forzar un rerun
                    const btns = window.parent.document.querySelectorAll('button[kind="secondary"]');
                  }
                }
              });
            </script>
            """, unsafe_allow_html=True)

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
