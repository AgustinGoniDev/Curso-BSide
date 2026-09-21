---
name: claude-brain
description: >
  Instala un LLM Wiki (knowledge base markdown interconectado, estilo Carpati/Obsidian)
  en cualquier proyecto y lo puebla con el contexto del negocio mediante una entrevista
  corta. Genera la carpeta del wiki con schema operativo, índice, bitácora y registro de
  fuentes, más el slash command (ingest | query | lint) y la configuración de Foam para
  VSCode; después entrevista al usuario sobre su negocio y escribe los documentos de
  contexto. Usá este skill cuando el usuario diga "instalá el cerebro", "quiero un wiki
  LLM", "configurá el sistema de memoria", "armá el brain", "montá el knowledge base",
  "cargá el contexto de mi negocio", o cuando pida un sistema de conocimiento acumulativo
  mantenido por Claude.
---

# claude-brain

Instalador interactivo de un LLM Wiki para cualquier proyecto. Hace preguntas,
genera toda la estructura adaptada al contexto del usuario, e instala la configuración
necesaria para que Claude pueda mantener el wiki con `/brain ingest`, `/brain query`
y `/brain lint`.

El sistema está basado en el patrón Carpati: un knowledge base de markdown interconectado
con wikilinks Foam, nodos de sesión con frontmatter YAML, índice denso para el LLM,
bitácora append-only y registro de fuentes externas.

---

## Fase 1: Mirar el proyecto y preguntar sólo lo que falta

**Antes de la primera pregunta, mirá el proyecto.** La mayoría de lo que hace falta para generar
está ahí y no hay por qué preguntarlo.

Cada pregunta que hacés es una decisión que le pedís al usuario cuando todavía no sabe qué está
comprando. Preguntá dos, no siete.

### Lo que se detecta

| Qué | Cómo | Qué hacer con eso |
|---|---|---|
| **Idioma** | El de la conversación en curso | Usarlo. No preguntar |
| **Backend** | ¿Hay MCP de Notion en `.mcp.json`? | Si lo hay, proponerlo en una línea. Si no, standalone |
| **Material existente** | `README`, `docs/`, notas sueltas en la raíz | Guardarlo para la Fase 3. **No leerlo todavía** |
| **Sesiones históricas** | Logs, changelogs, carpetas de notas fechadas | Si aparecen candidatos, ofrecerlo. Si no, **ni mencionarlo** |

**Cómo se propone el backend detectado**, en una línea y con salida:

> "Vi que tenés Notion conectado. ¿Lo uso como fuente de verdad o arrancamos standalone?"

Si no hay nada detectado, **no preguntes**: standalone es el default correcto y se puede conectar
después.

> **Por qué standalone por default:** una wiki sin fuente externa funciona completa desde el minuto
> uno. Conectar Notion agrega valor pero también agrega un MCP que configurar, IDs que cargar y una
> forma nueva de que algo falle. No es una decisión para el minuto dos de un onboarding.

### Las dos preguntas

**1. Nombre del proyecto**
> "¿Cómo se llama tu proyecto o tu negocio?"

Es lo único que no se puede inferir de ninguna manera.

**2. Áreas de trabajo**
> "¿Cuáles son tus áreas de trabajo?"

**Sugerí a partir de lo que detectaste** en vez de preguntar en abstracto. Si el proyecto tiene
carpetas que parecen áreas, proponelas. Si no hay señal, ofrecé una sola área para empezar y aclarar
que se agregan después: arrancar con `general` y crecer es mejor que inventar seis categorías vacías.

### Lo que se resuelve solo

| Variable | Default |
|---|---|
| Directorio del wiki | `brain`, o `cerebro` si el idioma es español |
| Nombre del comando | Igual al directorio |

Decilo al pasar, no lo preguntes: *"te la armo en `cerebro/`, con el comando `/cerebro`"*. Si al
usuario no le gusta, lo dice — y ahí sí cambialo.

### Secciones según idioma

