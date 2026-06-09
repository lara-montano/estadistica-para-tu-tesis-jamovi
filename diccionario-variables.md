# Diccionario de variables

Dataset hilo conductor del Curso 01. Escenario: efecto de un **método de
aprendizaje/capacitación** (Control / Método A / Método B) sobre el **desempeño**.
n = 120 (40 por grupo). Reproducible con `generar_datos.py` (sin dependencias).

## Dos versiones del archivo
- **`datos_crudos.csv`** — materia prima realista para el **Módulo 2 (limpieza)**:
  etiquetas inconsistentes, valores imposibles, Likert fuera de rango, id
  duplicado, faltantes codificados (99 / NA) y filas basura. 122 filas.
- **`datos.csv`** — versión **limpia**, lista para analizar (la de todas las
  demos). 120 filas. Limpiar el crudo reproduce este archivo.

## Variables
| Variable | Descripción | Tipo | Nivel | Valores |
|---|---|---|---|---|
| `id` | Identificador | Entero | Nominal | 1–120 |
| `grupo` | Método recibido | Texto | Nominal (3) | Control · Método A · Método B |
| `sexo` | Sexo autoinformado | Texto | Nominal | Hombre · Mujer · Otro |
| `edad` | Edad (años) | Entero | Escala | 18–45 |
| `experiencia_previa` | Experiencia previa (años) | Entero | Escala | 0–~9 |
| `desempeno_pre` | Desempeño antes | Entero | Escala | 0–100 |
| `desempeno_post` | Desempeño después (DV principal) | Entero | Escala | 0–100 |
| `horas_practica` | Horas de práctica | Decimal | Escala | 0–~21 |
| `motivacion` | Motivación (ítem Likert) | Entero | Ordinal | 1–5 |
| `satisfaccion` | Satisfacción global (ítem Likert) | Entero | Ordinal | 1–5 |
| `util_1`…`util_5` | Escala de utilidad percibida (5 ítems) | Entero | Ordinal | 1–5 |
| `aprobado` | ¿`desempeno_post` ≥ 70? | Texto | Nominal | Sí · No |

## Notas
- **Escala `util_1…util_5`:** 5 ítems de un mismo constructo (utilidad percibida); sirven para el **alfa de Cronbach** (Módulo 12). Consistencia interna: α ≈ 0.81.
- **Relación nula a propósito:** `sexo` (3 niveles: Hombre/Mujer/Otro) no se asocia con `aprobado` — χ²(2) = 1.37, p = .51 → enseña a **reportar un no-significativo** con honestidad.
- **Valores perdidos** (en `datos.csv`): 2 celdas vacías en cada una de `horas_practica`, `motivacion`, `satisfaccion`. En el crudo aparecen como 99 / NA.
- **`aprobado`** se deriva de `desempeno_post` ≥ 70.
- **Lectura para ingeniería:** `grupo` = método/proceso; `desempeno_post` = métrica de calidad; `aprobado` = cumple/no cumple especificación.

## Cómo se usa en el curso
| Técnica | Variables |
|---|---|
| Limpieza (Módulo 2) | `datos_crudos.csv` → `datos.csv` |
| Descriptiva | todas |
| t pareada | `desempeno_pre` vs `desempeno_post` |
| t independiente (+ Mann-Whitney) | `desempeno_post`: Método A vs Control |
| ANOVA 1 vía (+ post-hoc, Kruskal-Wallis) | `desempeno_post` ~ `grupo` |
| Correlación (Pearson/Spearman) | `horas_practica` & `desempeno_post`; `satisfaccion` & `desempeno_post` |
| Regresión simple / múltiple | `desempeno_post` ~ `horas_practica` (+ `edad`, `experiencia_previa`, `motivacion`) |
| Chi-cuadrado (+ V de Cramer) | `aprobado` × `grupo` (significativo) · `aprobado` × `sexo` (nulo) |
| Fiabilidad (alfa de Cronbach) | `util_1`…`util_5` |

## Propiedades verificadas
- Efecto entre grupos claro y monótono: medias 61.6 / 74.2 / 79.0.
- Correlación `horas_practica`–`desempeno_post`: r ≈ 0.51.
- Mejora pre→post ≈ 12.3 puntos.
- Control no normal (asimetría ≈ −0.65) y con mayor varianza → no paramétricas y homogeneidad.
- Asociación `aprobado` × `grupo`: 22 / 68 / 85 %. Asociación `aprobado` × `sexo`: nula.
- Alfa de Cronbach (`util_1…util_5`) ≈ 0.81.

## Reproducir
```sh
python3 generar_datos.py   # regenera datos.csv y datos_crudos.csv (idénticos)
```
Para `.omv` nativo de Jamovi: abrir el CSV en Jamovi y *Guardar como* → `.omv`.
