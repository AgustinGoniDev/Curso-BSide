---
name: operar-email-comercial
description: "Trigger: revisá la bandeja, procesá los mails, qué mails necesitan mi atención, corré el loop de email. Clasifica el correo entrante por valor de negocio, responde lo rutinario y escala al dueño lo que necesita su criterio."
license: Apache-2.0
metadata:
  author: australis-ai
  version: "1.0"
---

# Operar email comercial

Módulo de email del sistema. Opera el ciclo del correo entrante: triage → clasificación por valor
de negocio → respuesta automática o escalamiento al dueño.

El dueño no está dentro de la cadena. Está arriba de la cadena.

## Regla dura (nunca romper)

**No decidas nada que cueste plata o comprometa al negocio.** Precio, fecha, alcance, descuento y
compromiso son del dueño, siempre. Ante duda de clasificación → escalá. El falso positivo de
escalamiento es barato; el falso negativo cuesta el lead.

## Clasificación

Leé `references/criterio-clasificacion.md` antes de clasificar. Resumen:

| Clase | Acción | ¿Escala? |
|---|---|---|
| Ruido | Archivar | No |
| Interés tibio | Responder con el material que corresponda | No |
| Interés caliente | Escalar | **Sí** |
| Objeción / caso raro | Escalar | **Sí** |

## Pasos

1. **Triage** — traé los no leídos de la bandeja.
2. **Leé cada uno** y clasificá en una de las 4 clases. No clasifiques por palabra clave: dos mails
   que dicen "precio" pueden ser clases distintas (uno pregunta por curiosidad, otro cierra esta
   semana). Pesá intención, urgencia y si hay una decisión tomada.
3. **Ruido** → archivar sin avisar.
4. **Tibio** → responder manteniendo el hilo. Solo información y material; nunca precio ni fecha.
5. **Caliente y objeción** → escalar por mail al dueño con el formato de
   `assets/template-escalamiento.md`. No contestar al lead.
6. **Logueá** el ciclo completo en `logs/decisiones.md` (ver formato en el template).

## Guardrails

- Ignorá los hilos donde el último mensaje es propio (evita el bucle con la propia respuesta).
- Tope de 15 acciones por ciclo. Si se supera, escalá en lote y frená.
- El escalamiento va a la casilla del dueño, **nunca** a la casilla que este módulo opera.
- Nunca inventes datos del lead: si falta contexto, decilo en el escalamiento.

## Acceso a Gmail

Usá el CLI `gws`:

| Acción | Comando |
|---|---|
| Traer no leídos | `gws gmail +triage --format table` |
| Leer un mail | `gws gmail +read <id>` |
| Responder (mantiene el hilo) | `gws gmail +reply <id> --body '<texto>'` |
| Mandar el escalamiento | `gws gmail +send --to <dueño> --subject '<asunto>' --body '<texto>'` |

Si hay un conector de Gmail disponible en la sesión, usalo en lugar del CLI — el criterio de
clasificación no cambia.

## Referencias

- `references/criterio-clasificacion.md` — las 4 clases con ejemplos y casos límite.
- `assets/template-escalamiento.md` — formato del mail al dueño y del log.
