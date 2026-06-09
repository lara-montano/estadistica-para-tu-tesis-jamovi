#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dataset del PROYECTO FINAL (Módulo 15): escenario distinto al hilo conductor,
para que el alumno aplique todo de cero.

Escenario: efecto de un programa de ejercicio sobre el bienestar.
Grupos: Control / Programa A / Programa B. n = 90 (30 por grupo).
Estructura analoga al dataset del curso -> cubre t, ANOVA, correlacion,
regresion y chi-cuadrado. Reproducible (semilla fija), sin dependencias.
"""
import csv
import os
import random
import statistics

GROUPS = ["Control", "Programa A", "Programa B"]
EFF = {"Control": 0.0, "Programa A": 6.0, "Programa B": 12.0}
COLS = ["id", "programa", "sexo", "edad", "bienestar_pre", "bienestar_post",
        "horas_ejercicio", "adherencia", "recomienda"]


def generar(seed=11):
    random.seed(seed)
    rows = []
    i = 0
    for g in GROUPS:
        for _ in range(30):
            i += 1
            sexo = random.choices(["Hombre", "Mujer"], weights=[50, 50])[0]
            edad = round(min(60, max(18, random.gauss(35, 8))))
            pre = round(min(100, max(0, random.gauss(55, 10))))
            horas = round(max(0, random.gauss(4, 1.5)), 1)
            adher = round(min(5, max(1, random.gauss(3.5, 1.0))))
            noise = random.gauss(0, 6)
            post = 20 + 0.5 * pre + EFF[g] + 1.8 * horas + 1.0 * adher + noise
            post = round(min(100, max(0, post)))
            rows.append({
                "id": i, "programa": g, "sexo": sexo, "edad": edad,
                "bienestar_pre": pre, "bienestar_post": post,
                "horas_ejercicio": horas, "adherencia": adher,
                "recomienda": "Sí" if post >= 65 else "No",
            })
    return rows


def corr(rows, a, b):
    xs = [r[a] for r in rows]
    ys = [r[b] for r in rows]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / len(xs)
    return cov / (statistics.pstdev(xs) * statistics.pstdev(ys))


if __name__ == "__main__":
    rows = generar()
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos_proyecto.csv")
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    print(f"n = {len(rows)}   {out}")
    for g in GROUPS:
        v = [r["bienestar_post"] for r in rows if r["programa"] == g]
        print(f"  {g:11s}: bienestar_post {statistics.mean(v):5.1f}")
    print(f"  r(horas_ejercicio, bienestar_post) = {corr(rows, 'horas_ejercicio', 'bienestar_post'):.2f}")
    print(f"  % recomienda = {100*sum(1 for r in rows if r['recomienda']=='Sí')/len(rows):.0f}%")
