# cerebro — Schema operativo

Este directorio es el "brain" del proyecto: un wiki markdown interconectado
mantenido por Claude. Si estás leyendo este archivo, probablemente fuiste invocado
por el comando `/cerebro`. Seguí estas reglas al pie de la letra.

---

## Qué es cada archivo

- `index.md` — catálogo denso de nodos. Punto de entrada para cualquier query o ingest.
- `log.md` — bitácora append-only de **operaciones sobre el wiki** (ingest, lint, rename, merge). No es el log de trabajo — eso vive en los nodos.
- `sources.md` — registro de fuentes externas. Directorio, no cache de contenido.
- `contexto/` — qué **es** este negocio. Se lee antes de producir cualquier cosa.
- `sessions/` — nodos de sesión. Planos, un archivo por sesión.
- `llamadas/` — fichas de llamadas destiladas con `/destilar-llamada`. Un archivo por llamada (síntomas, objeciones, decisiones).
- `CLAUDE.md` — este archivo.

**La diferencia entre `contexto/` y `sessions/`** es la que ordena todo lo demás: las sesiones
registran lo que pasó, el contexto describe lo que el negocio es. Lo primero crece cada semana; lo
segundo cambia poco y se lee siempre.

---

## Tipos de nodo

Dos al arranque:

- **contexto** — vive en `contexto/`. Lo escribe la captura del onboarding y se actualiza cuando el
  negocio cambia, no cuando pasa algo.
- **session** — vive en `sessions/`. Uno por sesión de trabajo.

Conceptos, ADRs, entidades y personas emergerán orgánicamente vía `lint` cuando el patrón se repita
en 3+ nodos.

**NO** crear nodos de otros tipos preventivamente.

---

## Frontmatter obligatorio en cada nodo

Mismos campos para los dos tipos. Lo único que cambia es `type` y dónde vive el archivo.

```yaml
---
type: session                   # session | contexto
area: <general>
date: YYYY-MM-DD
slug: <slug-del-nombre-de-archivo-sin-fecha-ni-.md>
title: "<título humano>"
tags: [<libres, kebab-case>]
status: active                  # active | superseded | archived
related:
  - <slug-sin-.md>
sources:
  - repo:<id-o-path>
superseded_by: null             # slug del nodo que reemplaza a éste, o null
---
```

Reglas:
- `slug`: igual al nombre de archivo sin fecha ni `.md`. Kebab-case, ≤6 palabras. Describe el resultado, no el proceso.
- `area`: ruta relativa inequívoca. Single-value. Si una sesión toca dos áreas, crear dos nodos cross-linked, o uno con área primaria y cross-ref.
- `related`: slugs sin `.md`. Máx. 5. El LLM los detecta por tags solapados, misma área o proximidad cronológica.
- `sources`: prefijos válidos: `repo:<id>`, `repo:<path-relativo>`, `url:<url-completa>`.

---

## Convención de enlaces — Wikilinks Foam

**Regla crítica**: todos los enlaces internos del wiki usan `[[slug]]`, compatible con Foam/Markdown Notes en VSCode.

- **Sintaxis**: `[[slug]]` — solo el nombre del archivo sin `.md`, sin path, sin alias. Ej: `[[2026-04-05-nombre-del-nodo]]`.
- **Resolución**: Foam resuelve el slug al archivo por nombre. Los slugs son únicos por construcción (incluyen fecha).
- **Dónde se usan**:
  - `index.md`: cada entry del catálogo
  - Nodos: sección `## Cross-refs`
  - Nodos: sección `## Fuentes` cuando apunta a otro nodo del wiki o a un anchor interno (`[[sources#id]]`)
- **Dónde NO se usan**:
  - URLs externas: usar markdown link `[texto](url)`
  - Archivos fuera del vault `cerebro/`: backticks literales
  - "Origen histórico" en Fuentes: texto plano, **no enlazar**

---

## Cuerpo obligatorio de cada nodo session

Secciones en este orden exacto:

```
# <título del nodo>

## Contexto

## Decisiones

## Output

## Pendiente

## Cross-refs
- [[slug]] — razón en una línea

## Fuentes
- [[sources#id]]
- Origen histórico (no modificar): `ruta/original.md`
```

Reglas del cuerpo:
- `Cross-refs`: **sólo wikilinks** a otros nodos del wiki. Cada bullet con razón en una línea. Sin razón → candidato orphan-link en lint.
- `Fuentes`: referencias externas. Para sources externos: `[[sources#id]]`. Para URLs web: `[texto](url)`. Para archivos del repo fuera del vault: texto plano o backticks.

---

## Reglas de ingest

Cuando se invoca `/cerebro ingest`:

1. Leer `cerebro/CLAUDE.md` y `cerebro/index.md`.
2. Revisar la conversación actual. Identificar:
   - Área(s) tocadas.
   - Verbo de acción principal (definimos, migramos, decidimos, implementamos, debuggeamos).
   - Output concreto: archivos creados/modificados, URLs.
   - Decisiones con rationale.
   - Pendientes explícitos.
