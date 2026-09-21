# Notion — esquema y queries

Carpeta raíz: **Lumen Lab** (https://www.notion.so/35b8e29552c38082a59dfba5586c8cd4). Contiene tres bases. Esta skill lee dos y escribe en una.

| Base | Data source | Uso en la skill |
|---|---|---|
| Contenido Lumen Lab | `collection://c74ccafa-9008-47e7-a413-aa7c73fc5ab2` | lee |
| Pipeline Lumen Lab | `collection://86845970-7077-4fde-8e13-0eac9f61300b` | lee |
| Reportes semanales | `collection://19878eb9-f8ce-4686-ac2f-e3041e8cae04` | escribe una fila |

Si una query falla por columna inexistente, hacé `notion-fetch` del data source y revisá el schema: alguien pudo renombrar una propiedad.

## Contenido Lumen Lab

| Propiedad | Tipo | Nota |
|---|---|---|
| `Gancho` | title | Primera línea del post. Es lo que se clasifica. |
| `Fecha` | date | Fecha de publicación. Columna SQL: `date:Fecha:start`. |
| `Formato` | select | `Texto` / `Carrusel` / `Video` |
| `Impresiones`, `Reacciones`, `Comentarios`, `Mensajes` | number | `Mensajes` = DMs recibidos por el post: señal de intención más fuerte que una reacción. |
| `Leads` | relation → Pipeline | Leads que trajo el post. |

## Pipeline Lumen Lab

| Propiedad | Tipo | Nota |
|---|---|---|
| `Empresa` | title | |
| `Rubro` | text | Texto libre. Base del fit ICP. |
| `Cargo` | text | Texto libre. Puede venir `—` en clientes activos. |
| `Estado` | select | `Research`, `Contactado`, `Reunión agendada`, `Propuesta enviada`, `En evaluación`, `Cliente activo`, `Frío` |
| `Origen` | select | `Referido`, `LinkedIn`, `Outbound`, `Evento` |
| `Valor USD/mes` | number | Puede ser null si aún no hay propuesta. |
| `Probabilidad cierre %` | number | 0–100. |
| `Post que lo trajo` | relation → Contenido | Atribución a contenido. Solo se carga a mano. |
| `Fecha de ingreso` | date | Columna SQL: `date:Fecha de ingreso:start`. |

Ojo: `Nexo Contadores` (Frío, outbound) no es `Nexo Legal` (cliente activo). No los confundas.

## Queries

**Contenido de la ventana** (reemplazá `:inicio5` por el lunes de hace 4 semanas y `:fin` por el domingo de la semana reportada):

```sql
SELECT url, Gancho, Formato,
       "date:Fecha:start" AS fecha,
       Impresiones, Reacciones, Comentarios, Mensajes, Leads
FROM "collection://c74ccafa-9008-47e7-a413-aa7c73fc5ab2"
WHERE "date:Fecha:start" >= :inicio5 AND "date:Fecha:start" <= :fin
ORDER BY "date:Fecha:start" DESC
```

**Pipeline completo:**

```sql
SELECT url, Empresa, Rubro, Cargo, Estado, Origen,
       "Valor USD/mes" AS valor, "Probabilidad cierre %" AS prob,
       "Post que lo trajo" AS post,
       "date:Fecha de ingreso:start" AS ingreso
FROM "collection://86845970-7077-4fde-8e13-0eac9f61300b"
```

Usá `notion-query-data-sources` en modo `sql` con el data source correspondiente. Si vuelven 100 filas o más, paginá.

## Cómo unir las bases

Las columnas `Leads` y `post` traen un array JSON de URLs de páginas. Normalizá cada URL a su **ID de 32 caracteres hexadecimales** (últimos 32 hex de la URL, sin guiones) y comparalo contra el `url` de la fila del otro lado, normalizado igual. Guardá ese ID como `id` de cada post y de cada fila del pipeline en `datos.json`.

Chequeos de consistencia (van a `calidad_datos` si fallan):

- Post con `Leads` cuyo lead no tiene ese post en `Post que lo trajo`, o al revés.
- Post con `Mensajes` > 0 y sin ningún lead.
- Fila de pipeline con `Origen = LinkedIn` y sin `Post que lo trajo` (lead de LinkedIn sin atribuir).
- Fila con `Post que lo trajo` y `Origen` distinto de `LinkedIn`.
- `Rubro` vacío, o `Valor USD/mes` vacío en estados `Propuesta enviada` / `En evaluación`.

## Escribir en Reportes semanales

Propiedades de la base: `Nombre` (title), `Semana` (date, admite rango), `Generado por` (select: `Manual` / `Tarea local` / `Rutina nube`).

Con `notion-create-pages`, `parent` = data source `19878eb9-f8ce-4686-ac2f-e3041e8cae04`. Las fechas se escriben con las claves expandidas `date:Semana:start` y `date:Semana:end`. Verificá el schema exacto de `notion-create-pages` con ToolSearch antes de llamarlo.

Antes de crear, consultá si ya existe una fila con `date:Semana:start` igual al lunes reportado:

```sql
SELECT url, Nombre FROM "collection://19878eb9-f8ce-4686-ac2f-e3041e8cae04"
WHERE "date:Semana:start" = :lunes
```
