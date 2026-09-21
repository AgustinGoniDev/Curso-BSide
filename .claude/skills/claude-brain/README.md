# claude-brain

Un skill de Claude Code que instala una **LLM Wiki** (base de conocimiento estilo Obsidian) en cualquier proyecto. Un solo comando y Claude configura todo: una wiki en markdown interconectada con nodos de sesión, un índice denso, un log append-only, y un slash command (`/brain`) para operaciones de ingest, query y lint.

## Qué obtenés

Después de ejecutar el skill, tu proyecto tendrá:

```
brain/                        ← directorio de la wiki (el nombre es configurable)
├── CLAUDE.md                 ← esquema operacional (reglas para Claude)
├── index.md                  ← catálogo denso de nodos (cursor del LLM)
├── log.md                    ← bitácora append-only de operaciones
├── sources.md                ← registro de fuentes externas
├── contexto/                 ← qué ES tu negocio (se llena en el onboarding)
└── sessions/                 ← un archivo markdown por sesión
.claude/commands/brain.md     ← slash command /brain
.vscode/settings.json         ← configuración de wikilinks para Foam
```

**Y no queda vacía.** El onboarding termina con una entrevista corta sobre tu negocio, y con eso
escribe los primeros archivos en `contexto/`. Antes de cerrar, la skill le hace una pregunta a la
wiki y te muestra la respuesta, para que veas que funciona.

La diferencia entre las dos carpetas es la que ordena todo lo demás: **`sessions/` registra lo que
pasó, `contexto/` describe lo que tu negocio es.** Lo primero crece cada semana; lo segundo cambia
poco y se lee siempre.

La wiki es mantenida por Claude a través de tres operaciones:

| Comando | Qué hace |
|---------|----------|
| `/brain ingest` | Crea un nodo de sesión a partir de la conversación actual. Extrae decisiones, outputs, referencias cruzadas e ítems pendientes. Actualiza el índice y el log automáticamente. |
| `/brain query <pregunta>` | Responde usando la wiki como fuente, con citas `[[wikilink]]`. Obtiene contenido actualizado de fuentes externas cuando es necesario. |
| `/brain lint` | Chequeo de salud: wikilinks rotos, nodos huérfanos, claims desactualizados, referencias cruzadas faltantes, candidatos a nuevos conceptos. Solo lectura. |

## Requisitos previos

Antes de instalar, asegurate de tener:

