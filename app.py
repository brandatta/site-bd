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
    # ---- Estilos portada (Apple-ish: aire, tipografía sistema, monocromo) ----
    st.markdown("""
    <style>
      :root {
        --hairline: #e5e5e7;          /* línea finita tipo Apple */
        --text: #1d1d1f;              /* texto principal Apple */
        --bg-hero: #d4fbd7;           /* tu verde suave de portada */
      }
      html, body, [data-testid="stAppViewContainer"] {
        background: var(--bg-hero) !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display",
                     system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        color: var(--text);
      }
      header {visibility: hidden;}  #MainMenu {visibility: hidden;}  footer {visibility: hidden;}

      @keyframes blink {
        0% { opacity: 1; transform: scale(1); }
        50% { opacity: .35; transform: scale(1.02); }
        100% { opacity: 1; transform: scale(1); }
      }

      /* Contenedor centrado con aire vertical */
      .hero-wrap {
        min-height: 86vh;
        display: flex; flex-direction: column;
        align-items: center; justify-content: center;
        text-align: center;
        gap: 18px;
      }

      /* Logo (220px) con titilado sutil */
      .hero-wrap img {
        width: 220px; max-width: 220px; height: auto;
        animation: blink 1.6s ease-in-out infinite;
      }

      /* Botón estilo Apple (bordes rectos, outline suave) */
      .cta {
        display: inline-flex; align-items: center; justify-content: center;
        height: 40px; padding: 0 18px;
        border: 1px solid var(--hairline);
        background: #fff;
        color: var(--text);
        font-weight: 600; letter-spacing: -0.01em;
        border-radius: 0;                /* recto como pediste */
        transition: background .18s ease, transform .18s ease, border-color .18s ease;
        cursor: pointer; user-select: none;
      }
      .cta:hover { background: #f5f5f7; transform: translateY(-1px); border-color: #d0d0d4; }
      .cta:active { transform: translateY(0); }
    </style>
    """, unsafe_allow_html=True)

    # ---- Logo + botón en el mismo bloque (botón debajo del logo) ----
    try:
        logo = Image.open("logo.png")
        buf = BytesIO(); logo.save(buf, format="PNG")
        b64 = base64.b64encode(buf.getvalue()).decode()
        logo_html = f"<img src='data:image/png;base64,{b64}' alt='logo'/>"
    except Exception:
        logo_html = "<div style='font-weight:600;'>Subí <code>logo.png</code> a la carpeta de la app.</div>"

    st.markdown(f"""
    <div class="hero-wrap">
      {logo_html}
      <div>
        <button class="cta" id="ingresar-btn">Ingresar</button>
      </div>
    </div>
    <script>
      const btn = document.getElementById('ingresar-btn');
      if (btn) {{
        btn.addEventListener('click', () => {{
          const el = window.parent.document.querySelector('button[kind="secondary"]') || null;
          // No dependemos de hacks: el click real lo maneja Streamlit en Python (debajo).
        }});
      }}
    </script>
    """, unsafe_allow_html=True)

    # Botón real de Streamlit (para estado) oculto visualmente pero activado por el usuario
    # Nota: mantenemos el botón visible también para máxima compatibilidad y accesibilidad.
    if st.button("Ingresar"):
        st.session_state.ingresado = True

# ================== SERVICIOS (Apple-like minimal) ==================
else:
    st.markdown("""
    <style>
      :root {
        --hairline: #e5e5e7;
        --text: #1d1d1f;
      }
      [data-testid="stAppViewContainer"] {
        background: #ffffff !important;
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display",
                     system-ui, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
        color: var(--text);
      }
      header {visibility: hidden;}  #MainMenu {visibility: hidden;}  footer {visibility: hidden;}

      /* Contenedor centrado con ancho contenido (Apple usa mucho aire) */
      .wrap {
        max-width: 1200px;
        margin: 0 auto;
        padding: 24px 12px 50px;
      }

      /* Título sobrio, tracking leve negativo */
      .title {
        text-align: center;
        font-weight: 700;
        font-size: 28px;
        letter-spacing: -0.02em;
        margin: 6px 0 32px 0;
      }

      /* Tile cuadrado minimal, bordes rectos, hairline */
      .tile {
        width: 150px;                 /* más chico */
        margin: 0 auto;               /* centrado dentro de la columna */
      }
      @media (max-width: 860px) { .tile { width: 140px; } }
      @media (max-width: 640px) { .tile { width: 130px; } }

      .card {
        width: 100%;
        aspect-ratio: 1 / 1;          /* cuadrado perfecto */
        background: #ffffff;
        border: 1px solid var(--hairline);
        border-radius: 0;              /* bordes rectos */
        display: flex; align-items: center; justify-content: center; text-align: center;
        transition: transform .2s cubic-bezier(.2,.8,.2,1), background .2s ease, border-color .2s ease;
      }
      .card:hover { transform: translateY(-2px) scale(1.015); background: #fafafa; border-color: #d8d8dc; }

      .label {
        margin: 0;
        font-size: 15px;
        font-weight: 600;
        letter-spacing: -0.01em;
        color: var(--text);
      }

      /* Separación vertical marcada entre filas (Apple usa mucho aire) */
      .row-spacer { height: 48px; }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="wrap">', unsafe_allow_html=True)
    st.markdown('<div class="title">Servicios</div>', unsafe_allow_html=True)

    servicios = [
        "Consultoría & Discovery",
        "Desarrollo de Aplicaciones",
        "Integraciones (SAP / Ecommerce)",
        "Tableros & Analytics",
        "Automatizaciones & RPA",
        "Soporte & Capacitación"
    ]

    # Fila 1
    cols = st.columns(3, gap="large")
    for i, col in enumerate(cols):
        with col:
            st.markdown(f"""
            <div class="tile">
              <div class="card"><p class="label">{servicios[i]}</p></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="row-spacer"></div>', unsafe_allow_html=True)

    # Fila 2
    cols2 = st.columns(3, gap="large")
    for j, col in enumerate(cols2):
        idx = 3 + j
        with col:
            st.markdown(f"""
            <div class="tile">
              <div class="card"><p class="label">{servicios[idx]}</p></div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.caption("Tip: cambiá los títulos en la lista `servicios` para personalizar las tarjetas.")
