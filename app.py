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
if "servicio_seleccionado" not in st.session_state:
    st.session_state.servicio_seleccionado = None

# ================== HELPERS ==================
def img_to_base64(path):
    try:
        img = Image.open(path)
        buf = BytesIO()
        img.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        return f"data:image/png;base64,{b64}"
    except Exception:
        return ""

def hover_img_html(path, alt="img"):
    b64 = img_to_base64(path)
    if b64:
        return f"<img class='hover-img' src='{b64}' alt='{alt}' />"
    return ""

# ================== CSS ==================
st.markdown("""
<style>
body, [data-testid="stAppViewContainer"] {
    background-color: #fff !important;
    font-family: "Manjari", sans-serif;
}
header, footer {visibility: hidden;}
.services-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    justify-items: center;
}
.tile {
    width: 100%;
    max-width: 400px;
    position: relative;
    transition: transform 0.25s ease;
    cursor: pointer;
}
.tile:hover { transform: translateY(-4px); }
.card {
    background: #fff;
    border: 1px solid #d4fbd7;
    height: 110px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
    border-radius: 10px;
}
.card:hover {
    border-color: #bff3c5;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}
.card h3 {
    font-size: 1.1rem;
    color: #111;
    font-weight: 700;
    margin: 0;
}
.hovercard {
    position: absolute;
    top: 100%;
    left: 50%;
    transform: translateX(-50%);
    background: #fff;
    border: 1px solid #e5e5e7;
    border-radius: 10px;
    padding: 10px 14px;
    width: 90%;
    box-shadow: 0 12px 24px rgba(0,0,0,0.1);
    opacity: 0;
    visibility: hidden;
    transition: all 0.2s ease;
    z-index: 50;
}
.card-wrap:hover .hovercard {
    opacity: 1;
    visibility: visible;
}
.hovercard h4 {
    margin: 6px 0;
    font-size: 1rem;
    font-weight: 700;
}
.hovercard p {
    margin: 0;
    font-size: 0.9rem;
}
.hover-img {
    display:block;
    width:100%;
    max-height:120px;
    object-fit:contain;
    margin:0 0 8px 0;
    border-radius:8px;
}
.detail {
    border: 1px solid #e5e5e7;
    border-radius: 10px;
    padding: 16px 20px;
    box-shadow: 0 10px 24px rgba(0,0,0,0.06);
    background: #fff;
    animation: fadeIn 0.3s ease;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(10px);}
    to {opacity: 1; transform: translateY(0);}
}
.btn-back {
    display:inline-block;
    margin-top:10px;
    padding:8px 12px;
    border:1px solid #ccc;
    border-radius:8px;
    text-decoration:none;
    color:#111;
    background:#fafafa;
}
.btn-back:hover {
    background:#f0f0f0;
}
</style>
""", unsafe_allow_html=True)

# ================== DATA ==================
servicios = [
    {
        "titulo": "APIs",
        "desc1": "Diseño y desarrollo de APIs escalables.",
        "desc2": "Autenticación, rate limiting y monitoreo.",
        "img": "download.png",
        "long": "Diseñamos e implementamos APIs REST y GraphQL con autenticación segura, control de versiones y monitoreo en tiempo real. Integración con gateways corporativos y documentación automatizada (Swagger/OpenAPI)."
    },
    {
        "titulo": "Software para Industrias",
        "desc1": "Sistemas a medida para planta/producción.",
        "desc2": "Integración con ERP y tableros.",
        "img": "download.png",
        "long": "Aplicaciones de planta, captura de datos en línea, OEE, control de calidad, y tableros integrados con SAP y Produmex."
    },
    {
        "titulo": "Tracking de Pedidos",
        "desc1": "Trazabilidad punta a punta.",
        "desc2": "Notificaciones y SLA visibles.",
        "img": "download.png",
        "long": "Desde la carga del pedido hasta la entrega final. Paneles de trazabilidad, métricas de cumplimiento y alertas automáticas."
    },
    {
        "titulo": "Ecommerce",
        "desc1": "Tiendas headless / integradas.",
        "desc2": "Pagos, logística y analytics.",
        "img": "download.png",
        "long": "Arquitecturas headless, integraciones ERP/WMS, gestión avanzada de promociones y experiencia de checkout optimizada."
    },
    {
        "titulo": "Finanzas",
        "desc1": "Forecasting y conciliaciones automáticas.",
        "desc2": "Reportes y auditoría.",
        "img": "download.png",
        "long": "Modelos financieros, conciliación bancaria automatizada, aging y reportería multiempresa."
    },
    {
        "titulo": "Gestión de Stock",
        "desc1": "Inventario en tiempo real.",
        "desc2": "Alertas, valuación y KPIs.",
        "img": "download.png",
        "long": "App móvil para inventario, control por lote y ubicación, reposición y valuación dinámica conectada a ERP."
    },
]

# ================== JS LOGIC ==================
st.markdown("""
<script>
function openSvc(id){
  window.parent.postMessage({ type: "selectService", value: id }, "*");
}
function closeSvc(){
  window.parent.postMessage({ type: "closeService" }, "*");
}
</script>
""", unsafe_allow_html=True)

# ================== BACKEND COMMUNICATION ==================
st.markdown("""
<script>
window.addEventListener("message", (e) => {
  if (e.data.type === "selectService") {
    const svc = e.data.value;
    window.parent.Streamlit.setComponentValue(svc);
  }
  if (e.data.type === "closeService") {
    window.parent.Streamlit.setComponentValue(null);
  }
});
</script>
""", unsafe_allow_html=True)

# ================== RENDER ==================
st.title("Servicios")

seleccionado = st.session_state.servicio_seleccionado

if not seleccionado:
    st.markdown("<div class='services-grid'>", unsafe_allow_html=True)
    for svc in servicios:
        img_html = hover_img_html(svc["img"], svc["titulo"])
        st.markdown(f"""
        <div class='tile' onclick="openSvc('{svc["titulo"]}')">
            <div class='card-wrap'>
                <div class='card'><h3>{svc["titulo"]}</h3></div>
                <div class='hovercard'>
                    {img_html}
                    <h4>{svc["titulo"]}</h4>
                    <p>• {svc["desc1"]}</p>
                    <p>• {svc["desc2"]}</p>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
else:
    svc = next((s for s in servicios if s["titulo"] == seleccionado), None)
    if svc:
        st.markdown(f"""
        <div class='detail'>
            <h3>{svc["titulo"]}</h3>
            <p><b>{svc["desc1"]}</b><br>{svc["desc2"]}</p>
            <p>{svc["long"]}</p>
            <button class='btn-back' onclick="closeSvc()">← Volver</button>
        </div>
        """, unsafe_allow_html=True)
