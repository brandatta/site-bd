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
sel_qp  = unquote(qp.get("sel")) if qp.get("sel") else None  # <-- tarjeta seleccionada (ya no se usa para abrir detalle)

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

# ===== Helper: logo portada (en base64) =====
def logo_html_src(path="logo.png", width_px=200):
    try:
        img = Image.open(path)
        buf = BytesIO(); img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f'<img src="data:image/png;base64,{b64}" alt="logo" style="width:{width_px}px;max-width:{width_px}px;height:auto;display:block;margin:0 auto;" />'
    except Exception:
        return "<p style='text-align:center;font-weight:600;margin:0;'>Subí <code>logo.png</code> a la carpeta de la app.</p>"

# ===== Helper: logo header (en base64) =====
def header_logo_html(path="logooo (1).png"):
    try:
        img = Image.open(path)
        buf = BytesIO(); img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f'<img id="brand-logo" src="data:image/png;base64,{b64}" alt="Brandatta" />'
    except Exception:
        # fallback si no existe el archivo
        return "<div id='brand-logo' style='width:160px;height:60px;background:#eee;border:1px solid #ddd;border-radius:6px;'></div>"

# ===== Helper: imagen para hover/modal (en base64) =====
def hover_img_html(path, alt="img"):
    try:
        img = Image.open(path)
        buf = BytesIO(); img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f"<img class='hover-img' src='data:image/png;base64,{b64}' alt='{alt}' />"
    except Exception:
        return ""  # si no existe, no muestra nada

