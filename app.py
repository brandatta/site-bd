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
if "soporte_authed" not in st.session_state:
    st.session_state.soporte_authed = False
if "soporte_user" not in st.session_state:
    st.session_state.soporte_user = None

OPCIONES = ["Servicios", "Contacto", "Acerca de Nosotros", "Clientes", "Soporte"]
SOPORTE_OPCIONES = ["Cargar Ticket", "Documentación", "Manuales"]

# -------- Query params helpers --------
def _qp_get() -> dict:
    try:
        return {k: (v[0] if isinstance(v, list) else v) for k, v in st.query_params.items()}
    except Exception:
        try:
            return {k: (v[0] if isinstance(v, list) else v) for k, v in st.experimental_get_query_params().items()}
        except Exception:
            return {}

def _qp_set(d: dict):
    clean = {k: v for k, v in d.items() if v is not None}
    try:
        st.query_params.from_dict(clean)
    except Exception:
        try:
            st.experimental_set_query_params(**clean)
        except Exception:
            pass

# ====== Leer query params ======
qp = _qp_get()
nav_qp  = unquote(qp.get("nav"))  if qp.get("nav")  else None
ing_qp  = qp.get("ing")
snav_qp = unquote(qp.get("snav")) if qp.get("snav") else None
sp_qp   = qp.get("sp")

if ing_qp == "1":
    st.session_state.ingresado = True
if sp_qp == "1":
    st.session_state.soporte_authed = True

if nav_qp in OPCIONES:
    st.session_state.nav = nav_qp
elif "nav" not in st.session_state or st.session_state.get("nav") not in OPCIONES:
    st.session_state.nav = "Servicios"

if snav_qp in SOPORTE_OPCIONES:
    st.session_state.snav = snav_qp
elif "snav" not in st.session_state or st.session_state.get("snav") not in SOPORTE_OPCIONES:
    st.session_state.snav = SOPORTE_OPCIONES[0]