- Español: Contexto, Decisiones, Output, Pendiente, Cross-refs, Fuentes
- English: Context, Decisions, Output, Pending, Cross-refs, Sources
- Otro: adaptar manteniendo el mismo orden y función

---

## Fase 2: Generación de archivos

Con lo detectado y lo preguntado, generá los siguientes archivos usando los templates de
`references/`.

### Variables a resolver antes de generar

```
WIKI_DIR        = default: "brain" ("cerebro" si el idioma es español)
COMMAND_NAME    = igual a WIKI_DIR
PROJECT_NAME    = pregunta 1
AREA_ENUM       = pregunta 2, separadas por " | " (ej: "marketing | ops | dev")
SECTION_CONTEXT     = "Contexto" | "Context" | custom
SECTION_DECISIONS   = "Decisiones" | "Decisions" | custom
SECTION_OUTPUT      = "Output" (igual en todos los idiomas)
SECTION_PENDING     = "Pendiente" | "Pending" | custom
SECTION_CROSS_REFS  = "Cross-refs" (igual en todos los idiomas)
SECTION_SOURCES     = "Fuentes" | "Sources" | custom
BACKEND_TYPE    = detectado en Fase 1. Sin señal → D (standalone)
HAS_LEGACY      = detectado en Fase 1. Sin candidatos → false
```

### Archivos a crear

#### 1. `<WIKI_DIR>/CLAUDE.md`

Tomá el template de `references/brain-claude-md.md` y reemplazá todos los placeholders:

- `{{WIKI_DIR}}` → WIKI_DIR
- `{{COMMAND_NAME}}` → COMMAND_NAME
- `{{AREA_ENUM}}` → AREA_ENUM
- Los seis nombres de sección según idioma, **uno por uno y sin comodines**:
  `{{SECTION_CONTEXT}}` · `{{SECTION_DECISIONS}}` · `{{SECTION_OUTPUT}}` · `{{SECTION_PENDING}}` ·
  `{{SECTION_CROSS_REFS}}` · `{{SECTION_SOURCES}}`
- `{{SECTION_TITLE}}` → **no es un nombre de sección.** Marca dónde va el título del nodo dentro del
  ejemplo de cuerpo. Reemplazalo por el texto literal `título del nodo`, para que el esquema generado
  lea `# <título del nodo>`. Si lo tratás como los anteriores, el esquema termina diciendo que cada
  nodo se titula "Contexto"
- `{{SOURCE_PREFIX}}` → según backend:
  - A (Notion): `notion`
  - B (archivos): `repo`
  - C (otro): el prefijo que tenga más sentido para la herramienta
  - D (ninguno): `repo`
- `{{BACKEND_QUERY_RULE}}` → según backend:
  - A: "Si algún nodo cita una fuente Notion (vía `sources.md`) Y la pregunta depende del contenido fresco, resolvé vía `mcp__notion__notion-fetch` usando la URL de `sources.md`. **NO respondas desde el resumen cache de `sources.md`** — ése es sólo un directorio."
  - B: "Si la pregunta depende del contenido actual de un archivo del repo, leelo directamente con Read. El wiki guarda punteros, no copias."
  - C: "Si la pregunta depende de contenido fresco de [nombre herramienta], consultala directamente. El wiki guarda punteros, no copias del contenido."
  - D: "Respondé exclusivamente desde los nodos del wiki. Si el contenido no está en el wiki, decilo explícitamente."
- `{{BACKEND_SECTION}}` → **el bloque entero**, separador y título incluidos, o nada.

  Con backend **D no hay sección de integración**: reemplazá el placeholder por **string vacío**.
  No lo dejes como título sin cuerpo — un `##` colgado en el esquema generado es basura que después
  el usuario lee y no entiende.

  Para A, B y C, el bloque completo es:

  ````
  ---

  ## <título según backend>

  <cuerpo según backend>
  ````

  | Backend | Título | Cuerpo |
  |---|---|---|
  | A | Integración con Notion | Notion es la fuente de verdad del proyecto. Los nodos referencian páginas de Notion con IDs cortos definidos en `{{WIKI_DIR}}/sources.md`. Claude **debe** hacer `mcp__notion__notion-fetch` con la URL correspondiente cuando la query depende del contenido fresco de una página. El resumen cache en `sources.md` solo sirve para decidir si vale la pena hacer fetch. |
  | B | Integración con archivos del repo | Los archivos del repo son la fuente de verdad. Los nodos referencian archivos con `repo:<path>` en el frontmatter. Cuando una query depende del contenido actual de un archivo, Claude lo lee directamente con Read. El wiki no duplica el contenido — guarda punteros. |
  | C | Integración con [nombre herramienta] | Las instrucciones de integración que dio el usuario. |
