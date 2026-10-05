---
type: session
area: general
date: 2026-09-23
slug: 2026-09-23-skill-reporte-semanal-contenido
title: "Skill de reporte semanal de contenido y subida a GitHub"
tags: [reporte-semanal, contenido, icp, pipeline, notion, github, skill]
status: active
related:
  - cliente
  - que-hacemos
  - voz
  - procesos
  - 2026-09-10-instalacion-wiki-cerebro
sources:
  - repo:.claude/skills/reporte-semanal-contenido
  - repo:reportes/reporte-semanal-2026-09-20.html
  - url:https://www.notion.so/35b8e29552c38082a59dfba5586c8cd4
  - url:https://github.com/AgustinGoniDev/Curso-BSide
superseded_by: null
---

# Skill de reporte semanal de contenido y subida a GitHub

## Contexto

El usuario confirmó que Notion está conectado (conector MCP) y pasó la carpeta raíz "Lumen Lab", que tiene tres bases: Pipeline, Contenido y Reportes semanales. Pidió, usando el `skill-creator`, una skill que cruce el Pipeline con la tabla de Contenido y use la capa de contexto (ICP y oferta de `cerebro/contexto/`) para detectar si el contenido atrae al cliente ideal, con métricas referidas a eso, en HTML con el branding de la agencia. Después, con `/setup-git-equipo`, pidió subir la carpeta al repo `AgustinGoniDev/Curso-BSide`, y por último guardar las decisiones en el cerebro. Antes de todo esto había pedido instalar `claude-brain-skill` desde GitHub; esa instalación quedó interrumpida y sin hacer.

## Decisiones

- **"Atrae al ICP" se mide por los leads que entran, no por la audiencia.** Notion no trae quién ve cada post en LinkedIn. El reporte lo dice explícito.
- **El reporte abre con pipeline, no con impresiones.** Leads ICP, pipeline USD y avance del embudo van primero; impresiones y reacciones quedan como contexto. Coincide con [[voz]]: alcance y engagement no son un fin.
- **Ventana de 5 semanas** (la reportada + 4 previas), con comparación contra la semana anterior y el promedio de 4 semanas. Rationale: con ~2 posts por semana una sola semana casi nunca alcanza para concluir.
- **Semáforo del veredicto:** menos de 3 leads en la ventana = sin datos; 70 % o más de leads ICP fuerte = atrae al ICP; 40–69 % = mixto; menos de 40 % = audiencia equivocada. Son umbrales propuestos por Claude, **no validados por el negocio**.
- **El ICP se lee de `cerebro/contexto/` en cada corrida**, no se copia a la skill. Fit del lead: fuerte / parcial / fuera, según Rubro, Cargo (decisor) y ticket ($1.500–$3.500). Las red flags de [[cliente]] no se aplican porque están marcadas como "supuesto a validar".
- **Tipos de post:** `dolor-icp`, `educativo-generico`, `marca-personal`, decididos por el gancho sin mirar las métricas, para que el reporte pueda descubrir si alcance y tipo se contradicen.
- **Branding:** la paleta de `generar-propuesta` (`#1a1a2e`, acento `#e94560`, Inter), porque no existe guía de marca.
- **Salida y ejecución:** HTML local en `reportes/` más una fila en la base Reportes semanales (`Generado por = Manual`). Solo a pedido; sin tarea programada hasta validar el primer reporte. La skill no modifica Contenido ni Pipeline.
- **Notion es la fuente de verdad.** Si el snapshot de `CLAUDE.md` no coincide, se reporta como hallazgo; no se corrige en silencio.
- **GitHub:** se usó el repo vacío `AgustinGoniDev/Curso-BSide` (no un repo nuevo ni `lumen-lab`, que ya tiene contenido distinto). Se le advirtió al usuario que el repo era público y que la carpeta incluye clientes, MRR y pipeline; **eligió dejarlo público**. Se agregó un `.gitignore` básico y no se movió la carpeta fuera de OneDrive.

