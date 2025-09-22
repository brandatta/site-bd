import streamlit as st
from PIL import Image
import base64
from io import BytesIO

# ================== CONFIG ==================
st.set_page_config(page_title="Brandatta - Servicios", layout="wide")

# ================== STATE ==================
if "ingresado" not in st.session_state:
    st.session_state.ingresado = False

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

# ================== SERVICIOS ==================
else:
    # ---- Estilos servicios: fondo blanco + tarjetas sobrias ----
    st.markdown("""
    <style>
      [data-testid="stAppViewContainer"] { background: #ffffff !important; }
      header {visibility: hidden;}  #MainMenu {visibility: hidden;}  footer {visibility: hidden;}

      /* Contenedor de ancho máximo para centrar la grilla */
      .wrap {
        max-width: 1180px;
        margin: 0 auto;
      }

      /* Tarjeta sobria: blanca, borde fino y acento lateral sutil */
      .card {
        position: relative;
        background: #ffffff;
        border: 1px solid #d4fbd7;
        border-radius: 16px;
        padding: 20px 18px 18px 22px;
        min-height: 130px;

        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;

        transition: transform .12s ease, box-shadow .12s ease, border-color .12s ease;
        box-shadow: 0 2px 10px rgba(0,0,0,0.03);
      }

      /* Acento lateral izquierdo (muy sutil) */
      .card::before {
        content: "";
        position: absolute;
        left: 0;
        top: 10px;
        bottom: 10px;
        width: 4px;
        border-radius: 6px;
        background: #d4fbd7;
        opacity: 0.9;
      }

      .card:hover {
        transform: translateY(-1px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.06);
        border-color: #c7f6cb; /* leve énfasis en hover */
      }

      .card h3 {
        margin: 0;
        font-size: 1.02rem;
        font-weight: 600;
        letter-spacing: .15px;
        color: #111827; /* gris oscuro, sobrio */
      }

      /* Espaciado entre filas */
      .row-gap { margin-bottom: 14px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='wrap'>", unsafe_allow_html=True)
    st.markdown("<h2 style='margin:0 0 1rem 0; text-align:center; font-weight:700; font-size:1.35rem;'>Servicios</h2>", unsafe_allow_html=True)

    servicios = [
        "Consultoría & Discovery",
        "Desarrollo de Aplicaciones",
        "Integraciones (SAP / Ecommerce)",
        "Tableros & Analytics",
        "Automatizaciones & RPA",
        "Soporte & Capacitación"
    ]

    # 3 x 2 grid (dentro del contenedor centrado)
    for fila in range(2):
        cols = st.columns(3, gap="large")
        for i, col in enumerate(cols):
            idx = fila*3 + i
            if idx >= len(servicios): 
                continue
            with col:
                st.markdown(f"<div class='card'><h3>{servicios[idx]}</h3></div>", unsafe_allow_html=True)
        # separador entre filas en pantallas chicas
        st.markdown("<div class='row-gap'></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)  # cierre .wrap
    st.caption("Tip: cambiá los títulos en la lista `servicios` para personalizar las tarjetas.")
