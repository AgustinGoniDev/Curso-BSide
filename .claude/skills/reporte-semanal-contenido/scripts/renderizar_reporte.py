#!/usr/bin/env python3
"""Renderiza el reporte semanal de contenido de Lumen Lab en HTML.

Uso: python renderizar_reporte.py datos.json salida.html

Requiere que datos.json ya tenga "metricas" (calcular_metricas.py) y "narrativa".
Formato: references/metricas.md
"""

import json
import os
import sys
from html import escape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from calcular_metricas import TIPOS, d, leads_por_post  # noqa: E402

PLANTILLA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "assets", "template-reporte.html")

MESES = ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"]
SEMAFOROS = {
    "atrae-icp": "● Atrae al cliente ideal",
    "mixto": "◐ Señal mixta",
    "audiencia-equivocada": "▲ Atrae audiencia equivocada",
    "sin-datos": "○ Sin datos suficientes",
}
TIPO_LABEL = {"dolor-icp": "Dolor del ICP", "educativo-generico": "Educativo genérico", "marca-personal": "Marca personal"}
FIT_LABEL = {"fuerte": "ICP fuerte", "parcial": "ICP parcial", "fuera": "Fuera de ICP"}
ORDEN_ESTADOS = ["Research", "Contactado", "Reunión agendada", "Propuesta enviada", "En evaluación", "Cliente activo", "Frío"]


def e(x):
    return escape(str(x), quote=True)


def n(x):
    return "—" if x is None else f"{round(x):,}".replace(",", ".")


def dec(x):
    if x is None:
        return "—"
    if abs(x) >= 100 or abs(x - round(x)) < 1e-9:
        return n(x)
    return f"{x:.1f}".replace(".", ",")


def dec2(x):
    return "—" if x is None else f"{x:.2f}".replace(".", ",")


def usd(x):
    return "—" if x is None else "$" + n(x)


def pct(x):
    return "—" if x is None else f"{x:.0f}%"


def dia(s):
    f = d(s)
    return f"{f.day} {MESES[f.month - 1]}"


def rango(ini, fin, con_anio=True):
    a, b = d(ini), d(fin)
    if a.month == b.month:
        txt = f"{a.day}–{b.day} {MESES[b.month - 1]}"
    else:
        txt = f"{a.day} {MESES[a.month - 1]} – {b.day} {MESES[b.month - 1]}"
    return f"{txt} {b.year}" if con_anio else txt


def delta(cur, prev, fmt=n, invertir=False):
    if cur is None or prev is None:
        return '<span class="delta-flat">—</span>'
    diff = cur - prev
    if abs(diff) < 1e-9:
        return '<span class="delta-flat">= igual</span>'
    sube = diff > 0
    bueno = sube != invertir
    signo = "+" if sube else "−"
    return f'<span class="{"delta-up" if bueno else "delta-down"}">{"▲" if sube else "▼"} {signo}{fmt(abs(diff))}</span>'


def truncar(s, k=90):
    return s if len(s) <= k else s[: k - 1].rstrip() + "…"


def validar_narrativa(nar):
    if not isinstance(nar, dict):
        sys.exit("Falta la clave 'narrativa' en datos.json (ver references/metricas.md).")
    v = nar.get("veredicto") or {}
    if v.get("semaforo") not in SEMAFOROS or not v.get("frase"):
        sys.exit("narrativa.veredicto necesita 'semaforo' válido y 'frase'.")
    if len(nar.get("evidencias") or []) != 3:
        sys.exit("narrativa.evidencias debe tener exactamente 3 elementos.")
    ac = nar.get("acciones") or {}
    for k in ("repetir", "dejar", "angulos"):
        if not ac.get(k):
            sys.exit(f"narrativa.acciones.{k} está vacío.")
    if not 2 <= len(ac["angulos"]) <= 3:
        sys.exit("narrativa.acciones.angulos debe tener 2 o 3 elementos.")


def lista(items, vacio="Sin observaciones."):
    if not items:
        return f'<p class="empty">{e(vacio)}</p>'
    return "<ul>" + "".join(f"<li>{e(i)}</li>" for i in items) + "</ul>"


