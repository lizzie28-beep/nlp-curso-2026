# Tarea 1 – Clasificador de Noticias Peruanas

## Pregunta del proyecto
¿Pueden los titulares de diarios peruanos clasificarse automáticamente por categoría?

## 📰 Medios y fechas de extracción
- **La República** (`larepublica.pe`) — 200 noticias — Recolectado el 2026-10-18
- **El Comercio** (`elcomercio.pe`) — 200 noticias — Recolectado el 2026-10-18
- **Categorías:** politica, economia, deportes, ciencia_tecnologia

## 🔍 Hallazgos analíticos
1. El Comercio genera más contenido digital en todas las categorías, especialmente en Política, mientras La República tiene cobertura más equilibrada entre categorías.
2. El Comercio usa titulares más largos y descriptivos (+300 caracteres) mientras La República tiende a ser más directa y concisa, lo que refleja diferencias editoriales entre ambos medios.

## ⚠️ Limitaciones técnicas
1. Los sitios web cargan contenido dinámicamente con JavaScript, lo que limita el scraping a las noticias visibles en el HTML estático, impidiendo acceder a archivos históricos completos.
2. El modelo zero-shot en español tiene bajo rendimiento (F1=0.485) porque fue entrenado principalmente en inglés, lo que justifica el fine-tuning con datos locales.

## 🚀 Cómo ejecutar

### Instalar dependencias
```bash
pip install -r requirements.txt
```

### Ejecutar notebooks
Abrir en orden:
1. `01_recoleccion.ipynb`
2. `02_clasificacion.ipynb`

### Ejecutar dashboard
```bash
streamlit run app.py
```

## 📊 Resultados del modelo
| Métrica | Valor |
|---------|-------|
| F1 Macro (Test) | 0.766 |
| Zero-shot F1 | 0.485 |
| Acuerdo LLM-Humano | 9/20 (45%) |