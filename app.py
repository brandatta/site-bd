import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from urllib.parse import quote, unquote

# ================== CONFIG ==================
st.set_page_config(page_title="Brandatta - Servicios", layout="wide")

# ================== STATE ==================
if "ingresado" not in st.session_state:
    st.session_state.ingresado = False

OPCIONES = ["Servicios", "Contacto", "Acerca de Nosotros", "Clientes"]

# -------- Query params (compat 1.30+ y previas) --------
def _qp_get() -> dict:
    if hasattr(st, "query_params"):
        try:
            qp = st.query_params
            return {k: (v[0] if isinstance(v, list) else v) for k, v in qp.items()}
        except Exception:
            pass
    try:
        return {k: (v[0] if isinstance(v, list) else v) for k, v in st.experimental_get_query_params().items()}
    except Exception:
        return {}

def _qp_set(d: dict):
    clean = {k: v for k, v in d.items() if v is not None}
    if hasattr(st, "query_params"):
        try:
            st.query_params.from_dict(clean); return
        except Exception:
            pass
    try:
        st.experimental_set_query_params(**clean)
    except Exception:
        pass

# ====== Leer nav/ingresado desde la URL ANTES de renderizar ======
qp = _qp_get()
nav_qp = unquote(qp.get("nav")) if qp.get("nav") else None
ing_qp = qp.get("ing")  # 🔸 ing=1 mantiene la sesión como ingresada

if ing_qp == "1":
    st.session_state.ingresado = True  # 🔸 fuerza sesión ingresada si la URL lo dice

if nav_qp in OPCIONES:
    st.session_state.nav = nav_qp
