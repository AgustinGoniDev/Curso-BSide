---
name: reporte-semanal-contenido
description: "Arma el reporte semanal de contenido de Lumen Lab: cruza la base Contenido con el Pipeline comercial en Notion, usa el ICP y la oferta del cerebro para medir si el contenido está atrayendo al cliente ideal, y lo entrega como HTML con el branding de la agencia (más un registro en la base Reportes semanales). Usá esta skill siempre que el usuario pida 'el reporte semanal', 'el reporte de contenido', 'cómo rindió el contenido esta semana', 'el informe del lunes', '¿el contenido está trayendo clientes ideales?', 'qué posts trajeron leads', 'cruzá contenido con pipeline' o cualquier variante que pida evaluar posts de LinkedIn contra leads, ICP o pipeline, aunque no diga la palabra 'reporte'."
---

# Skill: Reporte semanal de contenido — Lumen Lab

Responde una sola pregunta: **¿el contenido de esta semana está atrayendo al cliente ideal de Lumen Lab?**

La respuesta sale de cruzar tres capas:

1. **Contenido** (Notion): qué se publicó y cuánto alcance tuvo.
2. **Pipeline** (Notion): qué leads entraron, de dónde, cuánto valen y cómo avanzan.
3. **Contexto** (`cerebro/contexto/`): quién es el ICP y qué vendemos. Es el criterio contra el que se mide todo.

## Por qué el reporte abre con pipeline y no con impresiones

En Lumen Lab el alcance por sí solo engaña: los posts genéricos (hashtags, herramientas de IA, tendencias) suelen juntar 3–4 veces más impresiones que los posts que hablan del dolor real del ICP, y aun así no traen ni un mensaje. Lo que importa es si entran leads que son ICP y si avanzan. `cerebro/contexto/voz.md` ya lo dice: alcance y engagement no son un fin, lo son la demanda, el pipeline y las reuniones. Por eso el reporte pone primero los leads y el pipeline, y deja impresiones y reacciones como contexto.

## Parámetros

- **semana** (opcional): por defecto, la última semana cerrada lunes a domingo respecto de la fecha de hoy. Acepta "semana del 18/08", un rango de fechas o "esta semana" (en curso, se marca como parcial).

No hace falta pedir nada más: los datos salen de Notion y del cerebro.

---

## Step 1 — Fijar la semana

Calculá `inicio` (lunes) y `fin` (domingo) con la fecha de hoy que figura en el contexto de la sesión. La ventana de análisis es de **5 semanas**: la semana pedida más las 4 anteriores, porque con ~2 posts por semana una sola semana rara vez alcanza para concluir algo.

## Step 2 — Leer la capa de contexto

Leé, dentro de `cerebro/` del proyecto (ruta relativa; ignorá la ruta absoluta que pueda figurar en `CLAUDE.md`, puede estar desactualizada):

- `cerebro/contexto/cliente.md` — ICP, dolor típico, red flags, preguntas de calificación.
- `cerebro/contexto/que-hacemos.md` — oferta, tickets, diferencial.
- `cerebro/contexto/voz.md` — qué no se dice (jerga de marketing como fin en sí misma).

No copies el ICP a mano en el reporte: leelo en cada corrida para que, si el contexto cambia, el criterio cambie con él. Si un archivo tiene marcas `**Abierto:**` que afectan el criterio (hoy las red flags del cliente son "supuesto a validar"), mencionalo en la sección de calidad de datos.

## Step 3 — Traer los datos de Notion (solo lectura)

Usá `notion-query-data-sources` (cargá su schema con ToolSearch si está diferido). En `references/notion-schema.md` están los IDs, las columnas y las queries SQL listas. Resumen:

- **Contenido** (`collection://c74ccafa-9008-47e7-a413-aa7c73fc5ab2`): posts de la ventana de 5 semanas.
- **Pipeline** (`collection://86845970-7077-4fde-8e13-0eac9f61300b`): todas las filas (son pocas).
- Uní ambas por URL de página: `Contenido.Leads` ↔ `Pipeline."Post que lo trajo"`. Seleccioná siempre `url` en las dos queries.

Esta skill **no modifica** Contenido ni Pipeline.

## Step 4 — Clasificar (tu criterio, con la rúbrica)

Leé `references/icp-scoring.md` y clasificá:

- **Cada post** → `dolor-icp` | `educativo-generico` | `marca-personal`, según el gancho frente al dolor del ICP y la oferta.
- **Cada lead atribuido a contenido** → fit `fuerte` | `parcial` | `fuera`, según `Rubro`, `Cargo` y ticket frente al ICP; anotá las red flags que apliquen.

Escribí una línea de fundamento por cada clasificación. El reporte las muestra: quien lea el reporte tiene que poder discrepar de un criterio concreto, no de una caja negra.

