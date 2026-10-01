---
type: contexto
area: general
date: 2026-09-10
slug: procesos
title: "Cómo se trabaja en Lumen Lab"
tags: [funnel, ventas, onboarding, retainer, equipo]
status: active
related:
  - que-hacemos
  - cliente
  - voz
sources:
  - repo:CLAUDE.md
  - repo:docs/proceso-ventas.md
  - repo:docs/proceso-operativo.md
  - repo:docs/equipo-roles.md
superseded_by: null
---

Recorrido desde que alguien muestra interés hasta que está cobrado y entregado.

## Funnel de ventas

1. **Prospección (outbound sistematizado)** — identificación del prospecto + research (skill `/investigar-prospecto`), envío de Email 1 ("Consultor, no Vendedor").
2. **Seguimiento / manejo de objeciones** — Email 2 si el prospecto objeta. **Abierto:** cadencia exacta de seguimiento si no responde, no confirmada.
3. **Reunión** — se agenda con el prospecto calificado según el ICP.
4. **Propuesta** — input: cliente + dolor + alcance acordado en la reunión. Output: propuesta HTML + email de envío. Tiempo objetivo: menos de 20 minutos (skill `/generar-propuesta`).
5. **Cierre** — ratio de cierre histórico: 55%.
6. **Onboarding** — arranca la ejecución del retainer.

## Ciclo mensual del retainer

**Abierto:** la secuencia de onboarding y la cadencia exacta del ciclo mensual están marcadas como "supuesto a validar" en `docs/proceso-operativo.md` — adaptadas de la oferta, no confirmadas paso a paso por el dueño.

En términos generales: producción de contenido (4–8 posts LinkedIn + newsletter mensual), outbound sistematizado, y reporting/reunión de seguimiento mensual con el cliente.

## Qué está escrito vs. qué vive en la cabeza de Tomás

El pipeline hoy vive en la cabeza de Tomás Ruiz (dueño). Usa Notion para tracking básico (Pipeline CRM, ver `cerebro/sources.md`). El objetivo declarado de este wiki es que Claude pueda manejar el contexto operativo para que Tomás empiece a delegar decisiones rutinarias.

## Equipo

8 personas (5 fijos + 3 freelancers). Tomás Ruiz está en todos los frentes: atiende clientes, cierra propuestas, supervisa el contenido.

**Abierto:** nombres y roles individuales del resto del equipo (4 fijos + 3 freelancers) no están documentados — pendiente de completar.

## Cross-refs
- [[que-hacemos]] — la oferta que se produce y entrega en este proceso.
- [[cliente]] — el perfil que se califica en el paso de calificación del funnel.
- [[voz]] — el framework de Email 1 usado en el paso de prospección.
- [[2026-09-10-instalacion-wiki-cerebro]] — sesión donde se pobló este archivo desde `docs/`.
- [[2026-09-23-skill-reporte-semanal-contenido]] — skill que reporta cada semana cómo el contenido alimenta las etapas del funnel.
- [[2026-10-01-skills-sincronizadas-y-comando-goal]] — aclara que las propuestas de Lumen Lab van por `/generar-propuesta`, no por la skill de Australis AI.
