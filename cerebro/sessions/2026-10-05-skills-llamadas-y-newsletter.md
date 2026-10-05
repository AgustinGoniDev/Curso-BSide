---
type: session
area: general
date: 2026-10-05
slug: 2026-10-05-skills-llamadas-y-newsletter
title: "Skills para destilar llamadas y generar el newsletter, y consulta del cerebro ampliada"
tags: [skills, llamadas, newsletter, cerebro, voz, australis-ai]
status: active
related:
  - cliente
  - voz
  - 2026-09-23-skill-reporte-semanal-contenido
  - 2026-10-01-skills-sincronizadas-y-comando-goal
sources:
  - repo:.claude/skills/destilar-llamada/SKILL.md
  - repo:.claude/skills/generar-newsletter/SKILL.md
  - repo:cerebro/llamadas/2026-08-05-llamada-founder-agencia.md
  - repo:newsletter/2026-10-dolores-founders-agencias.md
superseded_by: null
---

# Skills para destilar llamadas y generar el newsletter, y consulta del cerebro ampliada

## Contexto

El usuario pegó la transcripción de una llamada con el founder de una agencia de marketing y
tecnología y pidió extraer síntomas, objeciones, decisiones y lo que no sirve. Después pidió
simular que la llamada era de Lumen Lab, convertir el proceso en una skill, y usar esa llamada para
armar un newsletter sobre los dolores de los founders de agencias.

## Decisiones

- **Las llamadas viven en `cerebro/llamadas/`, no en `sources.md`.** Primero se guardaron en
  `fuentes/llamadas/` con entrada en `sources.md`; el usuario corrigió: son contenido del cerebro, no
  fuentes externas. Se agregó la carpeta a `cerebro/CLAUDE.md` y una sección "Llamadas" en
  `index.md`.
- **`/destilar-llamada` destila en cuatro bloques:** síntomas (citas textuales y atribuidas),
  objeciones, lo que se decidió y lo que no sirve, más encaje con el ICP. Una llamada simulada
  queda marcada `simulada: true`.
- **La consulta del cerebro busca en sesiones y llamadas.** Para cualquier pregunta sobre un cliente
  o algo ya hablado, el modo query revisa `sessions/` y `llamadas/` (índice más Grep por nombre).
  Se agregó también una línea en el `CLAUDE.md` de la raíz y el lint pasó a leer `llamadas/`.
- **Newsletter: texto plano, una idea, un CTA, 150-250 palabras, voseo, firma "— Agustín".** Con
  esas reglas el segundo borrador mejoró mucho respecto del primero (que tenía headers, tuteo y dos
  ideas). `/generar-newsletter` lo formaliza, anonimiza a las personas y no inventa datos.

## Output

- `.claude/skills/destilar-llamada/SKILL.md` y `.claude/skills/generar-newsletter/SKILL.md`
  (ambas agregadas a la lista de skills de `CLAUDE.md`).
- `cerebro/llamadas/2026-08-05-llamada-founder-agencia.md`: ficha destilada (encaje medio con el ICP).
- `newsletter/2026-10-dolores-founders-agencias.md`: newsletter sobre depender de los referidos
  (unas 170 palabras).
- Cambios en `cerebro/CLAUDE.md`, `cerebro/index.md`, `.claude/commands/cerebro.md` y `CLAUDE.md`.

## Pendiente

- Pasar el link del último video: el newsletter tiene el marcador `[LINK AL ÚLTIMO VIDEO]` y la
  frase que lo introduce asume que habla de este tema.
- Confirmar si el founder dio el visto bueno para usar lo que dijo; mientras tanto el newsletter lo
  anonimiza. La llamada y las citas son simuladas como de Lumen Lab.
- Probar `/generar-newsletter` y `/destilar-llamada` con una llamada o un tema nuevo.
- Otras ideas de newsletter descartadas de esta llamada: dueño como cuello de botella y web o
  marca a medio hacer.

## Cross-refs
- [[cliente]] — la ficha de la llamada y el newsletter miden y cuentan el dolor del ICP (referidos, dueño en la operación, marca).
- [[voz]] — el newsletter usa la voz de Agustín (voseo) y respeta las palabras y promesas prohibidas.
- [[2026-09-23-skill-reporte-semanal-contenido]] — otra skill del proyecto que lee el cerebro para producir contenido.
- [[2026-10-01-skills-sincronizadas-y-comando-goal]] — sesión anterior sobre skills; acá se crearon dos skills nuevas.

## Fuentes
- Origen histórico (no modificar): `cerebro/llamadas/2026-08-05-llamada-founder-agencia.md`, transcripción de Fathom pegada (ficha local, no se sube) en la conversación.
