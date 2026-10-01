---
type: session
area: general
date: 2026-10-01
slug: 2026-10-01-skills-sincronizadas-y-comando-goal
title: "Skills sincronizadas de claude.ai y el comando /goal"
tags: [skills, claude-code, propuestas, australis-ai, automatizacion]
status: active
related:
  - procesos
  - 2026-09-28-landing-page-lumen-lab
sources:
  - repo:CLAUDE.md
  - url:https://code.claude.com/docs/en/goal.md
superseded_by: null
---

# Skills sincronizadas de claude.ai y el comando /goal

## Contexto

Sesión de consultas, sin producción. El usuario preguntó tres cosas: si estaba disponible la skill
`cotizacion-australis`, si se podía editar y para qué sirve el comando `/goal` de Claude Code.

## Decisiones

- **Dos skills de propuestas, cada una para su negocio.** `cotizacion-australis` es de Australis AI
  y genera un `.docx` con la estructura de esa agencia. `/generar-propuesta` es la de Lumen Lab y
  genera la propuesta HTML más el email de envío. Para prospectos de Lumen Lab se usa siempre
  `/generar-propuesta`.
- **Las skills sincronizadas se editan en claude.ai, no en local.** `cotizacion-australis` es una
  skill personal que se sincroniza desde la cuenta de claude.ai. Su copia local está en
  `~/.claude/skills/synced/<id>/cotizacion-australis/` (`SKILL.md` + `references/ejemplo-propuesta.md`)
  y la próxima sincronización pisa cualquier cambio hecho ahí. Para editarla hay dos caminos:
  hacerlo desde claude.ai (Settings → Capabilities → Skills) o armar la versión nueva en local,
  empaquetarla en `.zip` y subirla a claude.ai para reemplazar la actual.
- **`/goal` sirve para tareas con un resultado final comprobable.** Define una condición de
  cierre y Claude sigue trabajando solo, vuelta tras vuelta, hasta cumplirla. Después de cada
  vuelta, un modelo chico (Haiku, por defecto) evalúa si la condición se cumplió, juzgando solo
  por lo que Claude fue diciendo. Para que funcione bien, la condición tiene que describir un
  resultado verificable, decir cómo se comprueba y llevar un tope (por ejemplo, "o frená después
  de 15 vueltas"). Es distinto de `/loop`, que repite una tarea cada cierto tiempo. No anda si
  los hooks están desactivados.

## Output

- Ningún archivo del proyecto modificado (solo este nodo y el registro en el wiki).
- Ubicación confirmada de `cotizacion-australis`: `~/.claude/skills/synced/...` y una copia vieja
  en `~/.claude/skills/.trash/`.

## Pendiente

- Si se quiere cambiar `cotizacion-australis`: definir qué cambiar, leer su `SKILL.md` actual y
  generar la versión nueva para subirla a claude.ai.

## Cross-refs
- [[procesos]] — el proceso de propuestas de Lumen Lab que cubre `/generar-propuesta`, distinto de la skill de Australis AI.
- [[2026-09-28-landing-page-lumen-lab]] — el ejemplo de `/goal` usó la verificación de esta landing; las dos sesiones tocan Australis AI.

## Fuentes
- [[sources#claude-code-goal-docs]]
- Origen histórico (no modificar): `~/.claude/skills/synced/.../cotizacion-australis/SKILL.md`
