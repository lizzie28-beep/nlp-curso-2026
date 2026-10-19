import streamlit as st
import pandas as pd
import plotly.express as px
import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import numpy as np

st.set_page_config(
    page_title="Clasificador de Noticias Peruanas",
    page_icon="🗞️",
    layout="wide"
)

@st.cache_data
def cargar_datos():
    return pd.read_csv("datos/noticias.csv")

@st.cache_resource
def cargar_modelo():
    tokenizer = AutoTokenizer.from_pretrained("modelo/")
    model = AutoModelForSequenceClassification.from_pretrained("modelo/")
    model.eval()
    return tokenizer, model

df = cargar_datos()
tokenizer, model = cargar_modelo()

ID2LABEL = {0: "politica", 1: "economia", 2: "deportes", 3: "ciencia_tecnologia"}

st.title("🗞️ ¿Pueden los titulares peruanos clasificarse automáticamente?")
st.markdown("Dashboard de clasificación de noticias de **La República** y **El Comercio** usando DistilBERT fine-tuned.")
st.divider()

# Sidebar
st.sidebar.header("Filtros")
medios = ["Todos"] + sorted(df["medio"].unique().tolist())
medio_sel = st.sidebar.selectbox("Medio", medios)
cats = ["Todas"] + sorted(df["etiqueta"].unique().tolist())
cat_sel = st.sidebar.selectbox("Categoria", cats)

df_f = df.copy()
if medio_sel != "Todos":
    df_f = df_f[df_f["medio"] == medio_sel]
if cat_sel != "Todas":
    df_f = df_f[df_f["etiqueta"] == cat_sel]

# Métricas
col1, col2, col3 = st.columns(3)
col1.metric("Noticias recolectadas", f"{len(df):,}")
col2.metric("F1 Macro (Test)", "0.766")
col3.metric("Acuerdo LLM-Humano", "9/20 = 45%")

st.divider()

# Gráfico
st.subheader("Distribución de categorías")
conteo = df_f.groupby(["etiqueta","medio"]).size().reset_index(name="cantidad")
fig = px.bar(conteo, x="etiqueta", y="cantidad", color="medio", barmode="group",
             labels={"etiqueta": "Categoria", "cantidad": "Noticias"})
st.plotly_chart(fig, use_container_width=True)

# Tabla
st.subheader("Datos recolectados")
st.dataframe(df_f[["titular","medio","etiqueta","fecha","url"]], 
             use_container_width=True, height=300)
csv_bytes = df_f.to_csv(index=False).encode("utf-8")
st.download_button("Descargar CSV", csv_bytes, "noticias_filtrado.csv", "text/csv")

st.divider()

# Probador en vivo
st.subheader("Probador interactivo")
titular_input = st.text_input(
    "Escribe un titular de noticia peruana:",
    placeholder="Ej: Congreso debate nueva ley de pensiones"
)

if st.button("Clasificar"):
    if titular_input.strip():
        inputs = tokenizer(
            titular_input, return_tensors="pt",
            truncation=True, padding="max_length", max_length=128
        )
        with torch.no_grad():
            logits = model(**inputs).logits
        probs = torch.softmax(logits, dim=-1)[0].numpy()
        pred_id = int(np.argmax(probs))
        pred_label = ID2LABEL[pred_id]
        confianza = float(probs[pred_id])

        st.success(f"Categoria predicha: {pred_label}")
        st.progress(confianza, text=f"Confianza: {confianza:.1%}")

        prob_df = pd.DataFrame({
            "Categoria": [ID2LABEL[i] for i in range(4)],
            "Probabilidad": [float(probs[i]) for i in range(4)]
        }).sort_values("Probabilidad", ascending=False)
        st.bar_chart(prob_df.set_index("Categoria"))
    else:
        st.warning("Por favor ingresa un titular.")

st.divider()
st.caption("Tarea 1 - Opcion C Comparada | Curso NLP | 2026")