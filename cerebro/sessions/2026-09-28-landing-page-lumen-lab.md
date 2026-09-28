---
type: session
area: general
date: 2026-09-28
slug: 2026-09-28-landing-page-lumen-lab
title: "Landing page de Lumen Lab: copy y diseño"
tags: [landing, copy, web, identidad-visual, prueba-social, voz]
status: active
related:
  - voz
  - pruebas
  - cliente
  - identidad-visual
  - que-hacemos
sources:
  - repo:landing/copy.md
  - repo:landing/index.html
  - url:https://australisai.tech/
superseded_by: null
---

# Landing page de Lumen Lab: copy y diseño

## Contexto

El usuario pidió construir una landing page para Lumen Lab en dos fases: primero el copy y después la estructura visual. Todo el contenido salió de `cerebro/contexto/`: la oferta de [[que-hacemos]], el dolor y las citas de [[cliente]], las reglas de [[voz]], los testimonios de [[pruebas]] y los colores y la tipografía de [[identidad-visual]]. Para la fase 2 el usuario pidió copiar el estilo de la landing de Australis AI (https://australisai.tech/), adaptado a la marca de Lumen Lab. Aprobó el copy sin cambios antes de pasar al diseño.

## Decisiones

- **CTA único: agendar una conversación.** Se descartó vender la auditoría de USD 800 como acción principal. Rationale: coherente con el framework "Consultor, no Vendedor" de [[voz]]. La auditoría aparece como opción secundaria, sin botón propio, para responder la objeción "no quiero comprometerme a un mensual sin conocerlos".
- **Tono neutro LATAM (tú, sin voseo ni "usted") para la landing.** Rationale: la landing apunta a los 5 países del mercado. [[voz]] tenía el tono formal/informal como **Abierto**; esta decisión aplica a la landing y queda por confirmar si vale para toda la comunicación.
- **Titular del hero:** "Que tus próximos clientes no dependan de que alguien te nombre". Sale del síntoma más repetido en [[cliente]] ("Dependemos de que alguien nos nombre", 9 personas). Quedan 2 variantes para testear.
- **Casos sin métricas.** [[pruebas]] no tiene números verificados, así que donde Australis AI muestra métricas (80+, 40%), las tarjetas muestran la frase clave de la cita del cliente. En Faro Consulting se agregó el "Antes / Después" de su frase.
- **Plazos contados con lo que dijo ByData:** "Meses 1 y 2: no pasó casi nada" y "Mes 4: ya teníamos reuniones". Convierte la objeción del tiempo en una señal de honestidad y filtra a quien espera resultados en semanas.
- **Se copia el sistema de Australis AI, no su marca.** Se tomaron la estructura (menú fijo, hero a pantalla completa con las últimas palabras en color de acento, secciones alternadas, lista 01–04, línea de pasos, tarjetas de casos, cierre oscuro con footer de 3 columnas). Colores y fuente salen de [[identidad-visual]]: el verde pasa a coral `#e94560`, el negro a azul noche `#1a1a2e` y Montserrat a Inter 700.
- **Coral muy acotado.** Solo en el botón principal y en "alguien te nombre" del titular. El botón del menú va en azul noche para que no haya dos botones coral en la primera pantalla.
- **Sin sección "Sobre nosotros" por ahora:** no hay texto ni foto de Tomás, y [[identidad-visual]] prohíbe fotos de stock.
- **Formato:** un solo `landing/index.html` con el CSS dentro, pensado primero para celular, sin dependencias salvo Inter de Google Fonts.

## Output

- `landing/copy.md`: copy completo (meta, hero con 3 variantes de titular, 9 secciones, footer) y lista de 8 pendientes de validar. Revisado: sin palabras prohibidas de [[voz]], sin voseo, sin números que no haya dicho un cliente.
- `landing/index.html`: la landing terminada. Revisada en computadora y en celular (375px), sin que se salga de la pantalla hacia los costados. Los datos que faltan están marcados con comentarios `PENDIENTE` en el código.

## Pendiente

- **Link de agenda:** el botón final apunta a `AGENDA_URL`; hay que reemplazarlo por el link real (y confirmar la duración de la reunión).
- **Permiso de los clientes** para publicar su nombre y su cita. Andrés Villalba (Villalba & Asociados) aparece solo en [[cliente]], que junta clientes y prospectos: confirmar si es cliente o cambiar la cita del problema 04.
- **Quién dijo las citas de ByData y Pampa Talent** (en [[pruebas]] solo figura la empresa; podrían ser Carolina Méndez e Ignacio Paredes, sin confirmar).
- **Rubro de Kodea** para la etiqueta de su tarjeta (hoy muestra el nombre de la empresa).
- **"Para quién no es":** se apoya en las red flags de [[cliente]], que siguen como supuesto a validar. Tomás tiene que confirmarlas antes de publicar.
- **Datos de contacto** del footer (email, LinkedIn, WhatsApp).
- **Sección "Sobre nosotros":** falta texto en primera persona de Tomás y, si puede, una foto real.
- **Decidir si el tono neutro LATAM vale para toda la comunicación** y, si es así, cerrar el **Abierto** de [[voz]].
- Publicar la landing (hosting y dominio no definidos).

## Cross-refs
- [[voz]] — el copy aplica sus reglas y el CTA sigue el framework "Consultor, no Vendedor"; la sesión decide el tono para la landing.
- [[pruebas]] — única fuente de las citas y los casos de la landing.
- [[cliente]] — de acá salen el titular, los 4 síntomas del problema, las objeciones del FAQ y los red flags.
- [[identidad-visual]] — define los colores, la tipografía y el logotipo de la landing.
- [[que-hacemos]] — la oferta (retainer y auditoría) que describe la sección "Cómo trabajamos".

## Fuentes
- [[sources#landing-lumen-lab]]
- [[sources#australisai-referencia]]
- Origen histórico (no modificar): `landing/copy.md`, `landing/index.html`
