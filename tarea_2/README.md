# Tarea 2 – Documentos peruanos: del archivo escaneado al texto buscable

## Pregunta del proyecto
¿Pueden convertir documentos escaneados en un archivo de texto estructurado y buscable?

## Alcance (declaración honesta)
Esta entrega cubre **únicamente el Corpus A (documentos)**. No se recolectó audio, por lo que no hay ASR, diarización ni WER; `datos/transcripciones.csv` existe con sus columnas y sin filas.

**Pendiente (no alcanzado por tiempo):** referencias manuales de 10 documentos, CER, comparación con Tesseract, extracción con LLM (`extraccion_llm.csv`), auditoría de 20 casos y `02_evaluacion.ipynb`.

## Dashboard público
https://tarea2-documentos.streamlit.app/

## Corpus A: 25 documentos
| Tipo | Cantidad | Origen |
|---|---|---|
| Impreso | 8 | Constitución (OEA), artículos del CIUP y tesis de la Universidad del Pacífico, sentencia del TC (copia LP Derecho), plan del MINAM |
| Foto | 8 | Fotos propias de páginas de libros de terceros |
| Manuscrito | 9 | Textos ficticios escritos a mano |

Fuentes, licencias y fecha de extracción (25/10/2026): `datos/fuentes.csv`.

## Metodología
- OCR: PaddleOCR 3.7.0 (lang=es), Python 3.11.17, CPU, sin oneDNN. Sin preprocesamiento adicional: se desactivaron la orientación de documento, la corrección de deformación y la orientación de línea.
- Seudonimización: patrones (DNI, teléfono, correo) y lista de nombres. Entidades reemplazadas: DNI 0, teléfonos 0, correos 1, personas 4. **La revisión manual fue parcial.**
- Limpieza: sin duplicados ni documentos vacíos (mínimo 490 caracteres de texto).

## Hallazgos
1. Los impresos aportan más texto por página (promedio ≈3 088 caracteres) que las fotos (≈1 320) y los manuscritos (≈1 719).
2. El OCR devolvió texto en los 25 documentos. Sin referencias manuales no se mide su exactitud.

## Limitaciones
1. Licencia de reutilización no verificada en doc_003, doc_004 y doc_005 (acceso abierto, sin licencia visible): se usan solo para OCR y se muestran fragmentos cortos. Los textos de libros (fotos) tienen derechos de autor y se muestran truncados.
2.  No medí qué tan bien lee el OCR. Para eso hay que escribir a mano el texto correcto de cada documento y compararlo con lo que sacó el programa, y no alcancé a hacerlo. Además, mis 8 "fotos" son páginas de libros escaneadas y pueden haber salido derechas y con buena luz, sin las sombras o la inclinación que la tarea pide para ese tipo.

## Uso de IA
Asistente: Claude (chat). Capturas en `evidencias_ia/`.

## Ejecutar en local
```bash
pip install -r requirements.txt
streamlit run app.py
```