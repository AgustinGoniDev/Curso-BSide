---
name: investigar-prospecto
description: "Investiga un prospecto específico: hace research exhaustivo en internet (web, LinkedIn, prensa, portales de empleo, Meta Ad Library) y genera el Email 1 personalizado siguiendo el framework 'Consultor, no Vendedor' de Lumen Lab. Triggereá cuando el usuario diga 'investigá prospecto', 'investigá a [empresa]', 'armá el email para [empresa/contacto]', o cualquier variante que pida investigar y contactar un prospecto específico."
---

# Skill: Investigar Prospecto — Lumen Lab

Investiga un prospecto y genera el Email 1 personalizado siguiendo el framework de Lumen Lab.

## Parámetros

El usuario provee (en cualquier formato):
- **empresa**: nombre de la empresa a investigar
- **contacto**: nombre del contacto principal
- **cargo**: cargo del contacto
- Cualquier dato adicional que tenga (rubro, tamaño, ubicación, señal inicial)

---

## Step 1 — Research exhaustivo

Para el prospecto recibido, hacer todas las búsquedas en orden. Usar `WebSearch` para buscar y `WebFetch` para leer páginas. El objetivo es acumular el máximo contexto — cuanto más específico el email, mejor la tasa de respuesta.

**Regla de oro:** buscar hasta encontrar un dato concreto que justifique el contacto. Si no hay nada, usar Variante C.

### Búsqueda 1 — Web de la empresa (SIEMPRE)
Buscar la web y hacer `WebFetch` de homepage, "Servicios", "Nosotros".

Anotar:
- ¿Qué venden y cómo lo entregan?
- ¿Cuántos clientes o proyectos manejan?
- ¿Qué canales usan para vender?
- Tono: ¿empresa familiar, mediana, corporativa?

### Búsqueda 2 — Contacto en medios
Queries:
- `"{Contacto}" site:infobae.com OR site:ambito.com OR site:iprofesional.com OR site:cronista.com`
- `"{Contacto}" emprendedor entrevista`
- `"{Empresa}" expansión crecimiento 2025 2026`

Hacer `WebFetch` de las notas más relevantes. Las frases textuales del contacto son el gancho más poderoso.

### Búsqueda 3 — LinkedIn empresa
Query: `"{Empresa}" site:linkedin.com/company`

Anotar: empleados, posiciones abiertas, actividad reciente.

### Búsqueda 4 — LinkedIn contacto
Query: `"{Contacto}" "{Cargo}" "{Empresa}" site:linkedin.com`

Si es accesible: experiencia previa, actividad, tiempo en el cargo.

### Búsqueda 5 — Señales de contratación
Queries:
- `"{Empresa}" site:bumeran.com OR site:zonajobs.com OR site:computrabajo.com OR site:linkedin.com/jobs`
- `"{Empresa}" empleo trabajo contratar 2025`

Contratar coordinadores o roles operativos = señal de proceso manual escalando.

