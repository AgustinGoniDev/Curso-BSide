---
name: destilar-llamada
description: "Destila la transcripción de una llamada o reunión (Fathom, Meet, Zoom, notas pegadas o un archivo) en cuatro bloques útiles: síntomas del prospecto en sus palabras, objeciones, lo que se decidió y lo que no sirve. Guarda el resultado en cerebro/llamadas/ (la carpeta de llamadas del cerebro de Lumen Lab). Usá esta skill cuando el usuario diga 'destilá esta llamada', 'procesá la transcripción', 'sacá lo útil de esta reunión', 'analizá la llamada con [empresa]', 'guardá esta llamada en el cerebro', 'qué dijo el prospecto', o pegue una transcripción larga (con marcas de tiempo y nombres de hablantes) aunque no diga 'destilar'. No la uses para escribir emails (eso es /investigar-prospecto, /generar-email-1 o /responder-objecion) ni para propuestas (/generar-propuesta)."
---

# Skill: Destilar llamada — Lumen Lab

Convierte una transcripción larga en una ficha corta con lo único que vale: lo que la persona
cuenta de su problema, lo que frena, lo que se acordó y qué descartar. La guarda en el cerebro
para que `/investigar-prospecto`, `/generar-email-1`, `/responder-objecion` y `/generar-propuesta`
la puedan usar después.

> Una transcripción de 55 minutos tiene 5 minutos de oro. El oro son las palabras textuales del
> cliente sobre su dolor. Todo lo demás es contexto o ruido.

## Entrada

El usuario pasa la llamada de cualquiera de estas formas: texto pegado, ruta a un archivo, link de
Fathom con el texto, o notas propias. Si falta algo, preguntar solo lo imprescindible:

- **Quién es el prospecto o contacto** y su empresa. Si no queda claro quién habla, inferirlo por
  los nombres de hablante y confirmarlo en una línea.
- **Rol de la llamada**: `prospecto` (descubrimiento o venta), `cliente` (seguimiento) u `otro`
  (par, referente, mentor). Si no se aclara, inferirlo del contenido y dejarlo escrito.
- **Fecha**: sacarla del título o del texto. Si no hay, usar la fecha de hoy y avisarlo.

Si el usuario pide simular otro contexto (por ejemplo "simulemos que es de Lumen Lab"), seguirlo,
pero dejarlo escrito en la ficha para que no se confunda con una llamada real.

## Step 1 — Leer el contexto

Antes de destilar, leer `cerebro/index.md` y `cerebro/contexto/cliente.md` (ICP, dolor típico y red
flags). Sirve para medir el encaje del prospecto, no para completar lo que la persona no dijo.

## Step 2 — Destilar en cuatro bloques

### 1. Síntomas
Lo que la persona cuenta de su problema, **en sus palabras**. Es lo más valioso.
- Citas **textuales** entre comillas, con la marca de tiempo si existe. No parafrasear ni
  "mejorar" la redacción. Corregir solo errores obvios de transcripción automática, sin cambiar
  el sentido.
- Agrupar por tema: adquisición, posicionamiento y contenido, carga del dueño, procesos,
  herramientas.
- Separar los síntomas **del propio entrevistado** de los que **cuenta de terceros** (clientes,
  colegas, amigos). Los de terceros valen, pero son de segunda mano.
- Atribuir cada cita al hablante que la dijo. Nunca poner en boca del prospecto algo que dijo el
  equipo de Lumen Lab.