# ================== PORTADA ==================
if not st.session_state.ingresado:
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Manjari:wght@100;400;700&display=swap');
      html, body, [data-testid="stAppViewContainer"] { background: #d4fbd7 !important; font-family: 'Manjari', system-ui, sans-serif !important; }
      header, #MainMenu, footer { visibility: hidden; }
      .block-container { min-height: 100vh !important; display: flex !important; flex-direction: column !important; justify-content: center !important; align-items: center !important; }
      #hero .stButton > button { margin-top: 28px; border-radius: 0; border: 1px solid rgba(0,0,0,0.15); background: #fff; font-weight: 700; padding: 10px 18px; cursor: pointer; }
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
    # ====== CSS General + Servicios + Modal ======
    detail_open_class = ""  # (lo dejé vacío: ahora el detalle abre en modal)
    st.markdown(f"""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Manjari:wght@100;400;700&display=swap');
      [data-testid="stAppViewContainer"] {{ background:#fff !important; font-family:'Manjari', system-ui, sans-serif !important; }}
      header, #MainMenu, footer {{visibility: hidden;}}
      .block-container, [data-testid="block-container"]{{ padding-top: 0 !important; padding-bottom: 0 !important; }}
      [data-testid="stAppViewContainer"]{{ padding-top: 0 !important; }}

      /* ===== Header sticky con logo ===== */
      #topnav-wrap{{ position: sticky; top: 0; z-index: 1000; background: #ffffff; border-bottom: 1px solid #e5e5e7; box-shadow: 0 1px 6px rgba(0,0,0,.04); margin-top: 0 !important; }}
      nav.topnav{{ max-width: 1440px; margin: 0 auto; padding: 8px 16px !important; display: flex; align-items: center; justify-content: space-between; gap: 16px; position: relative; }}
      .nav-left{{ display:flex; align-items:center; gap:10px; min-width: 200px; }}
      .nav-center{{ position:absolute; left:50%; transform:translateX(-50%); display:flex; gap:28px; align-items:center; }}
      .nav-right{{ min-width: 200px; }}
      #brand-logo{{ height: 70px; width: auto; display:block; }}
      @media (max-width: 1200px){{ #brand-logo{{ height: 52px; }} .nav-left, .nav-right {{ min-width: 180px; }} }}
      @media (max-width: 900px){{ #brand-logo{{ height: 44px; }} .nav-left, .nav-right {{ min-width: 160px; }} }}
      @media (max-width: 640px){{ #brand-logo{{ height: 36px; }} .nav-left, .nav-right {{ min-width: 120px; }} }}
      .nav-center a{{ color: #0f0f0f; text-decoration: none; padding: 8px 2px; border-bottom: 2px solid transparent; text-transform: uppercase; font-weight: 700; font-size: .95rem; transition: border .15s; white-space: nowrap; }}
      .nav-center a:hover{{ border-bottom-color: #0f0f0f; }}
      .nav-center a.active{{ border-bottom-color: #0f0f0f; }}

      /* ===== Grilla de Servicios ===== */
      .services-area {{ max-width: 1320px; margin: 20px auto 12px; }}
      .services-grid {{
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 24px;
        justify-items: center;
        transition: transform .25s ease;
      }}

      .tile {{ width: 100%; max-width: 420px; position: relative; overflow: visible !important; z-index: 0; cursor:pointer; }}
      .tile:hover {{ z-index: 200; transform: translateX(-6px); transition: transform .2s ease; }}
      .card-wrap {{ position: relative; overflow: visible !important; }}
      .card {{ background:#fff; border:1px solid #d4fbd7; height:110px; display:flex; align-items:center; justify-content:center; transition:all .15s ease; box-sizing: border-box; border-radius:10px; }}
      .card:hover{{ border-color:#bff3c5; box-shadow:0 10px 24px rgba(0,0,0,.06); }}
      .card h3{{ font-size:1.05rem; font-weight:700; color:#111; margin:0; }}

      /* Hovercard (no altera layout) */
      .hovercard{{
        position:absolute; left:50%;
        background:rgba(255,255,255,0.97); backdrop-filter:blur(6px);
        border:1px solid #e5e5e7; border-radius:10px; padding:10px 14px;
        opacity:0; visibility:hidden; transition:opacity .15s, transform .15s;
        z-index: 300; box-shadow:0 12px 28px rgba(0,0,0,0.14);
        pointer-events: none; width: max(280px, 60%);
        text-align:left;
      }}
      .card-wrap:hover .hovercard{{ opacity:1; visibility:visible; }}
      .hover-up{{ bottom:calc(100% + 8px); transform:translateX(-50%) translateY(6px); }}
      .card-wrap:hover .hover-up{{ transform:translateX(-50%) translateY(0); }}
      .hover-down{{ top:calc(100% + 8px); transform:translateX(-50%) translateY(-6px); }}
      .card-wrap:hover .hover-down{{ transform:translateX(-50%) translateY(0); }}
      .hovercard h4{{ margin:0 0 4px; font-size:1rem; font-weight:700; }}
      .hovercard p{{ margin:0; font-size:.9rem; color:#111; }}
      .hover-img{{ display:block; width:100%; max-height:120px; object-fit:contain; margin:0 0 8px 0; background:#fff; border:1px solid #eef2f3; border-radius:8px; }}

      /* ===== MODAL (CSS-only con :target) ===== */
      .modal{ position: fixed; inset: 0; background: rgba(0,0,0,.45); display:none; align-items:center; justify-content:center; z-index: 9999; padding:20px; }
      .modal:target{ display:flex; }
      .modal-card{ background:#fff; color:#111; width:min(820px, 94vw); max-height:86vh; overflow:auto;
                   border:1px solid #e5e5e7; border-radius:14px; box-shadow:0 18px 44px rgba(0,0,0,.22); padding:18px 20px; animation: fadeIn .2s ease; }
      .modal-header{ display:flex; align-items:center; justify-content:space-between; gap:12px; border-bottom:1px solid #f0f0f2; padding-bottom:8px; margin-bottom:12px; }
      .modal-close{ display:inline-block; text-decoration:none; border:1px solid #e5e5e7; border-radius:8px; padding:6px 10px; background:#fafafa; color:#111; font-weight:600; }
      .modal-close:hover{ background:#f1f1f3; }
      .modal-body p{ margin:.4rem 0; }
      .modal-img{ display:block; width:100%; max-height:220px; object-fit:contain; margin:4px 0 10px 0; border:1px solid #eef2f3; border-radius:10px; background:#fff; }

      @keyframes fadeIn {{
        from {{opacity:0; transform: translateY(8px);}}
        to   {{opacity:1; transform: translateY(0);}}
      }}
    </style>
    """, unsafe_allow_html=True)

    # ===== HEADER (logo izquierda + nav centrado) =====
    logo_left = header_logo_html("logooo (1).png")
    links_html = []
    for label in OPCIONES:
        params = {"nav": label, "ing": "1"}
        if st.session_state.soporte_authed:
            params["sp"] = "1"
        href = "./?" + "&".join([f"{k}={quote(v)}" for k, v in params.items()])
        active = " active" if st.session_state.nav == label else ""
        links_html.append(f"<a class='{active}' href='{href}' target='_self'>{label.upper()}</a>")

    header_html = f"""
<div id='topnav-wrap'>
  <nav class='topnav'>
    <div class='nav-left'>
      <a href='./?nav=Servicios&ing=1{"&sp=1" if st.session_state.soporte_authed else ""}' target='_self'>{logo_left}</a>
    </div>
    <div class='nav-center'>
      {''.join(links_html)}
    </div>
    <div class='nav-right'></div>
  </nav>
</div>
"""
    st.markdown(header_html, unsafe_allow_html=True)

    # ===== CONTENEDOR =====
    st.markdown("<div class='wrap' style='padding-top:8px;'>", unsafe_allow_html=True)
    nav = st.session_state.nav

    # ===== SERVICIOS =====
    if nav == "Servicios":
        st.markdown("<div class='title' style='text-align:center;font-weight:700;font-size:1.2rem;margin:20px 0;'>Servicios</div>", unsafe_allow_html=True)

        # Definición de servicios (con 'id' y 'long' para modal)
        servicios = [
            {
                "id": "apis",
                "titulo": "APIs",
                "desc1": "Diseño y desarrollo de APIs escalables.",
                "desc2": "Autenticación, rate limiting y monitoreo.",
                "img": "download.png",
                "long": "Diseñamos APIs REST/GraphQL con seguridad (OAuth2/JWT), versionado, observabilidad, pruebas contractuales y SLAs claros. Integración con gateways y mensajería."
            },
            {
                "id": "industria",
                "titulo": "Software para Industrias",
                "desc1": "Sistemas a medida para planta/producción.",
                "desc2": "Integración con ERP y tableros.",
                "img": "download.png",
                "long": "MES/SCADA liviano, captura de datos en línea, controles de calidad y OEE. Integración con SAP/Produmex, dashboards en tiempo real y trazabilidad completa."
            },
            {
                "id": "tracking",
                "titulo": "Tracking de Pedidos",
                "desc1": "Trazabilidad punta a punta.",
                "desc2": "Notificaciones y SLA visibles.",
                "img": "download.png",
                "long": "Visibilidad e2e: toma de pedido → preparación → despacho → entrega. Notificaciones proactivas, auditoría y paneles con métricas de cumplimiento."
            },
            {
                "id": "ecommerce",
                "titulo": "Ecommerce",
                "desc1": "Tiendas headless / integradas.",
                "desc2": "Pagos, logística y analytics.",
                "img": "download.png",
                "long": "Arquitecturas headless, promociones avanzadas, OMS y sincronización con ERP/WMS. Checkout optimizado y data layer para analítica."
            },
            {
                "id": "finanzas",
                "titulo": "Finanzas",
                "desc1": "Forecasting y conciliaciones automáticas.",
                "desc2": "Reportes y auditoría.",
                "img": "download.png",
                "long": "Flujos de conciliación bancaria, aging y cashflow, integración contable, reportería multiempresa y reglas de auditoría con alertas."
            },
            {
                "id": "stock",
                "titulo": "Gestión de Stock",
                "desc1": "Inventario en tiempo real.",
                "desc2": "Alertas, valuación y KPIs.",
                "img": "download.png",
                "long": "App móvil de inventario, ubicación por sectores, reposición, lote/serie, valuación y KPIs operativos. Integración con WMS y ERP."
            },
        ]

        # Contenedor de tarjetas
        st.markdown(f"<div class='services-area {detail_open_class}'>", unsafe_allow_html=True)

        # Render de tarjetas clickeables -> abren MODAL con #svc-<id>
        html_cards = ""
        for i, svc in enumerate(servicios):
            hover_class = "hover-down" if i < 3 else "hover-up"
            img_html = hover_img_html(svc.get("img"), alt=svc["titulo"]) if svc.get("img") else ""
            html_cards += f"""
<div class='tile'>
  <div class='card-wrap'>
    <a class='card-link' href='#svc-{svc["id"]}' style='text-decoration:none;color:inherit;display:block;'>
      <div class='card'><h3>{svc["titulo"]}</h3></div>
    </a>
    <div class='hovercard {hover_class}'>
      {img_html}
      <h4>{svc["titulo"]}</h4>
      <p>• {svc["desc1"]}</p>
      <p>• {svc["desc2"]}</p>
    </div>
  </div>
</div>
"""
        st.markdown(f"<div class='services-grid'>{html_cards}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)  # cierre .services-area

        # ===== Modales por servicio (CSS :target) =====
        modals_html = ""
        for svc in servicios:
            modal_img = hover_img_html(svc.get("img"), alt=svc["titulo"]).replace("hover-img", "modal-img") if svc.get("img") else ""
            modals_html += f"""
<div id='svc-{svc["id"]}' class='modal'>
  <div class='modal-card' role='dialog' aria-modal='true' aria-labelledby='svc-title-{svc["id"]}'>
    <div class='modal-header'>
      <h3 id='svc-title-{svc["id"]}' style='margin:0;font-size:1.1rem;'>{svc["titulo"]}</h3>
      <a href='#' class='modal-close' aria-label='Cerrar'>×</a>
    </div>
    <div class='modal-body'>
      {modal_img}
      <p class='meta'>• {svc["desc1"]}<br/>• {svc["desc2"]}</p>
      <p>{svc["long"]}</p>
      <div style='margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;'>
        <a href='#' class='modal-close'>Cerrar</a>
        <a href='./?nav=Contacto&ing=1{"&sp=1" if st.session_state.soporte_authed else ""}'
           class='modal-close' style='text-decoration:none;border:1px solid #0f0f0f;border-radius:8px;padding:6px 10px;'>Contactar</a>
      </div>
    </div>
  </div>
</div>
"""
        st.markdown(modals_html, unsafe_allow_html=True)

    elif nav == "Contacto":
        st.markdown("<h3>Contacto</h3><p>Email: brandatta@brandatta.com.ar</p><p>Teléfono: +54 11 0000-0000</p><p>Dirección: Buenos Aires, Argentina</p>", unsafe_allow_html=True)

    elif nav == "Acerca de Nosotros":
        st.markdown("<h3>Acerca de nosotros</h3><p>Construimos soluciones digitales a medida: integraciones con SAP y Ecommerce, tableros, automatizaciones y apps. Enfocados en performance, UX minimalista y resultados de negocio.</p>", unsafe_allow_html=True)

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
                    _qp_set({"nav": "Soporte", "ing": "1", "sp": "1", "snav": st.session_state.snav})
                    st.success(f"Bienvenido/a, {email}")
                else:
                    st.error("Completá email y contraseña.")
        else:
            # Submenú Soporte (sticky y con persistencia)
            st.markdown("""
            <style>
              #subnav-wrap{ position: sticky; top: 48px; z-index: 900; background: #ffffff; border-bottom: 1px solid #f0f0f1; }
              nav.subnav{ max-width: 1000px; margin: 0 auto; padding: 8px 16px; display: flex; align-items: center; justify-content: center; gap: 22px; }
              nav.subnav a{ display:inline-block; color:#111827; text-decoration:none; padding:6px 2px; border-bottom:2px solid transparent; font-weight:600; font-size:.92rem; }
              nav.subnav a:hover{ border-bottom-color:#111827; }
              nav.subnav a.active{ border-bottom-color:#111827; }
            </style>
            """, unsafe_allow_html=True)

            sub_links = []
            for slabel in SOPORTE_OPCIONES:
                params = {"nav": "Soporte", "snav": slabel, "ing": "1", "sp": "1"}
                href = "./?" + "&".join([f"{k}={quote(v)}" for k, v in params.items()])
                active = " active" if st.session_state.snav == slabel else ""
                sub_links.append(f"<a class='{active}' href='{href}' target='_self'>{slabel}</a>")
            st.markdown(f"<div id='subnav-wrap'><nav class='subnav'>{''.join(sub_links)}</nav></div>", unsafe_allow_html=True)

            st.markdown("<div class='hairline' style='border-top:1px solid #e5e5e7;margin:10px 0 14px 0;'></div>", unsafe_allow_html=True)

            snav = st.session_state.snav
            if snav == "Cargar Ticket":
                st.markdown("### Cargar Ticket")
                with st.form("form_ticket", clear_on_submit=True):
                    col1, col2 = st.columns(2)
                    with col1:
                        email_t = st.text_input("Tu email", value=st.session_state.soporte_user or "")
                        asunto = st.text_input("Asunto")
                        severidad = st.selectbox("Severidad", ["Baja", "Media", "Alta", "Crítica"])
                    with col2:
                        area = st.selectbox("Área", ["Ecommerce", "Finanzas", "Industria", "Infraestructura", "Otro"])
                        archivo = st.file_uploader("Adjuntar archivo (opcional)")
                    descripcion = st.text_area("Descripción del problema", height=160, placeholder="Contanos qué ocurrió, pasos para reproducir, capturas, etc.")
                    enviar = st.form_submit_button("Enviar ticket")
                if enviar:
                    if not (email_t and asunto and descripcion):
                        st.error("Completá email, asunto y descripción.")
                    else:
                        import uuid
                        ticket_id = f"TCK-{uuid.uuid4().hex[:8].upper()}"
                        st.success(f"✅ Ticket creado: **{ticket_id}**")
                        st.info("Nuestro equipo te contactará a la brevedad. Revisá tu email para actualizaciones.")

            elif snav == "Documentación":
                st.markdown("### Documentación")
                doc_cols = st.columns(2)
                with doc_cols[0]:
                    st.markdown("- Introducción a APIs Brandatta")
                    st.markdown("- Integración con ERP (SAP)")
                    st.markdown("- Webhooks: mejores prácticas")
                    st.markdown("- Seguridad y autenticación")
                with doc_cols[1]:
                    st.markdown("- Métricas y monitoreo")
                    st.markdown("- Trazabilidad y tracking")
                    st.markdown("- E-commerce: Checkout & pagos")
                    st.markdown("- Resolución de errores comunes")

            elif snav == "Manuales":
                st.markdown("### Manuales")
                man_cols = st.columns(2)
                with man_cols[0]:
                    st.markdown("- Manual de Operador de Planta")
                    st.markdown("- Manual de Ecommerce (Administrador)")
                    st.markdown("- Manual de Finanzas (Conciliaciones)")
                with man_cols[1]:
                    st.markdown("- Manual de KPIs & Dashboards")
                    st.markdown("- Manual de Gestión de Stock")
                    st.markdown("- Manual de Alertas y SLA")

    st.markdown("</div>", unsafe_allow_html=True)