def bloque_veredicto(datos):
    m, nar = datos["metricas"], datos["narrativa"]
    v = nar["veredicto"]
    s = v["semaforo"]
    html = [f'<section class="verdict v-{s}">',
            f'<span class="badge b-{s}">{e(SEMAFOROS[s])}</span>',
            f'<p class="frase">{e(v["frase"])}</p>',
            lista(nar["evidencias"])]
    if m["divergencia_alcance_leads"] and m["top_alcance"]:
        t = m["top_alcance"][0]
        html.append(
            f'<div class="diverge"><strong>El alcance y los leads no coinciden.</strong> '
            f'El post de más alcance de la ventana («{e(truncar(t["gancho"], 80))}», {n(t["impresiones"])} impresiones) '
            f'no trajo ningún lead, y otros posts con menos alcance sí.</div>')
    html.append("</section>")
    return "".join(html)


def bloque_kpis(m):
    a = m["periodos"]["actual"]
    p = m["periodos"]["previa"]
    v = m["periodos"]["ventana_5_semanas"]
    cards = [
        ("primary", "Leads atribuidos a contenido", n(a["leads"]),
         f'{delta(a["leads"], p["leads"])} vs semana anterior · ventana 5 sem.: {n(v["leads"])}'),
        ("", "Leads que son ICP fuerte", f'{a["leads_fuerte"]} de {a["leads"]}',
         f'ventana 5 sem.: {v["leads_fuerte"]} de {v["leads"]} ({pct(v["pct_icp"])})'),
        ("", "Pipeline atribuido (USD/mes)", usd(a["pipeline_usd"]),
         f'ponderado {usd(a["pipeline_ponderado_usd"])} · ventana {usd(v["pipeline_usd"])}'
         + (f' · {a["leads_sin_valor"]} lead sin valor cargado' if a["leads_sin_valor"] == 1 else f' · {a["leads_sin_valor"]} leads sin valor cargado' if a["leads_sin_valor"] else "")),
        ("", "Leads ICP por 1.000 impresiones", dec2(a["leads_icp_por_1000_imp"]),
         f'ventana 5 sem.: {dec2(v["leads_icp_por_1000_imp"])}'),
    ]
    out = ['<section class="kpis">']
    for cls, lbl, val, sub in cards:
        out.append(f'<div class="kpi {cls}"><div class="lbl">{e(lbl)}</div><div class="val">{e(val)}</div><div class="sub">{sub}</div></div>')
    out.append("</section>")
    return "".join(out)


def bloque_grafico(m):
    out = ['<div class="bars">']
    for t in TIPOS:
        x = m["por_tipo"][t]
        out.append('<div class="bar-group">')
        out.append(f'<h3>{e(TIPO_LABEL[t])}<span>{x["posts"]} {"post" if x["posts"] == 1 else "posts"} · {x["leads"]} {"lead" if x["leads"] == 1 else "leads"} ({x["leads_fuerte"]} ICP fuerte) · '
                   f'{dec2(x["leads_icp_por_1000_imp"])} leads ICP por 1.000 imp.</span></h3>')
        ip = x["pct_impresiones"] or 0
        lp = x["pct_leads"] or 0
        out.append(f'<div class="bar-row"><span>Impresiones</span><div class="track"><div class="fill imp" style="width:{ip}%"></div></div>'
                   f'<span class="v">{pct(x["pct_impresiones"])} · {n(x["impresiones"])}</span></div>')
        out.append(f'<div class="bar-row"><span>Leads</span><div class="track"><div class="fill lead" style="width:{lp}%"></div></div>'
                   f'<span class="v">{pct(x["pct_leads"])} · {x["leads"]}</span></div>')
        out.append("</div>")
    out.append("</div>")
    out.append('<p class="legend"><i style="background:#9a9ab0"></i>% de las impresiones de la ventana'
               '<i style="background:#e94560"></i>% de los leads de la ventana</p>')
    return "".join(out)


def bloque_comparacion(m):
    a, p, b = (m["periodos"][k] for k in ("actual", "previa", "prom_4_semanas"))
    filas = [
        ("Posts publicados", "posts", n, False),
        ("Impresiones", "impresiones", n, False),
        ("Mensajes recibidos", "mensajes", n, False),
        ("Leads atribuidos", "leads", n, False),
        ("Leads ICP fuerte", "leads_fuerte", n, False),
        ("Pipeline atribuido (USD/mes)", "pipeline_usd", usd, False),
        ("Leads ICP por 1.000 impresiones", "leads_icp_por_1000_imp", dec2, False),
    ]
    out = ['<div class="table-wrap"><table><thead><tr><th>Métrica</th><th class="num">Esta semana</th>'
           '<th class="num">Anterior</th><th class="num">Cambio</th><th class="num">Prom. 4 sem.</th></tr></thead><tbody>']
    for lbl, k, fmt, inv in filas:
        bval = b[k]
        out.append(f'<tr><td>{e(lbl)}</td><td class="num"><strong>{fmt(a[k])}</strong></td><td class="num">{fmt(p[k])}</td>'
                   f'<td class="num">{delta(a[k], p[k], fmt, inv)}</td><td class="num">{(usd if fmt is usd else dec2 if fmt is dec2 else dec)(bval)}</td></tr>')
    out.append("</tbody></table></div>")
    return "".join(out)


