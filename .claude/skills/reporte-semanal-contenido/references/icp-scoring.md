# Rúbrica ICP

Esta rúbrica es la forma de aplicar el contexto del cerebro a los datos de Notion. **La fuente del ICP es `cerebro/contexto/cliente.md`**, no este archivo: leelo en cada corrida. Si cambia el ICP en el cerebro, la rúbrica se adapta; este documento solo explica cómo traducirlo a una clasificación.

## Fit ICP de un lead (`fit`)

Se evalúa con tres señales. Todas salen de la fila del pipeline.

| Señal | Se cumple si… | Fuente |
|---|---|---|
| **Rubro** | El `Rubro` cae en uno de los segmentos del ICP: estudios contables y consultoras de finanzas; agencias y software factories; consultoras de RRHH y reclutamiento; estudios de arquitectura, ingeniería y legal. Debe vender **servicios profesionales B2B**. | `cliente.md` |
| **Cargo** | Es quien decide o el dueño: fundador/a, co-fundador/a, socio/a, socio/a director/a, CEO, CFO-socio, director/a. Un cargo operativo o de marketing sin poder de compra no cumple. | criterio de venta consultiva; `cliente.md` habla del dueño como cuello de botella |
| **Ticket** | El valor propuesto, si existe, está dentro de $1.500–$3.500 USD/mes (o el rango vigente en `que-hacemos.md`). Si `Valor USD/mes` es null, la señal queda **sin dato** (no cuenta en contra). | `que-hacemos.md` |

Clasificación:

- **`fuerte`**: Rubro cumple **y** Cargo cumple, y el ticket no está fuera de rango.
- **`parcial`**: Rubro cumple pero Cargo o ticket no cumplen o no hay dato; o el rubro es adyacente (por ejemplo, consultoría de datos, que es servicio profesional B2B aunque no figure literal en la lista).
- **`fuera`**: el Rubro no es un servicio profesional B2B, o aplica una red flag decisiva de `cliente.md`.

Red flags: tomá las que figuren en la sección "Cliente que no funciona" de `cliente.md` y anotá cuál aplica. Hoy están marcadas como **supuesto a validar**; si las usás para bajar un fit, decilo ("red flag no confirmada"). Los datos de Notion suelen no alcanzar para detectarlas (por ejemplo, "no quieren exponer su marca en LinkedIn"), así que en la mayoría de los casos no vas a poder aplicarlas: no las supongas.

Escribí una línea de fundamento por lead: `"Estudio contable B2B, socia: rubro y cargo cumplen, $1.500 en rango"`.

Cuando el rubro sea ambiguo, elegí `parcial` y explicalo. Es mejor un `parcial` honesto que un `fuerte` inflado, porque el reporte existe para detectar si estamos atrayendo a quien no debemos.

## Tipo de post (`tipo`)

Se decide por el **gancho** (y el formato si ayuda), comparado contra el dolor y la oferta.

| Tipo | Qué es | Señales en el gancho |
|---|---|---|
| **`dolor-icp`** | Habla del dolor concreto del ICP: pipeline que depende del dueño y de referidos, falta de prospección saliente, no saber qué contenido producir ni cómo posicionarse. Interpela a un dueño de servicio profesional. | "si se va tu cliente más grande…", "el referido es bueno, el problema es que sea la única puerta", "todos los estudios contables dicen lo mismo", casos de una consultora de datos armando una segunda vía de clientes |
| **`educativo-generico`** | Consejo de marketing o LinkedIn que le sirve a cualquiera: hashtags, herramientas de IA, ganchos, errores de perfil, tendencias. No filtra por ICP. | "cómo usar los hashtags", "herramientas de IA para contenido", "las 7 tendencias de marketing B2B", "guía: escribir un gancho" |
| **`marca-personal`** | Frase inspiracional o detrás de escena sin tesis sobre el problema del ICP. | "Lunes: la constancia le gana al talento", "así planificamos un mes de contenido en dos horas" |

Un post puede rozar dos tipos. Elegí el que domina el gancho y anotá la duda en el fundamento. Si un consejo genérico está **dirigido explícitamente** a un segmento del ICP (por ejemplo, "por qué nadie abre tu newsletter" dicho a consultoras), es `educativo-generico` con nota, no `dolor-icp`, salvo que ataque el dolor central (dependencia de referidos, falta de sistema de prospección).

La clasificación no depende de cuánto alcance tuvo: se decide sin mirar las métricas, para que el reporte pueda descubrir si el alcance y el tipo se contradicen.

## Qué NO hace esta rúbrica

- No estima la audiencia de LinkedIn: no hay datos. Solo evalúa **leads reales** y **contenido publicado**.
- No decide si un lead es "bueno para cerrar": eso es `Probabilidad cierre %`, que carga el equipo comercial.
