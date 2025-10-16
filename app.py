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
sel_qp  = unquote(qp.get("sel")) if qp.get("sel") else None  # compat

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
    st.markdown("""
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Manjari:wght@100;400;700&display=swap');
      [data-testid="stAppViewContainer"] { background:#fff !important; font-family:'Manjari', system-ui, sans-serif !important; }
      header, #MainMenu, footer {visibility: hidden;}
      .block-container, [data-testid="block-container"]{ padding-top: 0 !important; padding-bottom: 0 !important; }
      [data-testid="stAppViewContainer"]{ padding-top: 0 !important; }

      /* ===== Header sticky con logo ===== */
      #topnav-wrap{ position: sticky; top: 0; z-index: 1000; background: #ffffff; border-bottom: 1px solid #e5e5e7; box-shadow: 0 1px 6px rgba(0,0,0,.04); margin-top: 0 !important; }
      nav.topnav{ max-width: 1440px; margin: 0 auto; padding: 8px 16px !important; display: flex; align-items: center; justify-content: space-between; gap: 16px; position: relative; }
      .nav-left{ display:flex; align-items:center; gap:10px; min-width: 200px; }
      .nav-center{ position:absolute; left:50%; transform:translateX(-50%); display:flex; gap:28px; align-items:center; }
      .nav-right{ min-width: 200px; }
      #brand-logo{ height: 70px; width: auto; display:block; }
      @media (max-width: 1200px){ #brand-logo{ height: 52px; } .nav-left, .nav-right { min-width: 180px; } }
      @media (max-width: 900px){ #brand-logo{ height: 44px; } .nav-left, .nav-right { min-width: 160px; } }
      @media (max-width: 640px){ #brand-logo{ height: 36px; } .nav-left, .nav-right { min-width: 120px; } }
      .nav-center a{ color: #0f0f0f; text-decoration: none; padding: 8px 2px; border-bottom: 2px solid transparent; text-transform: uppercase; font-weight: 700; font-size: .95rem; transition: border .15s; white-space: nowrap; }
      .nav-center a:hover{ border-bottom-color: #0f0f0f; }
      .nav-center a.active{ border-bottom-color: #0f0f0f; }

      /* ===== Grilla de Servicios ===== */
      .services-area { max-width: 1320px; margin: 20px auto 12px; }
      .services-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
        gap: 24px;
        justify-items: center;
        transition: transform .25s ease;
      }

      .tile { width: 100%; max-width: 420px; position: relative; overflow: visible !important; z-index: 0; cursor:pointer; }
      .tile:hover { z-index: 200; transform: translateX(-6px); transition: transform .2s ease; }
      .card-wrap { position: relative; overflow: visible !important; }
      .card { background:#fff; border:1px solid #d4fbd7; height:110px; display:flex; align-items:center; justify-content:center; transition:all .15s ease; box-sizing: border-box; border-radius:10px; }
      .card:hover{ border-color:#bff3c5; box-shadow:0 10px 24px rgba(0,0,0,.06); }
      .card h3{ font-size:1.05rem; font-weight:700; color:#111; margin:0; }

      /* Hovercard (solo imagen arriba) */
      .hovercard{
        position:absolute; left:50%;
        background:rgba(255,255,255,0.97); backdrop-filter:blur(6px);
        border:1px solid #e5e5e7; border-radius:10px; padding:10px 14px;
        opacity:0; visibility:hidden; transition:opacity .15s, transform .15s;
        z-index: 300; box-shadow:0 12px 28px rgba(0,0,0,0.14);
        pointer-events: none; width: max(280px, 60%);
        text-align:left;
      }
      .card-wrap:hover .hovercard{ opacity:1; visibility:visible; }
      .hover-up{ bottom:calc(100% + 8px); transform:translateX(-50%) translateY(6px); }
      .card-wrap:hover .hover-up{ transform:translateX(-50%) translateY(0); }
      .hover-down{ top:calc(100% + 8px); transform:translateX(-50%) translateY(-6px); }
      .card-wrap:hover .hover-down{ transform:translateX(-50%) translateY(0); }
      .hover-img{ display:block; width:100%; max-height:120px; object-fit:contain; margin:0; background:#fff; border:1px solid #eef2f3; border-radius:8px; }

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

      @keyframes fadeIn {
        from {opacity:0; transform: translateY(8px);}
        to   {opacity:1; transform: translateY(0);}
      }
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

        # Definición de servicios (sin desc1/desc2)
        servicios = [
            {
                "id": "interfaces",
                "titulo": "Interfaces",
                "img": "download.png",
                "long": """Diseñamos y desarrollamos interfaces para la integración de sistemas empresariales heterogéneos, garantizando la coherencia, seguridad y trazabilidad de los datos a lo largo de todo el ecosistema tecnológico de la organización.

Con una trayectoria consolidada y cientos de interfaces desarrolladas en diversos entornos productivos, contamos con la experiencia necesaria para abordar escenarios de integración complejos, multiempresa y multiplataforma.

Nuestras soluciones permiten la interoperabilidad entre plataformas ERP, e-commerce, sistemas logísticos y servicios en la nube, asegurando la continuidad operativa y reduciendo la intervención manual en los flujos de información.

Utilizamos arquitecturas basadas en APIs REST, SOAP, conectores ODBC/JDBC y microservicios, diseñadas según los requerimientos de cada entorno y alineadas con las mejores prácticas de escalabilidad, versionado y monitoreo.

Con una visión de mantenimiento evolutivo, damos soporte tanto transacciones en tiempo real como procesos batch controlados, incorporando mecanismos de validación, auditoría y recuperación ante fallos.

Ejemplos de integraciónes:

SAP ↔ WooCommerce / Planexware / Mercado Libre

Sincronización bidireccional de pedidos, facturación y stock

Interfaces contables y de cobranza entre ERP y sistemas externos

Captura automática de datos desde terminales o dispositivos IoT

Consolidación de datos operativos en entornos analíticos y dashboards

Nuestro Objetivo Técnico:
Garantizar un flujo de información unificado, confiable y auditable entre los distintos sistemas críticos de la empresa, bajo un esquema modular, escalable y mantenible."""
            },
            {
                "id": "industria",
                "titulo": "Producción Industrial",
                "img": "download.png",
                "long": """Desarrollamos soluciones tecnológicas orientadas a la digitalización, trazabilidad y control operativo de procesos industriales, integrando datos en tiempo real desde planta, ERP, sistemas periféricos y archivos ad-hoc.

Nuestras herramientas permiten monitorear, registrar y optimizar la producción mediante la captura automatizada de información desde líneas, equipos y operadores, generando visibilidad completa sobre la eficiencia, el rendimiento y el cumplimiento de estándares productivos.

Conectando sensores, terminales de producción, sistemas de gestión de calidad, control de stock y mantenimiento, generamos una integración continua entre los multiples sectores de la empresa que consumen y analizan la informacion de planta.

Implementamos módulos específicos para seguimiento de órdenes de producción, control de paradas, gestión de lotes, trazabilidad de materiales y análisis de OEE (Overall Equipment Effectiveness), con tableros configurables que consolidan los indicadores clave de desempeño en tiempo real.

Características técnicas destacadas:

Integración directa con el ERP

Captura automática de datos desde terminales o dispositivos IoT

Modelos de datos normalizados para análisis histórico y predictivo

Protocolos seguros de comunicación y redundancia de información

Implementación bajo esquemas modulares y escalables

Nuestro Objetivo Técnico:
Brindar una infraestructura digital sólida para la gestión integral de la producción industrial, que garantice trazabilidad, disponibilidad de datos en tiempo real y soporte a la toma de decisiones basada en información confiable."""
            },
            {
                "id": "fuerza",
                "titulo": "Fuerza de Ventas",
                "img": "download.png",
                "long": """Desarrollamos plataformas y herramientas diseñadas para gestionar, monitorear y optimizar la operación comercial de las organizaciones, integrando en un mismo entorno la información proveniente de ERP, CRM, e-commerce, sistemas logísticos y módulos documentales.

Con el objetivo de abastecer integralmente las necesidades de informacion a consumir por los equipos de ventas, contemplamos desde la planificación de objetivos y seguimiento de desempeño hasta la automatización de pedidos, cotizaciones, cobranzas y reportes en tiempo real.

Implementamos entornos web y móviles adaptados a los diferentes perfiles de usuario —vendedores, supervisores, gerentes y back-office— garantizando acceso seguro, disponibilidad permanente y sincronización bidireccional con sistemas centrales.

Incorporamos además mecanismos de integración documental que permiten vincular automáticamente cotizaciones, órdenes, remitos y facturas dentro del flujo comercial, asegurando trazabilidad completa entre documentos y su correspondencia en el ERP.

Los desarrollos incluyen módulos de seguimiento de clientes, condiciones comerciales, histórico de ventas, control de cartera, análisis de rentabilidad y métricas de desempeño, todo sobre una base de datos centralizada y auditable.

Características técnicas destacadas:

Integración directa con el ERP

Sincronización online/offline con dispositivos móviles

APIs de conexión con plataformas e-commerce, pasarelas de pago y sistemas documentales

Arquitectura modular con control de accesos por roles y niveles jerárquicos

Dashboards analíticos para monitoreo de desempeño individual y global

Nuestr Objetivo técnico:
Proveer una plataforma robusta y escalable que centralice la gestión comercial, asegure la integridad de la información y brinde visibilidad completa sobre la operación de ventas, integrando la documentación transaccional para una trazabilidad comercial total."""
            },
            {
                "id": "ecommerce",
                "titulo": "E-commerce",
                "img": "download.png",
                "long": """Desarrollamos y administramos plataformas de comercio electrónico B2B integradas con los sistemas centrales de gestión empresarial, garantizando la consistencia de precios, stock, condiciones comerciales y documentación transaccional en tiempo real.

Nuestras soluciones de e-commerce están diseñadas para operar sobre entornos complejos, multiempresa y multilistado, con una arquitectura capaz de sincronizar información proveniente de ERP, catálogos externos y sistemas logísticos.

Proveemos una plataforma avanzada de gestión de promociones y reglas comerciales, que permite modelar estructuras complejas de descuentos, bonificaciones y condiciones dinámicas según múltiples variables:
cliente, rol, lista de precios, familia de productos, tipo de pedido, fechas de vigencia y prioridades combinadas.

Estas promociones se procesan mediante un motor lógico parametrizable que puede operar tanto de forma automática (auto-aplicación de cupones o reglas) como manual, respetando las políticas comerciales y segmentaciones definidas por la organización.

El sistema incluye además mecanismos de control y auditoría que garantizan la trazabilidad completa de cada promoción, desde su definición hasta su aplicación efectiva en los pedidos y documentos asociados.

Características técnicas destacadas:

Integración directa con el ERP

Sincronización bidireccional de precios, stock, pedidos y facturación

Motor de reglas para gestión dinámica de promociones y condiciones comerciales

Soporte para múltiples roles, listas de precios y jerarquías de clientes

Integración con gateways de pago, logística y sistemas documentales

Arquitectura modular y escalable con monitoreo de transacciones y logs de aplicación

Objetivo técnico:
Ofrecer una infraestructura de comercio electrónico totalmente integrada, capaz de administrar en tiempo real la información comercial, los flujos transaccionales y la aplicación controlada de promociones complejas, asegurando precisión, coherencia y trazabilidad en cada operación."""
            },
            {
                "id": "finanzas",
                "titulo": "Finanzas",
                "img": "download.png",
                "long": """Desarrollamos soluciones orientadas a la automatización, integración y control de los procesos financieros y contables, garantizando la coherencia y trazabilidad de la información entre los distintos sistemas corporativos.

Nuestras herramientas permiten consolidar en tiempo real los datos provenientes de ERP, bancos, sistemas de cobranzas, plataformas de facturación electrónica y portales de clientes, brindando una visión unificada del estado financiero de la organización.

Diseñamos módulos y dashboards que asisten en la gestión de cuentas corrientes, conciliaciones, aging de saldos, proyecciones de flujo de fondos y análisis de rentabilidad, incorporando modelos de datos estructurados para seguimiento histórico, auditoría y análisis predictivo.

Implementamos interfaces financieras robustas que sincronizan movimientos entre SAP, sistemas externos de facturación o cobro, y fuentes de datos auxiliares, asegurando consistencia contable y reducción de carga operativa.

Además, nuestras soluciones integran mecanismos de alertas automáticas, conciliaciones parametrizables y reglas de negocio configurables, permitiendo detectar desvíos, anticipar vencimientos y facilitar la toma de decisiones sobre base informada.

Algunos de nuestros Entregables:

Dashboards de aging, cobranzas y flujo de fondos consolidado

Interfaces de facturación electrónica y conciliación automática de pagos

Modelos de datos financieros normalizados y auditables

Automatización de reportes y generación de indicadores financieros clave

Control de acceso por roles y registro completo de operaciones

Objetivo técnico:
Proveer una infraestructura financiera integrada, auditable y en tiempo real, que unifique los procesos contables, bancarios y de cobranza, reduciendo la intervención manual y fortaleciendo la confiabilidad de la información económica de la empresa."""
            },
            {
                "id": "stock",
                "titulo": "Gestión de Stock",
                "img": "download.png",
                "long": """Gestión Integral de Stock

Desarrollamos soluciones tecnológicas para la administración, control y trazabilidad completa del inventario, integrando en tiempo real los movimientos físicos y contables entre sistemas ERP, plataformas logísticas, e-commerce y herramientas operativas de planta o depósito.

Nuestras aplicaciones permiten gestionar el ciclo completo del stock, desde la recepción de materiales hasta la expedición del producto final, contemplando control de ubicaciones, lotes, series, vencimientos y políticas de rotación.

Uno de los pilares de nuestra solución es la aplicación móvil de gestión de stock, utilizada diariamente en entornos operativos de alta demanda.
Diseñada para terminales industriales o dispositivos móviles convencionales, permite registrar movimientos, conteos, transferencias y ajustes en tiempo real, incluso en modo offline, sincronizando automáticamente con los sistemas centrales una vez restablecida la conexión.

La app se integra de forma nativa con los módulos ERP y WMS, reduciendo la carga administrativa y asegurando la consistencia de los datos entre el inventario físico y el inventario contable.
Incluye además mecanismos de validación, control de usuario, lectura de códigos de barras y reportes instantáneos de disponibilidad y movimientos.

Características técnicas destacadas:

Integración directa con el ERP

Aplicación móvil con soporte online/offline y sincronización automática

Control de lotes, series, vencimientos y ubicaciones (bin locations)

Interfaces con sistemas de gestión de depósitos (WMS) y producción (MES)

Dashboards de stock valorizado, cobertura y rotación

Monitoreo en tiempo real de movimientos, transferencias y ajustes

Nuestr Objetivo técnico:
Proveer una plataforma integral para la gestión de stock que combine infraestructura centralizada con herramientas móviles operativas, garantizando trazabilidad total, coherencia contable y disponibilidad de información en tiempo real."""
            },
        ]

        # Contenedor de tarjetas
        st.markdown("<div class='services-area'>", unsafe_allow_html=True)

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
      <p>{svc["long"].replace(chr(10), "<br/>")}</p>
      <div style='margin-top:10px;display:flex;gap:10px;flex-wrap:wrap;'>
        <a href='#' class='modal-close'>Cerrar</a>
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