- `{{LEGACY_NOTE}}` → según HAS_LEGACY:
  - true: "**NUNCA** tocar los archivos de sesiones legacy marcados como 'histórico inmutable' en `{{WIKI_DIR}}/sources.md`. Son histórico congelado. Nuevas sesiones van SOLO a `{{WIKI_DIR}}/sessions/`."
  - false: *(string vacío)*
- `{{LANGUAGE_RULE}}` → según idioma:
  - Español: "- Contenido de nodos: **español**.\n- Tags y slugs: **español sin tildes, kebab-case**.\n- Frontmatter keys: **inglés** (convención técnica)."
  - English: "- Node content: **English**.\n- Tags and slugs: **English, kebab-case**.\n- Frontmatter keys: **English**."
  - Otro: "- Contenido de nodos: **[idioma elegido]**.\n- Tags y slugs: kebab-case.\n- Frontmatter keys: **inglés** (convención técnica)."

#### 2. `<WIKI_DIR>/index.md`

Generá directamente (no hay template separado):

```markdown
# <WIKI_DIR> — Index

> Node catalog. One one-liner per node. Organized by type and then by area.
> To operate this wiki, read `CLAUDE.md` in this directory.
> When querying, read this file first to decide which nodes to open.

**Last updated:** <FECHA DE HOY>
**Total nodes:** 0 sessions | 0 concepts | 0 ADRs

---

## Contexto del negocio

> Lo que el sistema sabe del negocio. Se lee antes de producir cualquier cosa.

*(vacío — se puebla con la captura de la Fase 3)*

---

## Sessions

<una sección H3 por cada área en AREA_ENUM, en orden alfabético>
### <área-1>

*(empty)*

### <área-2>

*(empty)*

[... una por cada área ...]

---

## Concepts

*(empty — will emerge organically via `/<COMMAND_NAME> lint` when a term appears in 3+ nodes)*

## ADRs

*(empty)*
```

Si el idioma es español, los headers van en español: "Sesiones", "Conceptos".

#### 3. `<WIKI_DIR>/log.md`

```markdown
# <WIKI_DIR> — Operations Log

> Append-only. Most recent entries at the **end**.
> Format: `## [YYYY-MM-DD HH:MM] <operation> | <slug-or-target>`
> Valid operations: `bootstrap`, `ingest`, `update`, `rename`, `merge`, `split`, `lint`, `deprecate`.

---