## Output

- `.claude/skills/reporte-semanal-contenido/`: `SKILL.md`, `references/` (esquema de Notion, rúbrica ICP, métricas), `scripts/` (`calcular_metricas.py`, `renderizar_reporte.py`), `assets/template-reporte.html`, `evals/evals.json`. Pasa `quick_validate.py`.
- `reportes/reporte-semanal-2026-09-20.html` y una fila en Reportes semanales para la semana 14–20 sep 2026. Revisado en escritorio y a 375 px, sin errores.
- **Hallazgo del reporte (ventana 17 ago–20 sep):** 3 de 3 leads atribuidos a contenido son ICP fuerte (Acosta & Rey, Aranda Ingeniería, Benedetti Finanzas) y salen todos de posts `dolor-icp`, que son el 31 % de las impresiones. Los 4 posts educativos genéricos se llevaron el 62 % (24.970 impresiones) con 0 leads y 0 mensajes. El post de más alcance (guía de ganchos, 8.410) no trajo ningún lead.
- Repo publicado: commit `e529e7d` "Primera versión", rama `main`, 57 archivos, en `AgustinGoniDev/Curso-BSide`.
- El wiki tiene ahora un segundo nodo de sesión; `cerebro/sources.md` suma las bases de Contenido y Reportes semanales, la skill y el repo de GitHub.

## Pendiente

- **Reporte 7–13 sep a medio hacer:** las métricas se calcularon (ventana 10 ago–13 sep: 3 de 3 leads ICP fuerte — Síntesis Digital, Acosta & Rey, Aranda) pero faltan la narrativa, el HTML y la fila en Notion. Los datos intermedios estaban en una carpeta temporal y hay que rearmarlos.
- **Datos a corregir en Notion:** el post del 20/8 (2 mensajes) y el del 11/8 (1 mensaje) no tienen lead cargado; Aranda y Benedetti no tienen Valor USD/mes; solo 6 de 15 filas del Pipeline tienen "Post que lo trajo".
- **Snapshot de `CLAUDE.md` desactualizado:** dice pipeline ~$6.000 y reunión de Síntesis Digital el 14/05; Notion muestra $8.500/mes abiertos en 8 oportunidades y Síntesis en $3.000/mes. Además la skill nueva no figura en su lista de skills.
- **Validar con el negocio** los umbrales del semáforo y las red flags **Abiertas** de [[cliente]], que condicionan el fit.
- **Decidir si `Curso-BSide` queda público.** Para pasarlo a privado: `gh repo edit AgustinGoniDev/Curso-BSide --visibility private --accept-visibility-change-consequences` (no borra lo ya expuesto).
- **Invitar al equipo** al repo (faltan los usuarios de GitHub).
- **Retomar la instalación de `claude-brain-skill`:** ya existe `.claude/skills/claude-brain/`; falta verificar si es la misma versión que el repo de GitHub.
- **Programar el reporte** los lunes (`Generado por = Tarea local`) una vez validado el primero.

## Cross-refs
- [[cliente]] — el ICP y el dolor contra los que la skill clasifica posts y leads.
- [[que-hacemos]] — oferta y ticket usados en el criterio de fit del lead.
- [[voz]] — regla de no tratar alcance ni engagement como fin, que ordena el reporte.
- [[procesos]] — etapas del funnel que aparecen como estados del Pipeline.
- [[2026-09-10-instalacion-wiki-cerebro]] — sesión que dejó pendiente conectar Notion; ahora está conectado por conector MCP.
- [[2026-10-05-skills-llamadas-y-newsletter]] — dos skills nuevas que también leen el cerebro para producir contenido.

## Fuentes
- [[sources#notion-pipeline-crm]]
- [[sources#notion-contenido]]
- [[sources#notion-reportes-semanales]]
- [[sources#skill-reporte-semanal-contenido]]
- [[sources#repo-github-curso-bside]]