### Búsqueda 6 — Publicidad activa (si tiene presencia digital)
Visitar: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=AR&q={Empresa}`

Ads activos + sin sistema = fuga de ROI directa.

---

## Step 2 — Clasificar señal y elegir variante

| Prioridad | Señal | Variante |
|---|---|---|
| 1 | Hiring activo — roles operativos | A |
| 2 | CEO en medios hablando de crecimiento | A |
| 3 | Expansión — nueva sede, nuevo mercado | A |
| 4 | Ads activos + sin sistema de atención evidente | B |
| 5 | Sin señal clara | C |

---

## Step 3 — Escribir el Email 1

**Reglas base — NO negociables:**
- Máximo 6 oraciones en total
- Sin links
- Primera persona singular: "Soy Agustín, founder de Lumen Lab" — nunca "ayudamos"
- Firma: solo "Agustín" — sin cargo, sin empresa
- Sin palabras de venta: "oportunidad", "propuesta", "transformación"
- **No diagnosticar la empresa del prospecto.** Usar marcadores de hipótesis: "suele", "en general", "no sé si les pasa".
- **El CTA no nombra la solución.** La pregunta es sobre el proceso actual.

### Los 4 bloques

**Bloque 1 — Asunto: 3 opciones distintas**
- Minúsculas, sin exclamación, 30–50 caracteres, tono de conocido
- Específicas al prospecto — si sirven para cualquier otro, son genéricas

**Bloque 2 — Hook (2 oraciones máx.)**
- Oración 1: la señal concreta que encontraste con la fuente ("vi en LinkedIn que…", "vi la nota en Ámbito donde…")
- Oración 2: patrón observado en empresas similares — NO diagnóstico

Ejemplos CORRECTOS:
- "Vi que publicaron dos posiciones de analista contable esta semana. En las firmas de outsourcing que crecen rápido, el cuello de botella suele aparecer antes en el proceso de revisión que en la capacidad de conseguir clientes."
- "Vi que anunciaron un nuevo cliente enterprise en LinkedIn. Cuando una consultora suma clientes de ese tamaño, la carga de onboarding suele multiplicarse — no sé si ya tienen un proceso armado para eso."

Ejemplos INCORRECTOS:
- "Manejan 50 clientes con 15 personas." ← recita datos internos
- "A ese volumen, la gestión manual no escala." ← diagnostica

**Bloque 3 — Posicionamiento + Caso (3 oraciones máx.)**
- "Soy Agustín, founder de Lumen Lab."
- "Trabajamos con [estudios contables / consultoras / agencias] en LATAM para [posicionamiento B2B + generación de demanda sistemática]."
- Caso conectado con la señal del Hook:
  - Crecimiento operativo → "Con Concreto Studio, un estudio de arquitectura similar, pasaron de 0 a 3 inbounds calificados por mes en 60 días con el sistema que les armamos."
  - Sin sistema de prospección → "Con ByData Consultores, reemplazamos el pipeline de referidos por outbound sistematizado — 4 reuniones calificadas en el primer mes."

**Bloque 4 — CTA**
- Pregunta abierta sobre el proceso actual, respondible desde el celular
- No nombra marketing, contenido, LinkedIn, outbound

Ejemplos CORRECTOS:
- "¿Hoy la prospección nueva sale principalmente de referidos o tienen algo más sistematizado?"
- "¿El proceso de onboarding de un cliente enterprise lo gestiona alguien del equipo o todavía es manual?"
- "¿Cuánto tiempo le dedica el equipo a generar demanda vs. atender a los clientes actuales?"

---

## Step 4 — Output al usuario

Presentar la investigación completa:

```
# Investigación — {Empresa}

## Resumen de la empresa
{3-5 oraciones: qué venden, cómo, canales, tamaño, geografía}

## Señal identificada
**Tipo:** {Hiring / CEO en medios / Expansión / Ads+sin sistema / Sin señal}
**Detalle:** {Dato concreto con fuente}

## Calificación ICP Lumen Lab
✅ Pasa / ⚠️ Dudoso / ❌ No pasa
{1-2 oraciones: fit con el ICP de Lumen Lab (PyME B2B servicios profesionales)}

## Email 1

**Asuntos (elegir uno):**
1. `opción A`
2. `opción B`
3. `opción C`

{Cuerpo del email}

Agustín

---
**Variante:** {A / B / C} | **Señal usada:** {descripción breve}
```

---

## Notas importantes

- **No inventar datos**: sin información concreta → Variante C
- **WebFetch la web siempre**: fuente más confiable de contexto
- **LinkedIn sin login**: solo snippets de Google, no WebFetch de perfiles privados
- **Caso de éxito relevante según rubro del prospecto:**
  - Contables/finanzas → mencionar ByData Consultores (no revelar detalles internos)
  - Consultoras/RRHH → mencionar Concreto Studio como referencia
  - Tech/agencias → mencionar el caso de software factory
