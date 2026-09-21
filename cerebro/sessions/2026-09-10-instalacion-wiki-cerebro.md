---
type: session
area: general
date: 2026-09-10
slug: 2026-09-10-instalacion-wiki-cerebro
title: "Instalación del wiki cerebro"
tags: [claude-brain, cerebro, onboarding, setup]
status: active
related:
  - que-hacemos
  - cliente
  - procesos
  - voz
sources:
  - repo:CLAUDE.md
  - repo:docs/README.md
  - url:https://github.com/AgustinGoniDev/claude-brain-skill
superseded_by: null
---

# Instalación del wiki cerebro

## Contexto

El usuario pidió analizar e instalar el skill `claude-brain` (repo público `AgustinGoniDev/claude-brain-skill`) para montar una LLM Wiki en el proyecto Lumen Lab. El proyecto ya tenía documentación de negocio en `docs/` (ICP, ofertas, procesos, voz) pero no un sistema de wiki con nodos de sesión ni slash command dedicado. El repo ya tenía un `/memoria` mencionado en `CLAUDE.md`, pero no estaba instalado en el proyecto — el sistema que terminó instalándose y quedando activo es `cerebro/` con el comando `/cerebro`.

## Decisiones

- **Nombre del wiki:** `cerebro/` (no `brain/`) por ser el idioma español de la conversación. Comando: `/cerebro`.
- **Nombre del proyecto:** Lumen Lab, tomado directamente del `CLAUDE.md` de la raíz sin preguntarlo (ya estaba confirmado ahí).
- **Áreas de trabajo:** una sola área, `general`, por elección explícita del usuario en vez de las 4 propuestas (prospección/ventas, clientes, contenido/voz, operaciones). Se puede subdividir más adelante si crece.
- **Backend:** standalone (`D`) — no hay `.mcp.json` ni MCP de Notion conectado en el proyecto. El Pipeline CRM de Notion quedó documentado en `cerebro/sources.md` como referencia manual, sin fetch automático.
- **Captura de contexto sin entrevista completa:** en vez de correr la entrevista de 4 preguntas de la Fase 3 del skill, se generaron los 4 archivos de `contexto/` (`que-hacemos`, `cliente`, `procesos`, `voz`) directamente a partir del material ya existente en `docs/`, porque ya cubría lo que la entrevista buscaba. Los huecos que `docs/` marcaba como "supuesto a validar" se preservaron como `**Abierto:**` en vez de inventarse.
- Después de instalado, `CLAUDE.md` (raíz) se actualizó (por el usuario, fuera de esta conversación) para instruir que siempre se use `cerebro/` al responder consultas.

## Output

- `cerebro/CLAUDE.md` — esquema operativo del wiki (frontmatter, wikilinks, reglas de ingest/query/lint).
- `cerebro/index.md` — catálogo con las 4 entradas de contexto y la sección de sesiones (área `general`).
- `cerebro/log.md` — bitácora, con el bootstrap inicial.
- `cerebro/sources.md` — registro de fuentes, incluye el link al Pipeline CRM de Notion.
- `cerebro/contexto/que-hacemos.md`, `cliente.md`, `procesos.md`, `voz.md` — poblados desde `docs/`.
- `cerebro/sessions/` — creado, este nodo es el primero.
- `.claude/commands/cerebro.md` — slash command (ingest | query | lint).
- `.vscode/settings.json` — creado nuevo, con `foam.files.ignore`.
- `.claude/skills/claude-brain/` — el skill clonado desde GitHub (instalador, no parte del wiki en sí).
- Se probó el wiki con dos queries reales ("¿quiénes somos y qué hacemos?" y "¿a quién le vendemos?"), ambas respondidas correctamente citando `contexto/`.

## Pendiente

- Completar con Tomás los huecos marcados `**Abierto:**` en `contexto/cliente.md` (red flags y preguntas de calificación no confirmadas) y en `contexto/que-hacemos.md` (condiciones comerciales) y `contexto/procesos.md` (roles individuales del equipo, cadencia exacta del ciclo mensual).
- Decidir si en algún momento se conecta el MCP de Notion como backend (hoy standalone) para que las queries puedan traer el pipeline fresco en vez de solo el link de referencia.
- Instalar la extensión Foam en VSCode si se quiere ver el grafo visual (no confirmado si ya está instalada).
- Evaluar si conviene subdividir el área `general` en áreas más específicas (ventas, clientes, contenido, operaciones) a medida que crezcan las sesiones.

## Cross-refs
- [[que-hacemos]] — contexto de negocio poblado en esta sesión.
- [[cliente]] — contexto de negocio poblado en esta sesión.
- [[procesos]] — contexto de negocio poblado en esta sesión.
- [[voz]] — contexto de negocio poblado en esta sesión.

## Fuentes
- Origen histórico (no modificar): `CLAUDE.md`
- Origen histórico (no modificar): `docs/README.md`
- [Repo del skill instalado](https://github.com/AgustinGoniDev/claude-brain-skill)