elif "nav" not in st.session_state or st.session_state.get("nav") not in OPCIONES:
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
      @import url('https://fonts.googleapis.com/css2?family=Manjari:wght@100;400;700&display=swap');
      html, body, [data-testid="stAppViewContainer"] { background: #d4fbd7 !important; font-family: 'Manjari', system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif !important; }
      header, #MainMenu, footer { visibility: hidden; }
      .block-container, [data-testid="block-container"] { min-height: 100vh !important; display: flex !important; flex-direction: column !important; padding-top: 0 !important; padding-bottom: 0 !important; }
      [data-testid="stVerticalBlock"]:first-of-type { flex: 1 0 auto !important; display: flex !important; flex-direction: column !important; align-items: center !important; justify-content: center !important; gap: 14px !important; width: 100% !important; }
      #hero .stButton > button { display:block !important; margin:28px auto 0 auto !important; border-radius:0 !important; border:1px solid rgba(0,0,0,0.15) !important; background:#fff !important; font-weight:700 !important; font-family:'Manjari', system-ui, sans-serif !important; padding:10px 18px !important; cursor:pointer; }
      @keyframes blink { 0%{opacity:1;transform:scale(1);} 50%{opacity:.35;transform:scale(1.02);} 100%{opacity:1;transform:scale(1);} }
      #hero .hero-logo { animation: blink 1.6s ease-in-out infinite; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div id='hero'>", unsafe_allow_html=True)
    st.markdown(logo_html_src(width_px=200).replace("<img ", "<img class='hero-logo' "), unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        if st.button("Ingresar", key="ingresar_btn"):
            st.session_state.ingresado = True
            # 🔸 Seteamos ing=1 y mantenemos nav actual en la URL para que no vuelva la portada
            _qp_set({"nav": st.session_state.get("nav", "Servicios"), "ing": "1"})

    st.markdown("</div>", unsafe_allow_html=True)

# ================== CONTENIDO ==================
else:
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Manjari:wght@100;400;700&display=swap');

      [data-testid="stAppViewContainer"] { background:#ffffff !important; font-family:'Manjari', system-ui, sans-serif !important; }
      header, #MainMenu, footer {visibility: hidden;}
      .block-container, [data-testid="block-container"] { padding-top: 0 !important; padding-bottom: 0 !important; }

      .wrap { max-width: 1440px; margin: 0 auto; padding: 0 8px 16px; }
      [data-testid="stVerticalBlock"], [data-testid="column"], .wrap, .tile { overflow: visible !important; }

      /* ===== MENÚ: <nav> con links negros, horizontal, sticky ===== */
      #topnav-wrap{ position: sticky; top: 0; z-index: 999; background: #ffffff; border-bottom: 1px solid #e5e5e7; box-shadow: 0 1px 6px rgba(0,0,0,.04); }
      nav.topnav{ max-width: 1440px; margin: 0 auto; padding: 12px 16px; display: flex; align-items: center; justify-content: center; gap: 32px; }
      nav.topnav * { margin: 0; padding: 0; }
      nav.topnav a{ display: inline-block; color: #0f0f0f; text-decoration: none; padding: 8px 2px; border-bottom: 2px solid transparent; text-transform: uppercase; font-weight: 700; letter-spacing: .03em; font-size: .95rem; }
      nav.topnav a:hover{ border-bottom-color: #0f0f0f; }
      nav.topnav a.active{ border-bottom-color: #0f0f0f; }

      /* ===== Tarjetas ===== */
      .tile { width: 440px; margin: 0 auto 28px; position: relative; }
      @media (max-width: 1200px){ .tile{ width: 400px; } }
      @media (max-width: 900px){  .tile{ width: 360px; } }
      .card-wrap { position: relative; }
      .card { background:#ffffff; border:1px solid #d4fbd7; border-radius:0; height:110px; display:flex; align-items:center; justify-content:center; text-align:center; transition:border-color .12s ease, transform .12s ease, box-shadow .12s ease; }
      .card:hover{ border-color:#bff3c5; transform:translateY(-1px); box-shadow:0 12px 24px rgba(0,0,0,.06); }
      .card h3{ margin:0; font-size:1.05rem; font-weight:700; letter-spacing:.15px; color:#111827; line-height:1.25; padding:0 12px; }

      .row-spacer { height: 36px; }
      .title { text-align:center; font-weight:700; font-size:1.2rem; margin: 0 0 10px 0; }
      .hairline { border-top: 1px solid #e5e5e7; margin: 10px 0 14px 0; }
      .section h3 { margin: 0 0 6px 0; font-size: 1.05rem; font-weight:700; }
      .section p { margin: 0 0 4px 0; color: #333; font-size: 0.98rem; font-weight:400; }

      /* ===== Hovercard ===== */
      .hovercard { position:absolute; left:50%; width:min(420px,90vw); background:rgba(255,255,255,0.8); backdrop-filter:blur(8px); border:1px solid #e5e5e7; border-radius:10px; padding:10px 14px; box-shadow:0 14px 28px rgba(0,0,0,.12); opacity:0; visibility:hidden; transition:opacity .14s ease, transform .14s ease, visibility .14s; z-index:50; pointer-events:none; }
      .card-wrap .hovercard { bottom:calc(100% + 10px); transform:translateX(-50%) translateY(6px); }
      .card-wrap:hover .hovercard { opacity:1; visibility:visible; transform:translateX(-50%) translateY(0); }
      .card-wrap .hovercard::after{ content:""; position:absolute; top:100%; left:50%; transform:translateX(-50%); border-width:7px; border-style:solid; border-color:#e5e5e7 transparent transparent transparent; }
      .card-wrap .hovercard::before{ content:""; position:absolute; top:calc(100% - 1px); left:50%; transform:translateX(-50%); border-width:6px; border-style:solid; border-color:#ffffff transparent transparent transparent; }
      .card-wrap.below .hovercard { top: calc(100% + 10px); bottom:auto; transform: translateX(-50%) translateY(-6px); }
      .card-wrap.below:hover .hovercard { opacity:1; visibility:visible; transform: translateX(-50%) translateY(0); }
      .hovercard h4 { margin:0 0 6px 0; font-size:1rem; font-weight:700; color:#0f172a; }
      .hovercard p  { margin:0 0 4px 0; font-size:.9rem; color:#111827; }
    </style>
    """, unsafe_allow_html=True)

    # ===== MENÚ (nav con ?nav=... y preserva ing=1) =====
    links_html = []
    for label in OPCIONES:
        # 🔸 Si ya estás ingresado, agregamos ing=1 para no perder el estado al navegar
        if st.session_state.ingresado:
            href = f"./?nav={quote(label)}&ing=1"
        else:
            href = f"./?nav={quote(label)}"
        active_cls = " active" if st.session_state.nav == label else ""
        links_html.append(f"<a class='{active_cls}' href='{href}' target='_self'>{label.upper()}</a>")
    nav_html = f"<div id='topnav-wrap'><nav class='topnav'>{''.join(links_html)}</nav></div>"
    st.markdown(nav_html, unsafe_allow_html=True)

    # ===== CONTENIDO: SOLO la sección elegida =====
    st.markdown("<div class='wrap'>", unsafe_allow_html=True)
    nav = st.session_state.nav

    if nav == "Servicios":
        st.markdown("<div class='title'>Servicios</div>", unsafe_allow_html=True)
        servicios = [
            {"titulo": "APIs", "desc1": "Diseño y desarrollo de APIs escalables.", "desc2": "Autenticación, rate limiting y monitoreo."},
            {"titulo": "Software para Industrias", "desc1": "Sistemas a medida para planta/producción.", "desc2": "Integración con ERP y tableros."},
            {"titulo": "Tracking de Pedidos", "desc1": "Trazabilidad punta a punta.", "desc2": "Notificaciones y SLA visibles."},
            {"titulo": "Ecommerce", "desc1": "Tiendas headless / integradas.", "desc2": "Pagos, logística y analytics."},
            {"titulo": "Finanzas", "desc1": "Forecasting y conciliaciones automáticas.", "desc2": "Reportes y auditoría."},
            {"titulo": "Gestión de Stock", "desc1": "Inventario en tiempo real.", "desc2": "Alertas, valuación y KPIs."},
        ]
        cols = st.columns(3, gap="large")
        for i, col in enumerate(cols):
            with col:
                svc = servicios[i]
                st.markdown(f"""
                <div class='tile'>
                  <div class='card-wrap below'>
                    <div class='card'><h3>{svc["titulo"]}</h3></div>
                    <div class='hovercard'>
                      <h4>{svc["titulo"]}</h4>
                      <p>• {svc["desc1"]}</p>
                      <p>• {svc["desc2"]}</p>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)
        st.markdown("<div class='row-spacer'></div>", unsafe_allow_html=True)
        cols2 = st.columns(3, gap="large")
        for j, col in enumerate(cols2):
            idx2 = 3 + j
            with col:
                svc = servicios[idx2]
                st.markdown(f"""
                <div class='tile'>
                  <div class='card-wrap'>
                    <div class='card'><h3>{svc["titulo"]}</h3></div>
                    <div class='hovercard'>
                      <h4>{svc["titulo"]}</h4>
                      <p>• {svc["desc1"]}</p>
                      <p>• {svc["desc2"]}</p>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

    elif nav == "Contacto":
        st.markdown("<div class='hairline'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section">
          <h3>Contacto</h3>
          <p>Email: brandatta@brandatta.com.ar</p>
          <p>Teléfono: +54 11 0000-0000</p>
          <p>Dirección: Buenos Aires, Argentina</p>
        </div>
        """, unsafe_allow_html=True)

    elif nav == "Acerca de Nosotros":
        st.markdown("<div class='hairline'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section">
          <h3>Acerca de nosotros</h3>
          <p>Construimos soluciones digitales a medida: integraciones con SAP y Ecommerce, tableros, automatizaciones y apps.</p>
          <p>Enfocados en performance, UX minimalista y resultados de negocio.</p>
        </div>
        """, unsafe_allow_html=True)

    elif nav == "Clientes":
        st.markdown("<div class='hairline'></div>", unsafe_allow_html=True)
        st.markdown("""
        <div class="section">
          <h3>Clientes</h3>
          <p>Trabajamos con compañías de retail, industria y servicios: Georgalos, Vicbor, ITPS, Biosidus, Glam, Espumas, Café Martínez, entre otros.</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