def bloque_posts(datos):
    ini, fin = d(datos["semana"]["inicio"]), d(datos["semana"]["fin"])
    mapa = leads_por_post(datos)
    posts = sorted((p for p in datos["posts"] if ini <= d(p["fecha"]) <= fin), key=lambda p: p["fecha"])
    if not posts:
        return '<p class="empty">Esta semana no se publicó ningún post.</p>'
    out = ['<div class="table-wrap"><table><thead><tr><th>Fecha</th><th>Post</th><th>Formato</th>'
           '<th class="num">Imp.</th><th class="num">Reacc.</th><th class="num">Coment.</th><th class="num">Msj.</th><th class="num">Leads</th></tr></thead><tbody>']
    for p in posts:
        cls = "b-fuerte" if p["tipo"] == "dolor-icp" else "b-neutral"
        fund = f'<span class="small">{e(p.get("fundamento_tipo", ""))}</span>' if p.get("fundamento_tipo") else ""
        out.append(f'<tr><td>{dia(p["fecha"])}</td><td>{e(p["gancho"])}<br><span class="badge {cls}">{e(TIPO_LABEL[p["tipo"]])}</span>{fund}</td>'
                   f'<td>{e(p["formato"])}</td><td class="num">{n(p["impresiones"])}</td><td class="num">{n(p["reacciones"])}</td>'
                   f'<td class="num">{n(p["comentarios"])}</td><td class="num">{n(p["mensajes"])}</td><td class="num"><strong>{len(mapa[p["id"]])}</strong></td></tr>')
    out.append("</tbody></table></div>")
    return "".join(out)


def bloque_leads(datos):
    m = datos["metricas"]
    ini5 = d(m["periodos"]["ventana_5_semanas"]["inicio"])
    fin5 = d(m["periodos"]["ventana_5_semanas"]["fin"])
    mapa = leads_por_post(datos)
    pipeline = {f["id"]: f for f in datos["pipeline"]}
    posts_v = [p for p in datos["posts"] if ini5 <= d(p["fecha"]) <= fin5]
    por_lead = {}
    for p in posts_v:
        for lid in mapa[p["id"]]:
            if lid in pipeline:
                por_lead.setdefault(lid, []).append(p)
    if not por_lead:
        return '<p class="empty">Ningún post de la ventana tiene leads atribuidos.</p>'
    orden = sorted(por_lead, key=lambda i: max(p["fecha"] for p in por_lead[i]), reverse=True)
    out = ['<div class="table-wrap"><table><thead><tr><th>Lead</th><th>Rubro y cargo</th><th class="num">Valor</th>'
           '<th>Ajuste al ICP</th><th>Trajo el post</th></tr></thead><tbody>']
    for lid in orden:
        f = pipeline[lid]
        val = usd(f["valor"]) + (f'<span class="small">prob. {f["prob"]}%</span>' if f.get("prob") is not None else "") if f.get("valor") is not None else "—"
        post = "<br>".join(f'{dia(p["fecha"])} · {e(truncar(p["gancho"], 70))}' for p in por_lead[lid])
        out.append(f'<tr><td><strong>{e(f["empresa"])}</strong><span class="small">{e(f["estado"])} · {e(f.get("origen") or "—")}</span></td>'
                   f'<td>{e(f.get("rubro") or "—")}<span class="small">{e(f.get("cargo") or "—")}</span></td>'
                   f'<td class="num">{val}</td>'
                   f'<td><span class="badge b-{f["fit"]}">{e(FIT_LABEL[f["fit"]])}</span><span class="small">{e(f.get("fundamento_fit", ""))}</span></td>'
                   f'<td>{post}</td></tr>')
    out.append("</tbody></table></div>")
    return "".join(out)


