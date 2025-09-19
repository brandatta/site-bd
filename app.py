import streamlit as st
from PIL import Image
import base64
from io import BytesIO
from streamlit.components.v1 import html as st_html

# ================== CONFIG ==================
st.set_page_config(page_title="Brandatta - Servicios", layout="wide")

# ================== ESTILOS GLOBALES ==================
st.markdown("""
<style>
  html, body, [data-testid="stAppViewContainer"] { background: #d4fbd7 !important; }
  header {visibility: hidden;}  #MainMenu {visibility: hidden;}  footer {visibility: hidden;}

  /* Tarjetas */
  .card {
    border: 1px solid rgba(0,0,0,0.10);
    border-radius: 18px;
    padding: 18px 16px;
    background: white;
    box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    transition: transform .12s ease, box-shadow .12s ease;
    min-height: 120px;
    display: flex; align-items: center; justify-content: center; text-align: center;
  }
  .card:hover { transform: translateY(-2px); box-shadow: 0 10px 22px rgba(0,0,0,0.08); }
  .card h3 { margin: 0; font-size: 1.05rem; letter-spacing: .2px; }
</style>
""", unsafe_allow_html=True)

# ================== STATE ==================
if "ingresado" not in st.session_state:
    st.session_state.ingresado = False

# Soporte para query params (click del botón HTML)
qp = st.query_params
if not st.session_state.ingresado and qp.get("ing", ["0"])[0] == "1":
    st.session_state.ingresado = True
    try:
        del qp["ing"]
    except Exception:
        pass

# ================== PORTADA (HTML centrado en 800px de alto) ==================
if not st.session_state.ingresado:
    # Pasar logo a base64 para <img>
    try:
        logo = Image.open("logo.png")
        buf = BytesIO()
        logo.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        img_src = f"data:image/png;base64,{b64}"
    except Exception:
        img_src = ""

    st_html(f"""
    <div style="
        height: 100%;
        width: 100%;
        min-height: 100%;
        display: flex;
        align-items: center;
        justify-content: center;">
      <div style="text-align:center; max-width: 90vw;">
        {'<img src="'+img_src+'" alt="logo" style="max-width:220px;width:220px;height:auto;animation: blink 1.6s ease-in-out infinite; display:block; margin:0 auto 16px auto;" />' if img_src else '<div style="font-weight:600;margin-bottom:16px;">Subí <code>logo.png</code></div>'}
        <button id="ingresar"
          style="
            border-radius:999px; padding:11px 18px; font-weight:600;
            border:1px solid rgba(0,0,0,0.15); background:#fff; cursor:pointer;">
          Ingresar
        </button>
      </div>
    </div>
    <style>
      html, body {{
        margin: 0; padding: 0; height: 100%;
        overflow: hidden;
      }}
      @keyframes blink {{
        0% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: .35; transform: scale(1.02); }}
        100% {{ opacity: 1; transform: scale(1); }}
      }}
    </style>
    <script>
      const btn = document.getElementById('ingresar');
      if (btn) {{
        btn.addEventListener('click', () => {{
          const url = new URL(window.top.location);
          url.searchParams.set('ing', '1');
          window.top.location = url.toString();
        }});
      }}
    </script>
    """, height=800)  # ⬅️ altura visible del iframe (podés subir a 900/1000 si querés)
    st.stop()

# ================== HOME (Tarjetas de servicios) ==================
st.markdown("<h2 style='margin:0 0 .6rem 0;text-align:center;'>Servicios</h2>", unsafe_allow_html=True)

servicios = [
    "Consultoría & Discovery",
    "Desarrollo de Aplicaciones",
    "Integraciones (SAP / Ecommerce)",
    "Tableros & Analytics",
    "Automatizaciones & RPA",
    "Soporte & Capacitación",
]

for fila in range(2):
    cols = st.columns(3, gap="large")
    for i, col in enumerate(cols):
        idx = fila*3 + i
        if idx >= len(servicios): continue
        with col:
            st.markdown(f"<div class='card'><h3>{servicios[idx]}</h3></div>", unsafe_allow_html=True)

st.write("")
st.caption("Tip: cambiá los títulos en la lista `servicios` para personalizar las tarjetas.")
