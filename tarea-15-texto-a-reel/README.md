# Tarea 15: del texto a mi voz

**Texto usado:** Reporte Mensual de Conflictos Sociales N.° 271 (setiembre 2026), Defensoría del Pueblo.

## Pipeline
1. PDF leído con pypdf
2. Guion en JSON generado con Claude
3. Revisión humana contra el PDF
4. Voz clonada con Qwen3-TTS 0.6B
5. Subtítulos con Whisper; video con Pillow y ffmpeg

Todo corrió en Google Colab (GPU T4).

## Qué revisé y corregí del guion
- Cifras verificadas en el PDF: 193, 74.6 %, 47.2 %, 28.5 %, 151 y 257.
- Evité datos del PDF que salieron desordenados al extraer el texto.

_Voz generada con IA._