## Step 5 — Calcular las métricas

Armá `datos.json` (formato en `references/metricas.md`) en una carpeta temporal y corré:

```bash
python .claude/skills/reporte-semanal-contenido/scripts/calcular_metricas.py datos.json
```

El script agrega la clave `metricas` al mismo archivo: comparación semana vs semana anterior vs promedio de 4 semanas, leads ICP por 1.000 impresiones por tipo de post y por formato, embudo de los leads atribuidos, mezcla del pipeline por origen y un semáforo sugerido. Los números salen del script, no de tu cabeza.

## Step 6 — Escribir la narrativa

Agregá la clave `narrativa` a `datos.json` con (campos exactos en `references/metricas.md`):

- `veredicto`: una frase + semáforo (`atrae-icp` | `mixto` | `audiencia-equivocada` | `sin-datos`). Partí del semáforo sugerido por el script y cambialo solo con motivo escrito.
- `evidencias`: exactamente 3, cada una con su n ("2 de 3 leads", no "67%" a secas).
- `acciones`: qué repetir, qué dejar de hacer y 2–3 ángulos de post para la semana siguiente, derivados de los dolores del ICP en `cliente.md` (no de tendencias genéricas).
- `calidad_datos`: cada brecha o inconsistencia detectada.

### Reglas de honestidad

- **Mostrá siempre el n.** Con 2 posts por semana un porcentaje sin base miente.
- Con menos de 3 leads atribuidos en la ventana de 5 semanas, el veredicto es `sin-datos`, salvo que las 5 semanas juntas den una señal clara y lo expliques.
- Notion no trae quién ve cada post en LinkedIn. "Atrae al ICP" se mide por **los leads que efectivamente entran**, no por la audiencia. Decilo en el reporte.
- Una semana sin posts, o sin leads, igual se reporta, con esa conclusión. No rellenes.
- Notion es la fuente de verdad. Si el snapshot de `CLAUDE.md` (MRR, pipeline, fechas) no coincide, reportalo como hallazgo en `calidad_datos`; no lo corrijas en silencio ni lo uses como dato.
- Detectá y reportá: mensajes o comentarios altos en un post sin lead atribuido (posible lead sin cargar), lead con `Post que lo trajo` que el post no refleja (o al revés), lead sin `Rubro`, valor faltante.
- Nunca inventes métricas que Notion no tiene (CTR, seguidores, demografía).

## Step 7 — Generar el HTML

```bash
python .claude/skills/reporte-semanal-contenido/scripts/renderizar_reporte.py datos.json reportes/reporte-semanal-AAAA-MM-DD.html
```

`AAAA-MM-DD` es el domingo de la semana reportada. El script usa `assets/template-reporte.html` (branding de Lumen Lab: fondo blanco, `#1a1a2e`, acento `#e94560`, Inter; imprimible y legible en celular). Creá la carpeta `reportes/` si no existe. Abrí el archivo para revisarlo antes de dar el reporte por bueno.

## Step 8 — Registrar en Notion

Creá **una** fila en la base **Reportes semanales** (`collection://19878eb9-f8ce-4686-ac2f-e3041e8cae04`) con `notion-create-pages`:

- `Nombre`: "Reporte semanal — 14–20 sep 2026" (el rango de la semana reportada).
- `Semana`: fecha inicio y fin (propiedad de fecha con rango).
- `Generado por`: `Manual`.
- Cuerpo de la página: el veredicto, las 3 evidencias y la ruta del HTML local.

Antes de crear, buscá si ya existe una fila para esa semana; si existe, no dupliques: avisá y actualizá solo si el usuario lo confirma.

## Step 9 — Cierre al usuario

Entregá, en este orden:

1. Ruta del HTML (link clickeable) y link a la fila de Notion.
2. El veredicto en una frase, con el semáforo.
3. Las brechas de datos que el equipo tiene que corregir en Notion.
4. Si detectaste que el snapshot de `CLAUDE.md` está desactualizado, sugerilo como pendiente aparte.

Si el reporte cambió una decisión de contenido o descubrió un patrón nuevo, sugerí `/cerebro ingest` al cerrar la sesión para registrarlo.

---

## Archivos de la skill

- `references/notion-schema.md` — IDs, columnas, queries y cómo unir las bases.
- `references/icp-scoring.md` — rúbrica de fit de leads y de tipo de post.
- `references/metricas.md` — formato de `datos.json`, definiciones, umbrales del veredicto.
- `scripts/calcular_metricas.py` — métricas determinísticas.
- `scripts/renderizar_reporte.py` — arma el HTML desde la plantilla.
- `assets/template-reporte.html` — plantilla con el branding.
