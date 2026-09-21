#!/usr/bin/env python3
"""Calcula las métricas del reporte semanal de contenido de Lumen Lab.

Uso: python calcular_metricas.py datos.json

Lee posts + pipeline (ya clasificados) y agrega la clave "metricas" al mismo archivo.
Formato de entrada y definiciones: references/metricas.md
"""

import json
import sys
from datetime import date, timedelta

TIPOS = ("dolor-icp", "educativo-generico", "marca-personal")
FITS = ("fuerte", "parcial", "fuera")
ESTADOS_ABIERTOS = ("Contactado", "Reunión agendada", "Propuesta enviada", "En evaluación")


def d(s):
    return date.fromisoformat(s[:10])


def por_mil(leads, imp):
    return round(leads / imp * 1000, 2) if imp else None


def pct(a, b):
    return round(a / b * 100, 1) if b else None


def cargar(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def validar(datos):
    errores = []
    for p in datos["posts"]:
        if p.get("tipo") not in TIPOS:
            errores.append(f"Post sin tipo válido ({p.get('tipo')!r}): {p.get('gancho', p.get('id'))}")
    return errores


def leads_por_post(datos):
    """post_id -> set de ids de pipeline, uniendo ambos lados de la relación."""
    mapa = {p["id"]: set(p.get("lead_ids") or []) for p in datos["posts"]}
    for fila in datos["pipeline"]:
        for pid in fila.get("post_ids") or []:
            if pid in mapa:
                mapa[pid].add(fila["id"])
    return mapa


def agregar_periodo(posts, pipeline_por_id, mapa, ini, fin):
    en = [p for p in posts if ini <= d(p["fecha"]) <= fin]
    lead_ids = set()
    for p in en:
        lead_ids |= mapa[p["id"]]
    leads = [pipeline_por_id[i] for i in lead_ids if i in pipeline_por_id]
    imp = sum(p["impresiones"] or 0 for p in en)
    fuerte = sum(1 for l in leads if l.get("fit") == "fuerte")
    con_valor = [l for l in leads if l.get("valor") is not None]
    return {
        "posts": len(en),
        "impresiones": imp,
        "reacciones": sum(p["reacciones"] or 0 for p in en),
        "comentarios": sum(p["comentarios"] or 0 for p in en),
        "mensajes": sum(p["mensajes"] or 0 for p in en),
        "leads": len(leads),
        "leads_fuerte": fuerte,
        "leads_parcial": sum(1 for l in leads if l.get("fit") == "parcial"),
        "leads_fuera": sum(1 for l in leads if l.get("fit") == "fuera"),
        "pct_icp": pct(fuerte, len(leads)),
        "leads_icp_por_1000_imp": por_mil(fuerte, imp),
        "pipeline_usd": sum(l["valor"] for l in con_valor),
        "pipeline_ponderado_usd": round(sum(l["valor"] * (l.get("prob") or 0) / 100 for l in con_valor)),
        "leads_sin_valor": len(leads) - len(con_valor),
        "mensajes_por_post": round(sum(p["mensajes"] or 0 for p in en) / len(en), 1) if en else None,
    }


def promedio_4(base):
    """base: agregado de las 4 semanas previas sumadas. Devuelve promedio semanal."""
    prom = {}
    for k, v in base.items():
        if k in ("pct_icp", "leads_icp_por_1000_imp", "mensajes_por_post"):
            prom[k] = v  # ratios: se calculan sobre la suma, no se promedian
        else:
            prom[k] = round(v / 4, 1)
    return prom


def desglose(posts, pipeline_por_id, mapa, clave, valores):
    """Desglose por tipo o formato sobre la ventana completa."""
    total_imp = sum(p["impresiones"] or 0 for p in posts)
    total_leads = set()
    for p in posts:
        total_leads |= mapa[p["id"]]
    out = {}
    for val in valores:
        ps = [p for p in posts if p.get(clave) == val]
        ids = set()
        for p in ps:
            ids |= mapa[p["id"]]
        leads = [pipeline_por_id[i] for i in ids if i in pipeline_por_id]
        imp = sum(p["impresiones"] or 0 for p in ps)
        fuerte = sum(1 for l in leads if l.get("fit") == "fuerte")
        out[val] = {
            "posts": len(ps),
            "impresiones": imp,
            "pct_impresiones": pct(imp, total_imp),
            "impresiones_por_post": round(imp / len(ps)) if ps else None,
            "mensajes": sum(p["mensajes"] or 0 for p in ps),
            "comentarios": sum(p["comentarios"] or 0 for p in ps),
            "leads": len(leads),
            "pct_leads": pct(len(leads), len(total_leads)),
            "leads_fuerte": fuerte,
            "leads_icp_por_1000_imp": por_mil(fuerte, imp),
        }
    return out


def consistencia(datos, mapa):
    avisos = []
    posts = {p["id"]: p for p in datos["posts"]}
    pipeline = {f["id"]: f for f in datos["pipeline"]}
    for f in datos["pipeline"]:
        for pid in f.get("post_ids") or []:
            p = posts.get(pid)
            if p is not None and f["id"] not in (p.get("lead_ids") or []):
                avisos.append(f"{f['empresa']} dice que lo trajo «{p['gancho'][:50]}…», pero ese post no lo lista en Leads.")
    for p in datos["posts"]:
        for lid in p.get("lead_ids") or []:
            f = pipeline.get(lid)
            if f is not None and p["id"] not in (f.get("post_ids") or []):
                avisos.append(f"El post «{p['gancho'][:50]}…» lista a {f['empresa']} como lead, pero esa fila no tiene el post en «Post que lo trajo».")
        if (p["mensajes"] or 0) > 0 and not mapa[p["id"]]:
            avisos.append(f"El post «{p['gancho'][:50]}…» ({p['fecha']}) recibió {p['mensajes']} mensajes y no tiene ningún lead cargado: puede haber un lead sin registrar.")
    for f in datos["pipeline"]:
        if f.get("origen") == "LinkedIn" and not f.get("post_ids"):
            avisos.append(f"{f['empresa']} es de origen LinkedIn y no tiene «Post que lo trajo».")
        if f.get("post_ids") and f.get("origen") != "LinkedIn":
            avisos.append(f"{f['empresa']} tiene post atribuido pero su origen es {f.get('origen')}, no LinkedIn.")
        if not (f.get("rubro") or "").strip():
            avisos.append(f"{f['empresa']} no tiene Rubro cargado.")
        if f.get("estado") in ("Propuesta enviada", "En evaluación") and f.get("valor") is None:
            avisos.append(f"{f['empresa']} está en «{f['estado']}» sin Valor USD/mes.")
    return avisos


def mezcla_pipeline(pipeline):
    origenes = {}
    for f in pipeline:
        o = f.get("origen") or "Sin origen"
        m = origenes.setdefault(o, {"filas": 0, "abierto_usd": 0, "abierto_ponderado_usd": 0, "filas_abiertas": 0})
        m["filas"] += 1
        if f.get("estado") in ESTADOS_ABIERTOS:
            m["filas_abiertas"] += 1
            v = f.get("valor")
            if v is not None:
                m["abierto_usd"] += v
                m["abierto_ponderado_usd"] += round(v * (f.get("prob") or 0) / 100)
    abiertos = [f for f in pipeline if f.get("estado") in ESTADOS_ABIERTOS]
    atrib = [f for f in abiertos if f.get("post_ids")]
    abierto_usd = sum(f["valor"] for f in abiertos if f.get("valor") is not None)
    atrib_usd = sum(f["valor"] for f in atrib if f.get("valor") is not None)
    return {
        "por_origen": origenes,
        "abierto_filas": len(abiertos),
        "abierto_usd": abierto_usd,
        "abierto_atribuido_contenido_filas": len(atrib),
        "abierto_atribuido_contenido_usd": atrib_usd,
        "pct_abierto_atribuido_contenido": pct(atrib_usd, abierto_usd),
    }


def semaforo(leads, fuerte):
    if leads < 3:
        return "sin-datos"
    p = fuerte / leads * 100
    if p >= 70:
        return "atrae-icp"
    if p >= 40:
        return "mixto"
    return "audiencia-equivocada"


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 2:
        sys.exit("Uso: python calcular_metricas.py datos.json")
    path = sys.argv[1]
    datos = cargar(path)

    errores = validar(datos)
    if errores:
        sys.exit("Faltan clasificaciones:\n- " + "\n- ".join(errores))

    ini = d(datos["semana"]["inicio"])
    fin = d(datos["semana"]["fin"])
    ini_prev, fin_prev = ini - timedelta(days=7), fin - timedelta(days=7)
    ini_4, fin_4 = ini - timedelta(days=28), ini - timedelta(days=1)

    posts = datos["posts"]
    pipeline = datos["pipeline"]
    pipeline_por_id = {f["id"]: f for f in pipeline}
    mapa = leads_por_post(datos)

    ventana = [p for p in posts if ini_4 <= d(p["fecha"]) <= fin]
    fuera_ventana = len(posts) - len(ventana)

    actual = agregar_periodo(posts, pipeline_por_id, mapa, ini, fin)
    previa = agregar_periodo(posts, pipeline_por_id, mapa, ini_prev, fin_prev)
    base4 = agregar_periodo(posts, pipeline_por_id, mapa, ini_4, fin_4)
    vent = agregar_periodo(posts, pipeline_por_id, mapa, ini_4, fin)

    faltan_fit = [
        pipeline_por_id[i]["empresa"]
        for i in {i for p in ventana for i in mapa[p["id"]]}
        if i in pipeline_por_id and pipeline_por_id[i].get("fit") not in FITS
    ]
    if faltan_fit:
        sys.exit("Faltan fit en leads atribuidos: " + ", ".join(sorted(faltan_fit)))

    top = sorted(ventana, key=lambda p: p["impresiones"] or 0, reverse=True)[:3]
    top_alcance = [
        {"gancho": p["gancho"], "fecha": p["fecha"], "impresiones": p["impresiones"], "tipo": p["tipo"], "leads": len(mapa[p["id"]])}
        for p in top
    ]
    hay_leads_en_otros = any(len(mapa[p["id"]]) > 0 for p in ventana)
    divergencia = bool(top and len(mapa[top[0]["id"]]) == 0 and hay_leads_en_otros)

    datos["metricas"] = {
        "periodos": {
            "actual": {"inicio": str(ini), "fin": str(fin), **actual},
            "previa": {"inicio": str(ini_prev), "fin": str(fin_prev), **previa},
            "prom_4_semanas": {"inicio": str(ini_4), "fin": str(fin_4), **promedio_4(base4)},
            "ventana_5_semanas": {"inicio": str(ini_4), "fin": str(fin), **vent},
        },
        "por_tipo": desglose(ventana, pipeline_por_id, mapa, "tipo", TIPOS),
        "por_formato": desglose(ventana, pipeline_por_id, mapa, "formato", ("Texto", "Carrusel", "Video")),
        "embudo_ventana": _embudo(ventana, pipeline_por_id, mapa),
        "mezcla_pipeline": mezcla_pipeline(pipeline),
        "top_alcance": top_alcance,
        "divergencia_alcance_leads": divergencia,
        "semaforo_sugerido": semaforo(vent["leads"], vent["leads_fuerte"]),
        "consistencia": consistencia(datos, mapa),
        "posts_fuera_de_ventana_ignorados": fuera_ventana,
    }

    with open(path, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)

    m = datos["metricas"]
    print(f"OK. Semana {ini}..{fin} | posts {actual['posts']} | leads semana {actual['leads']} | "
          f"leads ventana {vent['leads']} ({vent['leads_fuerte']} ICP fuerte) | semáforo sugerido: {m['semaforo_sugerido']}")
    if divergencia:
        print("Divergencia: el post de más alcance de la ventana no trajo leads y otros sí.")
    for a in m["consistencia"]:
        print("  ! " + a)


def _embudo(ventana, pipeline_por_id, mapa):
    ids = set()
    for p in ventana:
        ids |= mapa[p["id"]]
    cuentas = {}
    for i in ids:
        f = pipeline_por_id.get(i)
        if f:
            cuentas[f["estado"]] = cuentas.get(f["estado"], 0) + 1
    return cuentas


if __name__ == "__main__":
    main()
