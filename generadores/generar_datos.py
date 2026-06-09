#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genera el dataset hilo conductor del Curso 01 (Escenario A) en DOS capas:

  - datos.csv         -> versión LIMPIA, lista para analizar (la de las demos).
  - datos_crudos.csv  -> versión SUCIA y realista (materia prima del Módulo 2
                         de limpieza): categorías inconsistentes, valores
                         imposibles, Likert fuera de rango, id duplicado,
                         faltantes codificados (99 / NA) y filas basura.

Limpiar datos_crudos.csv (normalizar etiquetas, recodificar 99/NA a perdido,
quitar fila duplicada y fila vacía/ inválida) reproduce datos.csv.

Incluye una escala de 5 ítems (util_1..util_5) para el alfa de Cronbach (Módulo 12)
y conserva una relación NULA (sexo vs resultado) para enseñar a reportar un
no-significativo. Reproducible (semillas fijas), sin dependencias externas.
"""
import csv
import os
import random
import statistics

N_PER = 40
GROUPS = ["Control", "Método A", "Método B"]
GROUP_EFFECT = {"Control": 0.0, "Método A": 7.0, "Método B": 14.0}

COLS = ["id", "grupo", "sexo", "edad", "experiencia_previa", "desempeno_pre",
        "desempeno_post", "horas_practica", "motivacion", "satisfaccion",
        "util_1", "util_2", "util_3", "util_4", "util_5", "aprobado"]
SAT_ITEMS = ["util_1", "util_2", "util_3", "util_4", "util_5"]
HERE = os.path.dirname(os.path.abspath(__file__))


def likert_sesgado():
    # satisfaccion global: sesgada al techo (sesgo de respuesta)
    return random.choices([1, 2, 3, 4, 5], weights=[2, 5, 13, 35, 45])[0]


def generar_limpio(seed=35):
    # --- Núcleo (misma secuencia que la versión verificada -> mismas propiedades) ---
    random.seed(seed)
    rows = []
    i = 0
    for g in GROUPS:
        for _ in range(N_PER):
            i += 1
            sexo = random.choices(["Hombre", "Mujer", "Otro"], weights=[48, 48, 4])[0]
            edad = round(min(45, max(18, random.gauss(24, 4))))
            experiencia = max(0, round(random.gauss(3, 2)))
            pre = round(min(100, max(0, random.gauss(60, 10))))
            horas = round(max(0, random.gauss(10, 4)), 1)
            motivacion = round(min(5, max(1, random.gauss(3.4, 1.0))))
            satisfaccion = likert_sesgado()
            noise = random.gauss(0, 5)
            post = (18 + 0.5 * pre + GROUP_EFFECT[g] + 1.3 * horas
                    + 0.5 * experiencia + 1.0 * motivacion + noise)
            if g == "Control" and random.random() < 0.12:
                post -= random.uniform(10, 25)
            post = round(min(100, max(0, post)))
            rows.append({
                "id": i, "grupo": g, "sexo": sexo, "edad": edad,
                "experiencia_previa": experiencia, "desempeno_pre": pre,
                "desempeno_post": post, "horas_practica": horas,
                "motivacion": motivacion, "satisfaccion": satisfaccion,
                "aprobado": "Sí" if post >= 70 else "No",
            })

    # --- Escala de utilidad percibida (5 ítems, 1 factor) para Cronbach ---
    random.seed(202)
    for r in rows:
        latent = random.gauss(0, 1)
        for it in SAT_ITEMS:
            val = 3.2 + 1.0 * latent + random.gauss(0, 0.9)
            r[it] = int(round(min(5, max(1, val))))

    # --- Valores perdidos a propósito (limpieza en el Módulo 2) ---
    random.seed(7)
    for col in ["motivacion", "satisfaccion", "horas_practica"]:
        for idx in random.sample(range(len(rows)), 2):
            rows[idx][col] = ""
    return rows


def ensuciar(clean):
    """Deriva la versión cruda inyectando suciedad realista (reversible)."""
    raw = [dict(r) for r in clean]
    random.seed(123)

    # 1) Faltantes codificados: las celdas perdidas pasan a 99 / NA
    for r in raw:
        if r["horas_practica"] == "":
            r["horas_practica"] = "99"
        if r["motivacion"] == "":
            r["motivacion"] = "NA"
        if r["satisfaccion"] == "":
            r["satisfaccion"] = "NA"

    # 2) Etiquetas inconsistentes en 'grupo'
    gvar = {
        "Control": ["control", "CONTROL", "Control "],
        "Método A": ["Metodo A", "método a", "Método A "],
        "Método B": ["metodo b", "Método B ", "MÉTODO B"],
    }
    for idx in random.sample(range(len(raw)), 12):
        raw[idx]["grupo"] = random.choice(gvar[raw[idx]["grupo"]])

    # 3) Etiquetas inconsistentes en 'sexo'
    svar = {"Hombre": ["H", "hombre", "HOMBRE"], "Mujer": ["M", "mujer", "Mujer "], "Otro": ["O", "otro"]}
    for idx in random.sample(range(len(raw)), 10):
        raw[idx]["sexo"] = random.choice(svar.get(raw[idx]["sexo"], [raw[idx]["sexo"]]))

    # 4) Filas basura: una duplicada (mismo id) y una vacía/ inválida
    raw.append(dict(raw[49]))                      # duplicado del id 50
    basura = {c: "" for c in COLS}
    basura.update({"id": "999", "grupo": "", "edad": "200", "motivacion": "7"})  # edad imposible, Likert fuera de rango
    raw.append(basura)
    return raw


def guardar(rows, nombre):
    out = os.path.join(HERE, nombre)
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(rows)
    return out


def cronbach(rows, items):
    data = [[float(r[it]) for it in items] for r in rows
            if all(r[it] not in ("", "NA") for it in items)]
    k = len(items)
    item_vars = [statistics.pvariance([row[j] for row in data]) for j in range(k)]
    var_total = statistics.pvariance([sum(row) for row in data])
    return (k / (k - 1)) * (1 - sum(item_vars) / var_total)


def corr(rows, a, b):
    pr = [(float(r[a]), float(r[b])) for r in rows if r[a] != "" and r[b] != ""]
    xs = [p[0] for p in pr]
    ys = [p[1] for p in pr]
    mx, my = statistics.mean(xs), statistics.mean(ys)
    cov = sum((x - mx) * (y - my) for x, y in pr) / len(pr)
    return cov / (statistics.pstdev(xs) * statistics.pstdev(ys))


def verificar(clean, raw):
    print("=== LIMPIO (datos.csv) ===")
    print(f"n = {len(clean)}")
    for g in GROUPS:
        v = [r["desempeno_post"] for r in clean if r["grupo"] == g]
        print(f"  {g:9s}: post {statistics.mean(v):5.1f} ± {statistics.pstdev(v):4.1f}")
    print(f"  r(horas, post) = {corr(clean, 'horas_practica', 'desempeno_post'):.2f}")
    print(f"  alfa de Cronbach (util_1..util_5) = {cronbach(clean, SAT_ITEMS):.2f}")
    # relacion nula sexo vs aprobado (Hombre/Mujer): % aprobado por sexo
    for s in ["Hombre", "Mujer"]:
        v = [r for r in clean if r["sexo"] == s]
        ap = 100 * sum(1 for r in v if r["aprobado"] == "Sí") / len(v)
        print(f"  aprobado entre {s}: {ap:.0f}%   (n={len(v)})  <- debe ser parecido (relación nula)")
    falt = {c: sum(1 for r in clean if r[c] == "") for c in COLS}
    print("  perdidos:", {c: n for c, n in falt.items() if n})

    print("\n=== CRUDO (datos_crudos.csv) ===")
    print(f"n filas = {len(raw)}  (incluye 1 duplicada + 1 basura)")
    print("  etiquetas de 'grupo':", sorted(set(r["grupo"] for r in raw)))
    print("  etiquetas de 'sexo' :", sorted(set(r["sexo"] for r in raw)))
    cod = sum(1 for r in raw for c in ["horas_practica", "motivacion", "satisfaccion"] if r[c] in ("99", "NA"))
    print(f"  faltantes codificados (99/NA): {cod}")
    print("  edades imposibles:", [r["edad"] for r in raw if r["edad"] not in ("",) and float(r["edad"]) > 100])


if __name__ == "__main__":
    clean = generar_limpio()
    raw = ensuciar(clean)
    p1 = guardar(clean, "datos.csv")
    p2 = guardar(raw, "datos_crudos.csv")
    verificar(clean, raw)
    print(f"\nGuardados:\n  {p1}\n  {p2}")