3. Generar el slug: `YYYY-MM-DD-<kebab-case>`. Fecha = hoy. El slug describe el RESULTADO (no el proceso), máx. 6 palabras.
4. ¿Existe nodo del mismo día con tema muy similar?
   - **Sí** → UPDATE: leerlo y appendear a Decisiones/Output/Pendiente bajo `### Actualización [HH:MM]`. No reescribir lo anterior.
   - **No** → CREATE.
5. CREATE: generar frontmatter completo. `related` busca en `index.md` nodos con tags solapados, misma área o proximidad cronológica. Máx. 5.
6. Escribir cuerpo con las 6 secciones obligatorias. Cross-refs con `[[slug]]` y razón en una línea.
7. **Bidireccionalidad obligatoria**: para cada nodo en `related`, abrirlo y agregar bullet recíproco en su `## Cross-refs` con `[[este-nodo]] — razón`. Sin excepciones.
8. Actualizar `cerebro/index.md`: insertar bullet `[[slug]] — one-liner` al tope de la sección del área. Si el área no existe, crearla en orden alfabético.
9. Append a `cerebro/log.md`: `## [YYYY-MM-DD HH:MM] ingest | <slug>` con metadata de cross-refs.
10. Reportar al usuario: path del nodo, cross-refs agregadas, decisiones ambiguas.



---

## Reglas de query

Cuando se invoca `/cerebro query <pregunta>`:

1. Leer `cerebro/CLAUDE.md` y `cerebro/index.md` completos.
2. **Si la pregunta es sobre el negocio** — qué hace, a quién le vende, cómo trabaja, cómo escribe —
   la respuesta está en `contexto/`. Leer esos archivos primero.
3. **Si la pregunta es sobre un cliente, un prospecto o algo que ya se habló**, buscar siempre en
   `sessions/` **y** en `llamadas/` (índice + Grep por el nombre de la empresa o persona y sus
   variantes). Las dos carpetas son memoria: las sesiones guardan lo que se hizo y decidió, las
   llamadas lo que dijeron las personas.
4. De los one-liners del índice y del Grep, seleccionar 1-5 nodos candidatos entre sesiones y
   llamadas. Leer esos nodos completos. Si el dato sale de una llamada, citar quién habló y cuándo;
   si está marcada `simulada: true`, avisarlo.
5. Respondé exclusivamente desde los nodos del wiki. Si el contenido no está en el wiki, decilo explícitamente.
6. Sintetizar respuesta en 2-5 párrafos con citations usando wikilinks: `[[slug-del-nodo]]`. **NO usar markdown links** para nodos del wiki.
7. Si detectás un gap (cross-ref obvio faltante, concepto en 3+ nodos sin nodo propio), NO arreglarlo — reportarlo al final como "Sugerencia para `/cerebro lint`".
8. Si no hay info suficiente, decirlo explícitamente. **No inventar ni extrapolar** más allá de lo que dicen los nodos.

---

## Reglas de lint

Cuando se invoca `/cerebro lint`:

1. Leer `cerebro/CLAUDE.md`, `cerebro/index.md` y **todos** los archivos en
   `cerebro/contexto/`, `cerebro/sessions/` y `cerebro/llamadas/`.
2. Revisar estas categorías:
   - **Orphan nodes**: nodos sin inbound wikilinks desde otros nodos ni desde `index.md`.
     **Los archivos de `contexto/` no son huérfanos aunque nadie los enlace** — son la base que se
     lee siempre, no nodos que dependan de estar conectados.
   - **Broken wikilinks**: `[[slug]]` que no resuelve a ningún archivo en `contexto/` ni en `sessions/`.
   - **Contexto incompleto**: áreas del negocio sin archivo en `contexto/`, o archivos con
     `**Abierto:**` sin resolver. Reportar como recordatorio, no como error.
   - **Stale claims**: fechas de pendientes que ya pasaron.
   - **Missing cross-refs**: pares con alto solape de tags o misma entidad sin wikilink entre sí.
   - **Conceptos emergentes**: términos que aparecen en 3+ nodos sin nodo propio. Reportar como candidatos, **no crear**.
   - **Contradicciones**: decisiones opuestas sin `superseded_by`.
   - **Frontmatter inválido**: campos faltantes o valores fuera de enum.
   - **Índice desincronizado**: nodo en `contexto/` o `sessions/` sin entry en `index.md`, o viceversa.
   - **Markdown links mal usados**: enlaces a nodos del wiki que usan `[text](path)` en lugar de `[[slug]]`.
3. Devolver reporte markdown estructurado por categoría con sugerencia accionable por ítem.
4. **NO modificar archivos.** Solo append de una entrada corta a `log.md` con conteos.
5. Append a `cerebro/log.md`: `## [fecha] lint | report` con conteo por categoría.



---

## Idioma

- Contenido de nodos: **español**.
- Tags y slugs: **español sin tildes, kebab-case**.
- Frontmatter keys: **inglés** (convención técnica).
