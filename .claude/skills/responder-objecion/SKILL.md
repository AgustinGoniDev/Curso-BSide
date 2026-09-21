---
name: responder-objecion
description: "Escribe el Email 2 para un prospecto que respondió el Email 1 con una objeción o duda. Recupera el contexto del prospecto desde cerebro/, clasifica la objeción contra una librería de objeciones clásicas B2B (o la interpreta si no encaja) y genera una respuesta consultiva siguiendo el framework 'Consultor, no Vendedor' de Lumen Lab. Triggereá cuando el usuario diga 'respondé la objeción de [empresa]', 'armá el email 2 para [empresa]', 'el prospecto dijo [X], qué le contesto', '[empresa] me puso que [objeción]', o cualquier variante que pida responder a un prospecto que objetó."
---

# Skill: Responder Objeción — Lumen Lab (Email 2)

Responde a un prospecto que contestó el Email 1 con una objeción o duda. El objetivo NO es
empujar: es manejar la objeción como consultor y mantener el deal vivo.

> El prospecto que objeta está VIVO. El que no contesta, no. Una objeción bien respondida es
> donde se gana o se pierde el deal. No la trates como un obstáculo — tratala como información.

## Parámetros

El usuario provee (en cualquier formato):
- **empresa**: nombre de la empresa (para buscar contexto en `cerebro/`)
- **contacto**: nombre del contacto principal (si lo tiene)
- **objeción**: la respuesta textual del prospecto — este es el input central
- Cualquier dato adicional: canal, tiempo transcurrido desde el Email 1, tono de la respuesta

---

## Step 1 — Recuperar contexto del prospecto

Antes de escribir nada, buscar en `cerebro/sessions/` el nodo del prospecto. Leer su frontmatter
y secciones para recuperar:
- La **señal original** que disparó el Email 1
- El **rubro** (contable/finanzas, RRHH, agencia/tech, arquitectura/ingeniería/legal)
- El **dolor hipotetizado** y el ángulo que se usó

Si no hay nodo en `cerebro/`, trabajar solo con lo que provee el usuario. **No inventar contexto.**

---

## Step 2 — Clasificar la objeción

Comparar la respuesta del prospecto contra la librería. Elegir el patrón de respuesta — que es un
**ángulo consultivo, no un template rígido.**

| Objeción del prospecto | Patrón de respuesta consultiva |
|---|---|
| "No es el momento" / "más adelante" | Validar el timing sin discutir. Reframe: el costo de esperar es operativo (se acumula), no comercial. Dejar la puerta abierta sin presionar — proponer retomar cuando el momento sea mejor. |
| "Ya tenemos a alguien" / "ya trabajamos esto" | No competir de frente con el actual. Preguntar por una brecha específica que ese alguien probablemente no cubre (ej. prospección saliente sistematizada vs. solo contenido). |
| "Mandame info" / "mandame una propuesta" | NO mandar PDF genérico. Hacer 1 pregunta de diagnóstico concreta que justifique una propuesta a medida — la pregunta demuestra que la propuesta no va a ser un machete. |
| "No tenemos presupuesto" / "está caro" | Reencuadrar de costo a retorno con el caso por rubro. Ofrecer el punto de entrada más chico (auditoría de posicionamiento $800) como primer paso, sin sonar a descuento ni a rebaja. |
| "No veo el valor" / "no me cierra" / "no entiendo qué hacen" | No defender ni explicar de más. Devolver una pregunta sobre el proceso actual que exponga el costo oculto que hoy no están midiendo. |
| (no encaja en ninguna) | **Interpretación libre.** Aplicar el framework Consultor-no-Vendedor a la respuesta literal: validar, reencuadrar sin diagnosticar, cerrar con una pregunta sobre el proceso. |

---

## Step 3 — Escribir el Email 2

**Reglas base — NO negociables (idénticas al Email 1):**
- Máximo ~6 oraciones en total
- Sin links
- Primera persona singular: "Soy Agustín, founder de Lumen Lab" — nunca "ayudamos"
- Firma: solo "Agustín" — sin cargo, sin empresa
- Sin palabras de venta: "oportunidad", "propuesta", "transformación"
- **No diagnosticar la empresa del prospecto.** Usar marcadores de hipótesis: "suele", "en general", "no sé si les pasa".
- **El CTA no nombra la solución.** La pregunta es sobre el proceso actual.

### Los bloques del Email 2

**Bloque 1 — Asunto: 3 opciones distintas**
- Responder sobre el hilo existente: `Re: {asunto original}` es válido y a menudo lo mejor.
- Si se abre uno nuevo: minúsculas, sin exclamación, 30–50 caracteres, tono de conocido.

**Bloque 2 — Reconocimiento (1 oración)**
- Acusar recibo de la objeción sin ponerse a la defensiva. Validar que tiene sentido.
- Ejemplos CORRECTOS:
  - "Tiene todo el sentido — si ya tienen a alguien en contenido, sumar otra cosa no es prioridad."
  - "Claro, entiendo que ahora no sea el momento de meterse en algo nuevo."

**Bloque 3 — Reframe consultivo (1–2 oraciones)**
- Aplicar el ángulo del Step 2 + el caso por rubro conectado con la objeción.
- Usar marcadores de hipótesis, no diagnóstico.
- Ejemplos CORRECTOS:
  - "Lo que suele pasar igual es que el contenido trae a los que ya te conocen, pero la prospección a puerta fría queda sin sistema. Con ByData Consultores reemplazamos justo ese pedazo — 4 reuniones calificadas el primer mes."
  - "En general el problema no es el momento sino que sin un proceso armado, cada mes que pasa el pipeline sigue dependiendo de los referidos."

**Bloque 4 — CTA (1 pregunta)**
- Pregunta abierta sobre el proceso actual, respondible desde el celular. No nombra la solución.
- Ejemplos CORRECTOS:
  - "¿Hoy la parte de salir a buscar clientes nuevos la cubre alguien o queda más para cuando hay tiempo?"
  - "¿Te sirve que te haga una pregunta antes de armar algo, así no te mando un machete genérico?"

---

## Step 4 — Output al usuario

Presentar el resultado:

```
# Email 2 — {Empresa}

## Contexto recuperado
{2-3 oraciones: señal original del Email 1, rubro, dolor hipotetizado. O "sin nodo en cerebro/" si no había.}

## Objeción
**Tipo:** {No es el momento / Ya tienen a alguien / Mandame info / Sin presupuesto / No ve el valor / Interpretada}
**Textual:** "{lo que dijo el prospecto}"

## Email 2

**Asuntos (elegir uno):**
1. `opción A`
2. `opción B`
3. `opción C`

{Cuerpo del email}

Agustín

---
**Objeción usada:** {tipo} | **Ángulo aplicado:** {descripción breve} | **Caso citado:** {empresa del caso}
```

---

## Notas importantes

- **No inventar contexto** que no esté en `cerebro/` ni lo provea el usuario.
- **No empujar.** Si la objeción es un "no" duro y definitivo, el email reconoce, deja la puerta
  abierta con una sola línea y CORTA. No insiste, no manda tres preguntas, no ruega.
- **Caso de éxito relevante según rubro** (igual que el Email 1):
  - Contables/finanzas → ByData Consultores (no revelar detalles internos)
  - Consultoras/RRHH → Concreto Studio como referencia
  - Tech/agencias → caso de software factory
  - Arquitectura/ingeniería → Concreto Studio (estudio de arquitectura)
- Al cerrar, sugerir al usuario `/memoria ingest` para registrar la objeción y la respuesta en el
  cerebro — así el contexto del prospecto queda completo para el próximo paso.
