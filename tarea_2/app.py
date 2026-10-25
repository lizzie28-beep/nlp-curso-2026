from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

BASE = Path(__file__).parent

st.set_page_config(page_title="Tarea 2 – Documentos peruanos", layout="wide")
st.markdown(
    "<h1 style='text-align:center'>¿Pueden convertir documentos escaneados en un archivo de texto estructurado y buscable?</h1>",
    unsafe_allow_html=True,
)
st.write(
    "Pipeline: 25 documentos peruanos (8 impresos, 8 fotos de libros, 9 manuscritos) → "
    "PaddleOCR 3.7.0 (lang=es) → seudonimización → exploración. "
    "**Alcance:** solo Corpus A (documentos). El Corpus B (audio) no se incluyó en esta entrega."
)


@st.cache_data
def leer(nombre):
    ruta = BASE / "datos" / nombre
    return pd.read_csv(ruta) if ruta.exists() else None


docs = leer("documentos.csv")
fuentes = leer("fuentes.csv")
llm = leer("extraccion_llm.csv")

if docs is None:
    st.error("No se encontró datos/documentos.csv")
    st.stop()

docs["texto_ocr"] = docs["texto_ocr"].fillna("")
docs["n_caracteres"] = docs["texto_ocr"].str.len()

st.sidebar.header("Filtros")
todos = sorted(docs["tipo"].unique())
tipos = st.sidebar.multiselect("Tipo de documento", todos, default=todos)
busq = st.sidebar.text_input("Buscar palabra en el texto OCR")

f = docs[docs["tipo"].isin(tipos)]
if busq:
    f = f[f["texto_ocr"].str.contains(busq, case=False, na=False, regex=False)]

tab1, tab2, tab3 = st.tabs(["Resumen", "Documentos", "Audios"])

with tab1:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Documentos procesados", len(docs))
    c2.metric("Coinciden con el filtro", len(f))
    c3.metric("CER (muestra de 10)", "Pendiente")
    c4.metric("Acuerdo LLM vs. humano", "Pendiente")

    if len(f):
        g1 = px.histogram(
            f, x="n_caracteres", color="tipo", nbins=15,
            title="Los impresos concentran los textos más largos del corpus",
        )
        st.plotly_chart(g1, use_container_width=True)
        g2 = px.bar(
            f.groupby("tipo").size().reset_index(name="documentos"),
            x="tipo", y="documentos", title="Documentos por tipo tras el filtro",
        )
        st.plotly_chart(g2, use_container_width=True)
    else:
        st.info("Ningún documento coincide con los filtros.")

    mostrar = f[["id", "tipo", "fuente", "n_caracteres"]]
    st.dataframe(mostrar, use_container_width=True)
    st.download_button(
        "Descargar tabla (CSV)",
        mostrar.to_csv(index=False).encode("utf-8"),
        "documentos_filtrados.csv",
        "text/csv",
    )
    st.caption("CER, Tesseract, extracción con LLM y auditoría quedaron pendientes en esta entrega.")

with tab2:
    if len(f) == 0:
        st.info("Ningún documento coincide con los filtros.")
    else:
        sel = st.selectbox("Documento", f["id"].tolist())
        fila = docs[docs["id"] == sel].iloc[0]
        st.write(f"**Tipo:** {fila['tipo']} | **Modelo:** {fila['modelo_ocr']}")
        st.write(f"**Fuente:** {fila['fuente']}")

        texto = fila["texto_ocr"]
        if fila["tipo"] == "foto" or sel in ("doc_003", "doc_004", "doc_005"):
            texto = texto[:300] + " […]"
            st.caption("Fragmento corto: el texto original tiene derechos de autor.")
        st.text_area("Texto OCR (seudonimizado)", texto, height=250)

        ref = fila.get("texto_referencia", "")
        if isinstance(ref, str) and ref.strip():
            st.text_area("Texto de referencia", ref, height=150)
        else:
            st.caption("Sin referencia manual (no forma parte de la muestra de evaluación).")

        img = BASE / "datos" / "ejemplos" / f"{sel}.jpg"
        if img.exists():
            st.image(str(img))

        if llm is not None and sel in llm["id"].values:
            st.json(llm[llm["id"] == sel].iloc[0]["campos_json"])

with tab3:
    st.info("El Corpus B (audio) no se incluyó en esta entrega, por lo que no hay transcripciones ni WER.")