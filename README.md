# Estadística para tu tesis con Jamovi (+ Python)

Datos y recursos del curso **Estadística para tu tesis con Jamovi** de **Danlara learning**.
Aquí están los conjuntos de datos para que practiques exactamente lo que ves en el curso.

## Contenido
```
datos/
  datos.csv            · dataset principal (limpio, 120 casos)
  datos_crudos.csv     · versión "sucia" para la lección de limpieza (Módulo 2)
  datos_proyecto.csv   · dataset del proyecto final (90 casos)
diccionario-variables.md · qué significa cada variable
notebooks/
  analisis_python.ipynb · pista opcional en Python (pandas + pingouin)
generadores/             · scripts que generan los datos (reproducibilidad)
```

## Cómo usar los datos

**En Jamovi (recomendado para empezar):**
1. Descarga `datos/datos.csv` (botón verde *Code → Download ZIP*, o clic en el archivo → *Download*).
2. En Jamovi: menú ☰ → *Open* → *This PC* → elige el `.csv`.

**En Python / Google Colab (pista opcional):**
- Abre el cuaderno directamente en Colab:
  https://colab.research.google.com/github/lara-montano/estadistica-para-tu-tesis-jamovi/blob/main/notebooks/analisis_python.ipynb
- O carga los datos por URL sin descargar nada:
  ```python
  import pandas as pd
  url = "https://raw.githubusercontent.com/lara-montano/estadistica-para-tu-tesis-jamovi/main/datos/datos.csv"
  df = pd.read_csv(url)
  ```

## El dataset principal (`datos.csv`)
Estudio del **efecto de un método de aprendizaje sobre el desempeño**. 120 participantes en
tres grupos (Control / Método A / Método B), con medición antes y después, horas de práctica,
motivación, satisfacción, una escala de 5 ítems (`util_1`…`util_5`) y la variable `aprobado`.
Sirve para practicar: descriptiva, prueba t, ANOVA, correlación, regresión, chi-cuadrado y
fiabilidad (alfa de Cronbach). Detalle completo en [`diccionario-variables.md`](diccionario-variables.md).

`datos_proyecto.csv` es un escenario distinto (programa de ejercicio → bienestar) para el
proyecto final.

## Reproducibilidad
Los datos se generan con semilla fija; puedes regenerarlos idénticos:
```bash
python3 generadores/generar_datos.py      # crea datos.csv y datos_crudos.csv
python3 generadores/generar_proyecto.py   # crea datos_proyecto.csv
```

## Licencia
Datos sintéticos para fines educativos. Uso libre para aprender y enseñar (CC BY 4.0).
Curso © Danlara learning.