def bloque_pipeline(m):
    emb = m["embudo_ventana"]
    chips = " · ".join(f'{e(est)}: <strong>{emb[est]}</strong>' for est in ORDEN_ESTADOS if est in emb)
    mez = m["mezcla_pipeline"]
    out = [f'<p><strong>Leads de contenido por etapa</strong> (ventana 5 semanas): {chips or "sin leads"}.</p>']
    if mez["abierto_usd"]:
        out.append(f'<p>Del pipeline abierto ({mez["abierto_filas"]} oportunidades, {usd(mez["abierto_usd"])}/mes), '
                   f'<strong>{mez["abierto_atribuido_contenido_filas"]} tienen origen en contenido</strong> (de cualquier fecha) '
                   f'({usd(mez["abierto_atribuido_contenido_usd"])}/mes, {pct(mez["pct_abierto_atribuido_contenido"])}). '
                   f'El resto entra por outbound, referidos o eventos.</p>')
    out.append('<div class="table-wrap"><table><thead><tr><th>Origen</th><th class="num">Filas</th><th class="num">Abiertas</th>'
               '<th class="num">Abierto USD/mes</th><th class="num">Ponderado</th></tr></thead><tbody>')
    for o, x in sorted(mez["por_origen"].items(), key=lambda kv: -kv[1]["abierto_usd"]):
        out.append(f'<tr><td>{e(o)}</td><td class="num">{x["filas"]}</td><td class="num">{x["filas_abiertas"]}</td>'
                   f'<td class="num">{usd(x["abierto_usd"])}</td><td class="num">{usd(x["abierto_ponderado_usd"])}</td></tr>')
    out.append(f'<tr class="total"><td>Total abierto</td><td class="num"></td><td class="num">{mez["abierto_filas"]}</td>'
               f'<td class="num">{usd(mez["abierto_usd"])}</td><td class="num"></td></tr></tbody></table></div>')
    out.append('<p class="lede">Abierto = Contactado, Reunión agendada, Propuesta enviada o En evaluación. Las oportunidades sin valor cargado no suman.</p>')
    return "".join(out)


def bloque_acciones(ac):
    def col(cls, titulo, items):
        return f'<div class="col {cls}"><h3>{titulo}</h3>{lista(items)}</div>'
    return ('<div class="cols">' + col("repetir", "Repetir", ac["repetir"]) + col("dejar", "Dejar de hacer", ac["dejar"])
            + col("angulos", "Ángulos para la semana que viene", ac["angulos"]) + "</div>")


def bloque_calidad(m, nar):
    avisos = list(m["consistencia"]) + list(nar.get("calidad_datos") or [])
    out = ['<div class="notes"><h3>Datos a corregir en Notion</h3>', lista(avisos, "No se detectaron inconsistencias.")]
    out.append("<h3>Supuestos de este reporte</h3>")
    out.append(lista(nar.get("supuestos") or [], "Sin supuestos adicionales."))
    out.append("</div>")
    return "".join(out)


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) != 3:
        sys.exit("Uso: python renderizar_reporte.py datos.json salida.html")
    with open(sys.argv[1], encoding="utf-8") as f:
        datos = json.load(f)
    if "metricas" not in datos:
        sys.exit("Falta 'metricas': corré primero calcular_metricas.py.")
    validar_narrativa(datos.get("narrativa"))

    m, nar, sem = datos["metricas"], datos["narrativa"], datos["semana"]
    v5 = m["periodos"]["ventana_5_semanas"]
    gen = d(datos.get("generado") or sem["fin"])

    slots = {
        "TITULO": f'Reporte semanal de contenido — Lumen Lab — {rango(sem["inicio"], sem["fin"])}',
        "RANGO": f'Semana del {rango(sem["inicio"], sem["fin"])}',
        "RANGO_VENTANA": rango(v5["inicio"], v5["fin"]),
        "GENERADO": f"{gen.day} {MESES[gen.month - 1]} {gen.year}",
        "PARCIAL": '<div class="partial">Semana en curso: los datos son parciales.</div>' if sem.get("parcial") else "",
        "VEREDICTO": bloque_veredicto(datos),
        "KPIS": bloque_kpis(m),
        "GRAFICO": bloque_grafico(m),
        "COMPARACION": bloque_comparacion(m),
        "POSTS": bloque_posts(datos),
        "LEADS": bloque_leads(datos),
        "PIPELINE": bloque_pipeline(m),
        "ACCIONES": bloque_acciones(nar["acciones"]),
        "CALIDAD": bloque_calidad(m, nar),
    }
    with open(PLANTILLA, encoding="utf-8") as f:
        html = f.read()
    for k, val in slots.items():
        html = html.replace("{{" + k + "}}", e(val) if k == "TITULO" else val)
    if "{{" in html:
        sys.exit("La plantilla tiene marcadores sin reemplazar.")

    salida = sys.argv[2]
    os.makedirs(os.path.dirname(os.path.abspath(salida)), exist_ok=True)
    with open(salida, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Reporte generado: {salida}")


if __name__ == "__main__":
    main()