# ===== Helper: logo en base64 =====
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
      html, body, [data-testid="stAppViewContainer"] { background: #d4fbd7 !important; font-family: 'Manjari', system-ui, sans-serif !important; }
      header, #MainMenu, footer { visibility: hidden; }
      .block-container { min-height: 100vh !important; display: flex !important; flex-direction: column !important; justify-content: center !important; align-items: center !important; }
      #hero .stButton > button { margin-top: 28px; border-radius: 0; border: 1px solid rgba(0,0,0,0.15); background: #fff; font-weight: 700; font-family: 'Manjari', sans-serif; padding: 10px 18px; cursor: pointer; }
      @keyframes blink { 0%{opacity:1;transform:scale(1);} 50%{opacity:.4;transform:scale(1.03);} 100%{opacity:1;transform:scale(1);} }
      #hero .hero-logo { animation: blink 1.6s ease-in-out infinite; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div id='hero'>", unsafe_allow_html=True)
    st.markdown(logo_html_src(width_px=200).replace("<img ", "<img class='hero-logo' "), unsafe_allow_html=True)

    if st.button("Ingresar", key="ingresar_btn"):
        st.session_state.ingresado = True
        _qp_set({"nav": st.session_state.get("nav", "Servicios"), "ing": "1", "sp": "1" if st.session_state.soporte_authed else None})

    st.markdown("</div>", unsafe_allow_html=True)

# ================== CONTENIDO ==================
else:
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Manjari:wght@100;400;700&display=swap');
      [data-testid="stAppViewContainer"] { background:#fff !important; font-family:'Manjari', system-ui, sans-serif !important; }
      header, #MainMenu, footer {visibility: hidden;}

      /* 🔹 Quitamos padding superior */
      .block-container, [data-testid="block-container"]{
        padding-top: 0 !important;
        padding-bottom: 0 !important;
      }
      [data-testid="stAppViewContainer"]{
        padding-top: 0 !important;
      }

      /* ===== Menú principal ===== */
      #topnav-wrap{ position: sticky; top: 0; z-index: 999; background: #ffffff; border-bottom: 1px solid #e5e5e7; box-shadow: 0 1px 6px rgba(0,0,0,.04); margin-top: 0 !important; }
      nav.topnav{ max-width: 1440px; margin: 0 auto; padding: 8px 16px !important; display: flex; align-items: center; justify-content: center; gap: 28px !important; }
      nav.topnav a{ color: #0f0f0f; text-decoration: none; padding: 8px 2px; border-bottom: 2px solid transparent; text-transform: uppercase; font-weight: 700; font-size: .95rem; transition: border .15s; }
      nav.topnav a:hover{ border-bottom-color: #0f0f0f; }
      nav.topnav a.active{ border-bottom-color: #0f0f0f; }

      /* ===== Grilla de Servicios ===== */
      .services-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 24px;
        max-width: 1320px;
        margin: 20px auto 32px;
        justify-items: center;
      }
      .tile { width: 100%; max-width: 420px; position: relative; }
      .card { background:#fff; border:1px solid #d4fbd7; height:110px; display:flex; align-items:center; justify-content:center; transition:all .15s ease; }
      .card:hover{ border-color:#bff3c5; transform:translateY(-2px); box-shadow:0 10px 24px rgba(0,0,0,.06); }
      .card h3{ font-size:1.05rem; font-weight:700; color:#111; margin:0; }
      .hovercard{ position:absolute; left:50%; bottom:calc(100% + 8px); transform:translateX(-50%); background:rgba(255,255,255,0.9); backdrop-filter:blur(6px); border:1px solid #e5e5e7; border-radius:10px; padding:10px 14px; opacity:0; visibility:hidden; transition:opacity .15s,transform .15s; }
      .card-wrap:hover .hovercard{ opacity:1; visibility:visible; transform:translateX(-50%) translateY(-4px); }
      .hovercard h4{ margin:0 0 4px; font-size:1rem; font-weight:700; }
      .hovercard p{ margin:0; font-size:.9rem; color:#111; }
    </style>
    """, unsafe_allow_html=True)

    # ===== HEADER =====
    links_html = []
    for label in OPCIONES:
        params = {"nav": label, "ing": "1"}
        if st.session_state.soporte_authed:
            params["sp"] = "1"
        href = "./?" + "&".join([f"{k}={quote(v)}" for k, v in params.items()])
        active = " active" if st.session_state.nav == label else ""
        links_html.append(f"<a class='{active}' href='{href}' target='_self'>{label.upper()}</a>")

    st.markdown(f"<div id='topnav-wrap'><nav class='topnav'>{''.join(links_html)}</nav></div>", unsafe_allow_html=True)

    st.markdown("<div class='wrap' style='padding-top:8px;'>", unsafe_allow_html=True)
    nav = st.session_state.nav

    # ===== SERVICIOS =====
    if nav == "Servicios":
        st.markdown("<div class='title' style='text-align:center;font-weight:700;font-size:1.2rem;margin:20px 0;'>Servicios</div>", unsafe_allow_html=True)

        servicios = [
            {"titulo": "APIs", "desc1": "Diseño y desarrollo de APIs escalables.", "desc2": "Autenticación, rate limiting y monitoreo."},
            {"titulo": "Software para Industrias", "desc1": "Sistemas a medida para planta/producción.", "desc2": "Integración con ERP y tableros."},
            {"titulo": "Tracking de Pedidos", "desc1": "Trazabilidad punta a punta.", "desc2": "Notificaciones y SLA visibles."},
            {"titulo": "Ecommerce", "desc1": "Tiendas headless / integradas.", "desc2": "Pagos, logística y analytics."},
            {"titulo": "Finanzas", "desc1": "Forecasting y conciliaciones automáticas.", "desc2": "Reportes y auditoría."},
            {"titulo": "Gestión de Stock", "desc1": "Inventario en tiempo real.", "desc2": "Alertas, valuación y KPIs."},
        ]

        html_cards = ""
        for i, svc in enumerate(servicios):
            html_cards += f"""
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
"""
        st.markdown(f"<div class='services-grid'>{html_cards}</div>", unsafe_allow_html=True)

    elif nav == "Contacto":
        st.markdown("<h3>Contacto</h3><p>Email: brandatta@brandatta.com.ar</p><p>Teléfono: +54 11 0000-0000</p>", unsafe_allow_html=True)

    elif nav == "Acerca de Nosotros":
        st.markdown("<h3>Acerca de nosotros</h3><p>Construimos soluciones digitales a medida: integraciones con SAP y Ecommerce, tableros, automatizaciones y apps.</p>", unsafe_allow_html=True)

    elif nav == "Clientes":
        st.markdown("<h3>Clientes</h3><p>Trabajamos con compañías de retail, industria y servicios: Georgalos, Vicbor, ITPS, Biosidus, Glam, Espumas, Café Martínez, entre otros.</p>", unsafe_allow_html=True)

    # ===== SOPORTE =====
    elif nav == "Soporte":
        if not st.session_state.soporte_authed:
            st.markdown("### Soporte — Iniciar sesión")
            with st.form("login_soporte"):
                email = st.text_input("Email corporativo")
                pwd = st.text_input("Contraseña", type="password")
                submit = st.form_submit_button("Entrar")
            if submit:
                if email and pwd:
                    st.session_state.soporte_authed = True
                    st.session_state.soporte_user = email
                    _qp_set({"nav": "Soporte", "ing": "1", "sp": "1"})
                    st.success(f"Bienvenido/a, {email}")
                else:
                    st.error("Completá email y contraseña.")
        else:
            sub_links = []
            for slabel in SOPORTE_OPCIONES:
                params = {"nav": "Soporte", "snav": slabel, "ing": "1", "sp": "1"}
                href = "./?" + "&".join([f"{k}={quote(v)}" for k, v in params.items()])
                active = " active" if st.session_state.snav == slabel else ""
                sub_links.append(f"<a class='{active}' href='{href}' target='_self'>{slabel}</a>")
            st.markdown(f"<div id='subnav-wrap'><nav class='subnav'>{''.join(sub_links)}</nav></div>", unsafe_allow_html=True)

            snav = st.session_state.snav
            if snav == "Cargar Ticket":
                st.markdown("### Cargar Ticket")
                with st.form("form_ticket"):
                    email_t = st.text_input("Tu email", value=st.session_state.soporte_user or "")
                    asunto = st.text_input("Asunto")
                    descripcion = st.text_area("Descripción del problema")
                    enviar = st.form_submit_button("Enviar ticket")
                if enviar:
                    st.success("✅ Ticket enviado correctamente.")
            elif snav == "Documentación":
                st.markdown("### Documentación\n- APIs Brandatta\n- Integración con ERP (SAP)\n- Webhooks y Seguridad", unsafe_allow_html=True)
            elif snav == "Manuales":
                st.markdown("### Manuales\n- Manual de Operador de Planta\n- Manual de Ecommerce (Administrador)\n- Manual de Finanzas", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
