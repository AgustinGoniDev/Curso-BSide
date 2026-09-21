---
name: generar-propuesta
description: "Genera una propuesta comercial completa para un prospecto de Lumen Lab. Triggereá cuando el usuario diga 'generá la propuesta para [empresa]', 'armá la propuesta de [cliente]', 'hacé la propuesta de [nombre]', 'necesito la propuesta para la reunión con [empresa]', o cualquier variante que pida crear un documento comercial de cierre."
---

# Skill: Generar Propuesta — Lumen Lab

Genera una propuesta comercial completa basada en el dolor y alcance del cliente.

## Parámetros

El usuario provee (en cualquier formato):
- **cliente**: nombre de la empresa y contacto
- **dolor**: el problema operativo o negocio identificado en la reunión
- **alcance**: qué se construye / entrega
- **valor**: precio mensual o de proyecto (si ya está definido)
- Cualquier contexto adicional de la conversación o el cerebro

---

## Step 1 — Buscar contexto del cliente en el cerebro

Antes de generar, hacer `WebSearch` en el directorio local o consultar `cerebro/` para:
- ¿Hay notas de reuniones o calls previas con este cliente?
- ¿Hay señales de investigación previas?
- ¿Qué problema detectamos originalmente que los trajo al pipeline?

Si hay un nodo en `cerebro/sessions/` con el nombre del cliente, leerlo.

---

## Step 2 — Validar los inputs

Si falta el dolor o el alcance, pedirlos antes de generar. Sin estos dos inputs, la propuesta no puede ser específica y pierde valor.

Si falta el valor: calcular según la tabla de precios de Lumen Lab:
- Retainer core (posicionamiento + contenido + outbound): $1.500–$2.500 USD/mes
- Retainer full (core + lead gen activo): $2.500–$3.500 USD/mes
- Auditoría puntual: $800 USD
- Setup inicial de funnel: $1.500–$2.500 USD

---

## Step 3 — Generar la propuesta en HTML

Generar un archivo HTML standalone (`propuesta-{empresa}.html`) con el siguiente contenido y estructura visual:

### Estructura de la propuesta

**Header:**
- Logo/nombre Lumen Lab (tipografía grande, oscuro)
- Título: "Propuesta Comercial — {Empresa}"
- Fecha: fecha actual

**Sección 1 — El problema (en lenguaje del cliente)**
Reescribir el dolor que describió el cliente como si fuera el principio de una historia. Máximo 3 párrafos. Usar los datos concretos que mencionó. El cliente debe leer esto y pensar "exactamente, así es".

Estructura interna:
- Párrafo 1: situación actual del negocio (dónde están)
- Párrafo 2: el problema específico y su costo operativo (lo que les genera el dolor)
- Párrafo 3: el costo de no resolverlo (por qué importa ahora)

**Sección 2 — La solución propuesta**
Describir qué vamos a construir/implementar. Concreto, sin jerga de marketing.
- Qué incluye el retainer mensual (bullets claros)
- Qué NO incluye (para manejar expectativas desde el inicio)
- Entregables de los primeros 30 días

**Sección 3 — Cómo trabajamos**
3-4 bullets sobre la metodología de Lumen Lab:
- Diagnóstico de posicionamiento antes de producir nada
- Primer mes de contenido y outbound como prueba, no como contrato eterno
- Revisión mensual de métricas y ajuste de estrategia
- El cliente es autónomo al final del proceso — no dependencia de la agencia

**Sección 4 — Inversión**
| Componente | Valor |
|-----------|-------|
| {Descripción del retainer} | ${valor} USD/mes |
| Duración mínima inicial | 3 meses |
| Forma de pago | Mensual, inicio de mes |

Si hay proyecto puntual además del retainer, agregar fila separada.

**Sección 5 — Próximos pasos**
3 pasos concretos con fechas tentativas:
1. Confirmar propuesta → {fecha: hoy + 3 días hábiles}
2. Kick-off de diagnóstico → {fecha: semana siguiente}
3. Primeros entregables → {fecha: 2 semanas desde kick-off}

**Footer:**
- "Agustín Goñi — Founder, Lumen Lab"
- Email de contacto ficticio: agustin@lumenlab.com
- "Esta propuesta es válida por 15 días desde la fecha de envío."

---

### Estilo visual del HTML

- Fondo: blanco (#FFFFFF)
- Tipografía: Inter o sistema sans-serif
- Color primario: #1a1a2e (azul muy oscuro)
- Acento: #e94560 (rojo/coral — color de marca Lumen Lab)
- Máximo 700px de ancho, centrado
- Sin dependencias externas (todo inline o CDN de Google Fonts)
- Imprimible — que se vea bien en PDF también

---

## Step 4 — Generar el email de envío

Además del HTML, generar el email que acompaña la propuesta:

```
Asunto: propuesta para {empresa} — {mes} 2026

{Nombre del contacto},

Adjunto la propuesta que mencionamos en la reunión.

El foco está en [el dolor principal en 1 oración]. El primer mes es de diagnóstico — no producimos nada hasta tener claro el posicionamiento y los mensajes que van a resonar con tu ICP.

Si tenés alguna pregunta sobre el alcance o los números, podemos hablar esta semana.

Agustín
```

---

## Step 5 — Output final

Entregar:
1. El archivo `propuesta-{empresa}.html` creado localmente
2. El email de envío listo para copiar
3. Resumen de inputs usados (dolor, alcance, valor, contexto del cerebro)

Si hay un nodo en el cerebro relacionado con este cliente, sugerir al usuario que haga `/memoria ingest` al cerrar la sesión para registrar que la propuesta fue generada.
