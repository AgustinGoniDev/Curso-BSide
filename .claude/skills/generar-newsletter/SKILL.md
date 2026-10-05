---
name: generar-newsletter
description: "Escribe el newsletter semanal en texto plano (150-250 palabras, una sola idea, un solo CTA) a partir de lo que hay en el cerebro: llamadas destiladas, sesiones y contexto del ICP. Aplica el formato y el tono de Agustín (voseo rioplatense, gancho directo, firma '— Agustín') y lo guarda en newsletter/. Usá esta skill cuando el usuario diga 'armá el newsletter', 'escribí el newsletter de esta semana', 'hacé un newsletter sobre [tema / dolor / llamada]', 'transformá esta llamada en un newsletter', 'newsletter sobre los dolores de [tipo de cliente]', o cualquier variante que pida un email semanal de contenido a la lista, aunque no diga 'newsletter'. No la uses para emails de prospección (eso es /investigar-prospecto o /generar-email-1), para responder objeciones (/responder-objecion) ni para posts de LinkedIn."
---

# Skill: Generar newsletter — semanal, texto plano

Escribe un newsletter corto, íntimo y de una sola idea, usando como materia prima lo que ya está
en el cerebro. No es un folleto: es un mail de un colega que sabe del tema.

> Una idea, un gancho directo, un CTA. Si hace falta una segunda idea, es otro newsletter.

## Parámetros

El usuario puede pasar (en cualquier formato):
- **tema o dolor**: de qué va (ej. "los dolores de founders de agencias").
- **fuente**: una llamada, una sesión o un cliente (ej. "la última llamada con un founder").
- **link del CTA**: casi siempre el último video de YouTube.

Si falta el tema, proponer 2 o 3 ideas sacadas del cerebro (una línea cada una, con la fuente) y
dejar que el usuario elija. Si falta el link, **no inventarlo**: usar el marcador
`[LINK AL ÚLTIMO VIDEO]` y avisarlo al final.

## Step 1 — Juntar la materia prima

Antes de escribir, leer `cerebro/index.md` y `cerebro/contexto/cliente.md` y `voz.md`. Después
buscar en `cerebro/llamadas/` **y** en `cerebro/sessions/` (índice + Grep por el tema, la empresa o
la persona), igual que el modo query de `/cerebro`.

De ahí sacar:
- **Citas textuales** de la gente (síntomas y objeciones). Son lo mejor del newsletter.
- **Patrones** que se repiten en más de una llamada o cliente.
- Datos concretos y verificados. Si un número no está en el cerebro, no se usa ni se estima.

Si la fuente es una llamada marcada `simulada: true`, usarla igual si el usuario lo pide, pero
avisarlo en el cierre.

## Step 2 — Elegir UNA idea

De todo lo que hay, elegir la que más duele y mejor se cuenta en 100-200 palabras. Las demás se
descartan o se proponen como ideas para próximos newsletters al final de la respuesta, en una
línea cada una. Nunca se mezclan dos ideas en el mismo mail.

## Step 3 — Escribir con este formato

```
ASUNTO: [Una idea concreta — no clickbait, no vago]

[Gancho — 2-3 líneas. Observación directa, situación reconocible o dato concreto.]

[Desarrollo — una sola idea. 100-200 palabras. Párrafos de 1-3 líneas con espacio.]

[CTA — una línea. Casi siempre: link al video de YouTube más reciente.]

— Agustín
```

### Reglas de formato
- **Texto plano.** Sin imágenes en el cuerpo, sin bullets decorativos, sin headers de sección, sin
  firma corporativa.
- **Longitud total: 150-250 palabras, nunca más.**
- **CTA:** casi siempre el link al último video de YouTube. Excepcionalmente, a un recurso concreto
  de la carpeta. **Nunca dos CTAs.**
- **Firma:** solo `— Agustín`. Sin logo, sin cargo, sin links de redes.

### Reglas de tono
- Primera persona, **voseo rioplatense**. Íntimo, como a un colega que sabe del tema.
- **El gancho arranca directo.** Sin "Hola [Nombre]", sin "esta semana quiero hablarte de…".
- Sin buzzwords ("transformación digital", "potenciar", "ecosistema", "sinergia", "soluciones
  integrales").
- Sin conclusiones genéricas. Si cierra con una pregunta, que apunte al proceso del lector, no a
  una moraleja.
- Se plantea como **hipótesis**, no como diagnóstico cerrado ("mi hipótesis es…", no "tu problema es…").

### Reglas del asunto
- 4-8 palabras. Lo que promete, lo entrega.
- Sin mayúsculas innecesarias ni puntos suspensivos clickbait.
- Sí: "El error que veo repetirse en PyMEs con IA", "80 horas por mes. Así se liberaron."
- No: "Esto va a cambiar tu empresa…", "¿Estás cometiendo este error?"

## Step 4 — Reglas del cerebro que siguen valiendo

- **Anonimizar.** Las personas de llamadas y clientes aparecen como "el founder de una agencia",
  "una consultora de RRHH", etc. Nunca nombre ni empresa, salvo que el usuario diga que tiene el
  visto bueno de esa persona.
- **No inventar.** Todo lo que se cuenta tiene que estar en el cerebro. Las citas van textuales.
- **Sin promesas** de leads, facturación o posiciones, ni resultados que un cliente no haya dicho
  en `pruebas.md`.
- **No mezclar con `pruebas.md`.** Lo que un prospecto cuenta de su problema no es un testimonio.

## Step 5 — Checklist pre-envío

Antes de guardar, repasar cada punto y corregir lo que falle:
- ¿Una sola idea?
- ¿El asunto promete lo que entrega (4-8 palabras, sin clickbait)?
- ¿Un solo CTA?
- ¿El gancho arranca sin saludar?
- ¿Menos de 250 palabras (contadas sin el asunto ni la firma)?
- ¿Sin buzzwords ni conclusiones genéricas?
- ¿Voseo rioplatense en todo el texto?
- ¿Anonimizado y sin datos inventados?

## Step 6 — Guardar y entregar

1. Guardar en `newsletter/YYYY-MM-DD-<slug>.md` (crear la carpeta si no existe). `slug` en
   kebab-case, sin tildes, ≤5 palabras, describe la idea. Si el archivo ya existe, agregar `-2`:
   no sobrescribir.
2. El archivo contiene **solo el email**, listo para copiar: sin frontmatter, sin notas.
3. Mostrar el email completo en el chat y debajo, en pocas líneas:
   - Ruta del archivo y cantidad de palabras.
   - El checklist, con lo que cumple y lo que no.
   - Lo que falta (link del video, visto bueno para citar, llamada simulada).
   - Ideas descartadas para próximos newsletters (una línea cada una).
4. **No enviar nada** ni publicarlo. Enviar es decisión del usuario.
5. No tocar el cerebro. Si el usuario quiere dejar registro, recomendar `/cerebro` en una línea al
   final.