- **[Claude Code](https://claude.ai/code)** — la CLI de Anthropic. Es el entorno donde se ejecutan los skills y slash commands. Sin esto, nada funciona.
- **Git** — para clonar el repositorio del skill.

Nada más. Opcionales, para después:

- **[Foam para VSCode](https://marketplace.visualstudio.com/items?itemName=foam.foam-vscode)** — si querés ver el grafo visual de tu wiki (ver más abajo).
- **Notion MCP** — solo si querés usar Notion como fuente de verdad. La skill lo detecta si ya lo tenés; si no, arranca standalone y funciona igual.

## Cómo instalar

### Paso 1 — Copiá el skill a tu proyecto

Tenés dos opciones según si querés usarlo solo en un proyecto o en todos:

```bash
# Para un proyecto específico (ejecutá esto dentro del directorio de tu proyecto)
git clone https://github.com/AgustinGoniDev/claude-brain-skill .claude/skills/claude-brain

# Para uso global (disponible en todos tus proyectos)
git clone https://github.com/AgustinGoniDev/claude-brain-skill ~/.claude/skills/claude-brain
```

> **La carpeta es `.claude/skills/`, no `.agents/skills/`.** Claude Code busca las skills ahí y sólo
> ahí. Si la ponés en otro lado, el comando no aparece y no hay ningún mensaje de error que te lo
> explique.

### Paso 2 — Ejecutá el skill desde Claude Code

Abrí Claude Code en tu proyecto y ejecutá:

```
/claude-brain
```

Claude te va a hacer las preguntas de configuración (puede hacerlas todas juntas) y va a generar toda la estructura automáticamente.

> Si el comando `/claude-brain` no aparece, verificá que el skill esté en la carpeta correcta:
> `.claude/skills/claude-brain/` (para el proyecto) o `~/.claude/skills/claude-brain/` (global).
> Y que adentro esté el `SKILL.md`, no una carpeta más de por medio.

## Qué pasa cuando lo ejecutás

El onboarding son cuatro pasos y lleva alrededor de quince minutos.

### 1 — Mira tu proyecto y te hace dos preguntas

Casi todo lo que necesita para armar la wiki está en tu proyecto, así que lo detecta en vez de
preguntártelo: el idioma, si ya tenés Notion conectado, qué material escrito tenés dado vueltas, y
si hay notas viejas que valga la pena migrar.

Lo único que te pregunta es lo que no puede adivinar:

- **Cómo se llama tu proyecto o negocio**
- **Cuáles son tus áreas de trabajo** — y te propone a partir de lo que encontró

El nombre de la carpeta y del comando salen por default (`brain`, o `cerebro` si escribís en
español). Si no te gustan, lo decís y los cambia.

> Si no tenés Notion ni ninguna otra herramienta conectada, arranca standalone. Funciona completa
> así, y conectar una fuente externa es un paso que podés dar después.

### 2 — Genera la estructura

Los archivos de la wiki, el slash command y la configuración de Foam. Los vas viendo aparecer.

### 3 — Te entrevista sobre tu negocio

Acá es donde la wiki deja de estar vacía. Cuatro áreas, una pregunta por vez, y **un archivo escrito
al cerrar cada una**:

| Área | Produce |
|------|---------|
| Qué hace el negocio | `contexto/que-hacemos.md` |
| Quién compra | `contexto/cliente.md` |
| Cómo se trabaja | `contexto/procesos.md` |
| Cómo se escribe y qué no se dice | `contexto/voz.md` |

**Si ya tenés material escrito** —un README, documentos, notas— los lee antes de la primera pregunta
y no te vuelve a preguntar lo que ahí ya está contestado. Nada entra a la wiki sin que lo apruebes.

**"No sé" es una respuesta válida.** Queda anotado como abierto y sigue. Y podés cortar en cualquier
área: tres archivos honestos sirven más que cuatro rellenados.

### 4 — Lo prueba y te lo muestra

Antes de cerrar le hace una pregunta a la wiki y te muestra la respuesta, para que veas que
efectivamente sabe algo de tu negocio. Después te dice qué sabe, **qué no sabe**, y un solo próximo
paso.

## Cómo funciona

Cada nodo de sesión es un archivo markdown con frontmatter YAML y seis secciones fijas:

```yaml
---
type: session
area: marketing
date: 2026-04-10
slug: email-infrastructure-setup
title: "Infraestructura de captura de emails: Brevo + n8n + Nginx"
tags: [email, lead-magnet, brevo, n8n, nginx]
status: active
related:
  - 2026-04-04-cold-email-sequence
sources:
  - notion:email-strategy
  - repo:.claude/plans/email-infra.md
superseded_by: null
---

## Contexto
## Decisiones
## Output
## Pendientes
## Cross-refs
- [[2026-04-04-cold-email-sequence]] — misma fecha, pieza complementaria
## Fuentes
- [[sources#email-strategy]] (Notion)
```

Los links internos usan la sintaxis `[[slug]]` (wikilinks). El índice (`index.md`) es el cursor principal: Claude lo lee primero en cada operación para decidir qué nodos abrir, sin leer toda la wiki de una vez.

## Visualización del grafo con Foam

Para ver el grafo visual de tu wiki, instalá la extensión **Foam** en Visual Studio Code:

1. Abrí el panel de extensiones (`Ctrl+Shift+X` en Windows/Linux, `Cmd+Shift+X` en Mac)
2. Buscá **"Foam"** y elegí la extensión de "Foam team"
3. Instalala y recargá VSCode
4. Con tu proyecto abierto, usá el comando **"Foam: Show Graph"** desde la paleta de comandos (`Ctrl+Shift+P` / `Cmd+Shift+P`)

Con Foam vas a tener:
- `[[wikilinks]]` clickeables en el editor
- Grafo visual interactivo de todos los nodos y sus conexiones
- Panel de backlinks (qué nodos apuntan al nodo actual)
- Autocompletado al escribir `[[`

El skill configura `.vscode/settings.json` automáticamente para que el grafo no incluya carpetas innecesarias como `.claude/` o sesiones legacy.

## Configuración de Notion (solo si usás ese backend)

Si elegiste Notion como fuente de verdad, necesitás:

1. Configurar el **MCP de Notion** en el archivo `.mcp.json` de tu proyecto
2. Completar `brain/sources.md` con los IDs cortos y URLs de tus páginas de Notion

Claude va a hacer fetch automático del contenido de Notion cuando lo necesite en una query.

## El patrón

Este skill implementa el **patrón LLM Wiki - Karpathy**: una base de conocimiento persistente y auto-compilada donde el LLM es tanto el escritor como el lector. La clave está en que Claude lee el índice primero en cada operación, haciendo que la recuperación sea O(índice) y no O(todos-los-archivos). Las referencias cruzadas son bidireccionales y se verifican en cada ingest.

La arquitectura de tres capas:
1. **Fuentes brutas** — páginas de Notion, archivos del repo (inmutables, obtenidos frescos)
2. **Wiki** — `brain/` — nodos de sesión con frontmatter, índice denso, referencias cruzadas
3. **Esquema** — `brain/CLAUDE.md` — el manual operacional que Claude lee antes de cada operación

## Licencia

MIT