### 2. Objeciones
Las dudas y los frenos que mostró, explícitos o implícitos.
- Una línea por objeción, con la cita que la respalda.
- Clasificar contra el patrón clásico B2B si encaja (precio, timing, "lo hacemos adentro", "ya
  tenemos a alguien", "no confío en agencias", desconfianza en resultados). Si no encaja,
  describirla con palabras propias.
- Incluir los frenos que aparecen como experiencias pasadas (por ejemplo, "probamos LinkedIn y
  lo dejamos").

### 3. Lo que se decidió
Acuerdos y próximos pasos.
- **Acuerdos**: lo que las partes dijeron que harían.
- **Próximos pasos**: cada uno con responsable y fecha. Sin fecha, escribir "sin fecha".
- Sumar los action items que traiga la herramienta de grabación (Fathom, etc.).
- Distinguir una **decisión** de una **idea** o de una opinión. Lo que quedó como idea va marcado
  como tal.

### 4. Lo que no sirve
Rompehielos, charla de relleno, anécdotas, quejas ajenas al negocio y **opiniones propias** de
quien habla (hipótesis sin datos, sesgos declarados).
- Una línea que diga qué se descartó y por qué. No expandirlo.
- Una opinión del prospecto sobre su mercado no es un síntoma de su problema.

## Step 3 — Encaje y siguiente paso

Cerrar la ficha con un bloque corto (máx. 5 líneas):
- **Encaje con el ICP** (alto, medio o bajo) y por qué, contra `cerebro/contexto/cliente.md`. Si
  hay red flags, nombrarlos.
- **Rubro** del prospecto, según las categorías del ICP.
- **Siguiente skill sugerida**: `/generar-email-1`, `/responder-objecion`, `/generar-propuesta` u
  ofrecer la auditoría de posicionamiento. Solo sugerir, no ejecutar.

## Step 4 — Guardar en el cerebro

Guardar sin pedir permiso solo la ficha, en la carpeta de llamadas del cerebro. Las llamadas
**no se registran en `sources.md`**: son contenido del cerebro, no fuentes externas. El resto
(nodo de sesión, cambios al contexto) se recomienda y espera el sí del usuario.

1. **Archivo**: `cerebro/llamadas/YYYY-MM-DD-<slug>.md` (crear la carpeta si no existe)
   - `slug`: kebab-case, sin tildes, ≤5 palabras, con la empresa o el contacto
     (ej. `2026-08-05-empresa-contacto`).
   - Si ya existe un archivo con ese nombre, no sobrescribir: agregar `-2`.
2. **Formato del archivo**:

```markdown
---
type: llamada
date: YYYY-MM-DD
empresa: <nombre>
contacto: <nombre y rol>
rol-de-la-llamada: prospecto | cliente | otro
rubro: <del ICP o "fuera de ICP">
encaje: alto | medio | bajo
duracion: <minutos, si se sabe>
fuente: <link de Fathom o ruta del original, o "pegado en chat">
simulada: false
tags: [<kebab-case, sin tildes>]
---

# Llamada con <empresa> — <fecha>

> <una línea: qué fue esta llamada y qué se llevó el negocio>

## Síntomas
## Objeciones
## Lo que se decidió
## Lo que no sirve
## Encaje y siguiente paso
```

   Si la llamada se simuló como de Lumen Lab, poner `simulada: true` y una nota arriba del título.
3. **Actualizar `cerebro/index.md`**: agregar `[[slug]] — one-liner` al tope de la sección
   "Llamadas" (crearla si no existe, entre Sesiones y Conceptos) y actualizar el total de nodos.
4. **Append a `cerebro/log.md`** (al final, formato del wiki):
   ```
   ## [YYYY-MM-DD HH:MM] ingest | <slug>
   - Área: llamadas
   - Fuente: cerebro/llamadas/<archivo>.md
   ```
5. **No crear nodos** en `cerebro/sessions/` ni `cerebro/contexto/`. Si la llamada cambia algo del
   negocio (ICP, oferta, voz), proponerlo al usuario en una línea. Si quiere guardar la sesión,
   `/cerebro` hace el ingest.

## Step 5 — Responder al usuario

Mostrar la ficha completa **en el chat** (para que la lea sin abrir el archivo), más:
- La ruta del archivo guardado.
- Qué se actualizó en `index.md` y `log.md`.
- Cualquier dato dudoso: quién habló, fecha inferida, un pasaje ininteligible.

## Reglas duras

- **No inventar.** Si la llamada no dice algo, no aparece en la ficha. Mejor "no se mencionó" que
  una suposición. Esto incluye presupuesto, decisores y plazos.
- **Citas textuales.** Lo entre comillas es lo que se dijo. La interpretación va aparte, sin comillas.
- **No mezclar con `pruebas.md`.** Lo que un prospecto dice de su problema no es un testimonio
  de Lumen Lab. Solo se cita como testimonio lo que diga un cliente sobre el trabajo de Lumen Lab.
- **Datos sensibles.** Si la transcripción trae datos personales o cifras financieras
  confidenciales del prospecto, incluir solo lo que sirve al negocio y no copiar el resto.
- **Idioma:** español, con las citas en su idioma original.
- **Largo:** la ficha debe leerse en 2 minutos. Si pasa de ~1 página, recortar por relevancia.
- **Transcripción mala:** si hay trozos ininteligibles por el audio, marcarlos como
  `[inaudible]` y no adivinar.