## [<FECHA HOY> <HORA ACTUAL>] bootstrap | wiki-initialized
- Created: CLAUDE.md, index.md, log.md, sources.md, sessions/
- Areas: <AREA_ENUM>
- Backend: <BACKEND_TYPE description>
- Generated by: skill claude-brain v1
```

#### 4. `<WIKI_DIR>/sources.md`

Usá el template correspondiente de `references/sources-templates.md`:
- Backend A (Notion) → TEMPLATE A
- Backend B (archivos) → TEMPLATE B
- Backend C (otro) → TEMPLATE D (completando `{{CUSTOM_BACKEND_NAME}}` e instrucciones)
- Backend D (ninguno) → TEMPLATE C

Reemplazá `{{WIKI_DIR}}` con WIKI_DIR.

#### 5. `<WIKI_DIR>/sessions/.gitkeep`

Archivo vacío para que git trackee el directorio vacío:
```
```
*(archivo completamente vacío)*

#### 5b. `<WIKI_DIR>/contexto/.gitkeep`

Igual: archivo vacío. Acá van los documentos que describen el negocio, que se escriben en la Fase 3.

**Por qué está separado de `sessions/`:** las sesiones registran lo que pasó; el contexto describe
lo que el negocio **es**. Lo primero crece todas las semanas, lo segundo cambia poco y se lee
siempre. Mezclarlos hace que el sistema cargue novedades cuando necesita fundamentos.

#### 6. `.claude/commands/<COMMAND_NAME>.md`

Tomá el template de `references/brain-command.md` y reemplazá:
- `{{WIKI_DIR}}` → WIKI_DIR
- `{{COMMAND_NAME}}` → COMMAND_NAME
- `{{PROJECT_NAME}}` → PROJECT_NAME
- `{{SECTION_DECISIONS}}`, `{{SECTION_OUTPUT}}`, `{{SECTION_PENDING}}`, `{{SECTION_CROSS_REFS}}` → nombres de secciones según idioma
- `{{BACKEND_QUERY_STEP}}` → misma regla que `{{BACKEND_QUERY_RULE}}` en CLAUDE.md
- `{{LEGACY_INGEST_NOTE}}` → según HAS_LEGACY:
  - true: "**NUNCA** toques los archivos de sesiones legacy marcados como inmutables. Son histórico congelado."
  - false: *(string vacío)*

#### 7. `.vscode/settings.json`

Este paso requiere lógica de merge:

**Si `.vscode/settings.json` NO existe:**
```json
{
  "foam.files.ignore": [
    "**/.claude/**",
    "**/node_modules/**"
  ]
}
```
(Si HAS_LEGACY=true, agregar también los paths de las carpetas legacy que el usuario indicó.)

**Si `.vscode/settings.json` YA existe:**
1. Leer el archivo actual con Read
2. Verificar si `foam.files.ignore` existe en el JSON
   - Si existe: agregar los nuevos paths al array existente (sin pisar los que ya están)
   - Si no existe: agregar el key `foam.files.ignore` con los paths nuevos
3. Usar Edit para hacer el cambio quirúrgico (NO sobreescribir el archivo completo)

Paths a agregar al array:
- `**/.claude/**`
- `**/node_modules/**`
- Si HAS_LEGACY=true, por cada carpeta de sesiones legacy que el usuario mencione: `**/<carpeta>/sessions/**`

---

## Fase 3: Captura del contexto del negocio

El wiki ya está montado, pero **está vacío**: sabe cómo guardar información y no sabe nada del
negocio. Un wiki sin contexto es un archivador.

Esta fase lo puebla con una entrevista corta de cuatro áreas, que produce cuatro archivos en
`<WIKI_DIR>/contexto/`.

**Seguí `references/captura-contexto.md`.** Ahí está el guion completo: las preguntas de apertura,
las repreguntas, qué se busca en cada área y cómo se escribe cada archivo.

| # | Área | Produce |
|---|---|---|
| 1 | Qué hace el negocio | `que-hacemos.md` |
| 2 | Quién compra | `cliente.md` |
| 3 | Cómo se trabaja | `procesos.md` |
| 4 | Cómo se escribe y qué no se dice | `voz.md` |

**Las reglas que no se negocian:**

- **Una pregunta por vez.** Preguntá, frená, esperá. Nunca una lista numerada.
- **Un archivo escrito al cerrar cada área**, y decilo en voz alta. El usuario tiene que ver que
  algo se construye mientras habla.
- **Máximo una repregunta por área.** Es una primera pasada, no la versión definitiva.
- **Nunca escribas algo que el usuario no haya dicho.** Los huecos se marcan `**Abierto:** ...`.
- **Se puede cortar en cualquier área.** Mejor tres archivos honestos que cuatro rellenados.

Al cerrar cada área, agregá la línea correspondiente a la sección **Contexto del negocio** de
`<WIKI_DIR>/index.md`.

**Si el usuario prefiere saltear esta fase**, decile en una línea que el wiki queda funcionando pero
sin saber nada del negocio, y que puede correr la captura después. No insistas.

---

## Fase 4: Verificar y cerrar

Antes del resumen, **probala**. Un onboarding que no verifica nada deja al usuario descubriendo los
problemas solo, tres días después.

### 1. Que la wiki responda

Hacele a la wiki recién sembrada una pregunta que sólo pueda contestar desde `contexto/`:

> ¿Quiénes somos y qué hacemos?

Seguí las reglas de query del esquema y **mostrale la respuesta**. Si contesta con el negocio del
usuario, el contexto entró. Si contesta genérico o dice que no sabe, algo falló en la Fase 3:
decilo y ofrecé rehacer el área que falta.

Es el momento en que el usuario entiende qué acaba de instalar. No lo saltees.

### 2. Que no haya quedado nada a medias

Chequeá, sin anunciarlo como una lista de tareas:

- **Ningún `{{PLACEHOLDER}}`** sin reemplazar en los archivos generados
- **El índice refleja lo que existe** — cada archivo de `contexto/` tiene su línea
- **El slash command está donde corresponde** — `.claude/commands/<COMMAND_NAME>.md`

Si algo falta, arreglalo antes de mostrar el resumen. Si no se puede arreglar, decilo con todas las
letras en el resumen: un onboarding que reporta éxito sobre algo roto es peor que uno que falla.

### 3. El resumen

Mostrá esto al usuario:

```
## claude-brain instalado

Wiki en: <WIKI_DIR>/
Comando: /<COMMAND_NAME> (ingest | query | lint)

### Archivos generados
<WIKI_DIR>/CLAUDE.md          ← abrí este para ver las reglas del wiki
<WIKI_DIR>/index.md           ← catálogo de nodos
<WIKI_DIR>/log.md             ← bitácora de operaciones
<WIKI_DIR>/sources.md         ← registro de fuentes externas
<WIKI_DIR>/contexto/          ← lo que el sistema sabe de tu negocio
<WIKI_DIR>/sessions/          ← acá van a vivir los nodos de sesión
.claude/commands/<COMMAND_NAME>.md  ← slash command instalado
.vscode/settings.json         ← configuración Foam (creado o actualizado)

### Lo que el sistema sabe de tu negocio
<una línea por cada archivo escrito en la Fase 3, con lo que cubre>
<si alguna área quedó pendiente, decilo acá en una línea>

### Probalo ahora
Preguntale al sistema "¿quiénes somos y qué hacemos?" y fijate si responde con
tu negocio. Si responde genérico, falta contexto.

### Próximos pasos
1. Instalar la extensión Foam en VSCode (si no la tenés):
   Marketplace: "Foam" de Foam team, o buscar foam-vscode
<SI BACKEND=A>
2. Completar brain/sources.md con las URLs de tus páginas de Notion
3. Asegurate de tener el MCP de Notion configurado en .mcp.json
</SI BACKEND=A>
<SI HAS_LEGACY=true>
2. Podés migrar sesiones históricas manualmente: copiá el contenido, agregá
   el frontmatter YAML y guardá en <WIKI_DIR>/sessions/YYYY-MM-DD-slug.md
</SI HAS_LEGACY>
4. Al final de tu primera sesión de trabajo, corré `/<COMMAND_NAME> ingest`
```

---

## Notas para el LLM

- Los templates en `references/` usan placeholders con doble llave `{{PLACEHOLDER}}`. Reemplazalos todos antes de escribir los archivos.
- No dejes ningún placeholder sin reemplazar en los archivos generados.
- Si el usuario da nombres en mayúsculas o con espacios para las áreas, convertirlos a kebab-case lowercase para el enum del frontmatter (ej: "Marketing Digital" → `marketing-digital`), pero mostrar el nombre original en el índice.
- El archivo `.vscode/settings.json` es el único que requiere lógica de merge — todos los demás se crean nuevos.
- Si `.claude/commands/` no existe, crearlo también.
- Verificar antes de crear que `<WIKI_DIR>/` no existe ya para evitar sobreescribir un wiki existente. Si existe, avisar al usuario y preguntar si quiere continuar.
