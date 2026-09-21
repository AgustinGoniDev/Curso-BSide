# Captura del contexto del negocio

Guía de la entrevista que puebla `{{WIKI_DIR}}/contexto/`. Cuatro áreas, cuatro archivos.

El wiki recién instalado sabe cómo guardar lo que pasa, pero no sabe nada del negocio. Esta
entrevista es lo que lo convierte de un archivador vacío en algo que puede producir trabajo.

## Cómo se conduce

Es una entrevista, no un formulario.

**Una pregunta por vez. Preguntá, frená, esperá.** Nunca mandes una lista numerada de preguntas.
Es la regla que más se rompe cuando uno quiere parecer eficiente, y es la que hace que esto se
sienta como una conversación en vez de un trámite.

**Al cerrar cada área, escribí el archivo y decilo.** El usuario tiene que ver que algo se está
construyendo mientras habla. Escribir todo al final es donde se pierde la sensación de que esto
funciona.

**Máximo una repregunta por área.** Si la respuesta alcanza, cerrá el archivo y seguí. Esta
entrevista busca una primera pasada completa, no la versión definitiva.

**Devolvé lo que entendiste.** Después de una respuesta importante, decí en una frase qué entendiste
y dejá que te corrija. Las correcciones son el material más valioso: es donde el usuario afina lo
que realmente quiso decir.

**Aceptá "no sé".** Un hueco anotado con honestidad vale más que un invento convincente. Se escribe
como `**Abierto:** ...` y se sigue.

**Usá las palabras del usuario.** Si dice "los pedidos", el archivo dice "los pedidos", no "las
órdenes de trabajo". Su vocabulario es parte de lo que hace suyo al sistema.

**Nunca escribas algo que el usuario no haya dicho.**

---

## 1. Qué hace el negocio → `que-hacemos.md`

**Apertura:** ¿A qué se dedica tu negocio? Contámelo como se lo contarías a alguien que recién
conocés.

Repregunta, según lo que diga:

- ¿Qué es lo que te compran exactamente?
- Cuando alguien te elige a vos y no a otro, ¿por qué te elige?

**Lo que buscás:** qué vende, a cambio de qué, y qué lo hace distinto. Si contesta con una categoría
("hago marketing"), pedile un ejemplo concreto del último trabajo que entregó.

---

## 2. Quién compra → `cliente.md`

**Apertura:** Pensá en tu mejor cliente del último año. ¿Quién es y por qué te buscó?

Repregunta:

- ¿En qué situación estaba cuando te contactó? ¿Qué le estaba pasando?
- ¿Hay algún tipo de cliente que te llega seguido y con el que la cosa no funciona?

**Lo que buscás:** la situación concreta en la que alguien se convierte en cliente, no un dato
demográfico. "Empresas de 10 a 50 personas" no sirve; "el dueño se dio cuenta de que está frenando
al equipo" sí.

El cliente que **no** funciona suele ser más informativo que el ideal.

---

## 3. Cómo se trabaja → `procesos.md`

**Apertura:** Llevame desde que alguien muestra interés hasta que está cobrado y entregado. ¿Qué
pasa en el medio?

Repregunta:

- De todo eso, ¿qué está escrito en algún lado y qué vive sólo en tu cabeza?
- ¿Qué parte se rompe más seguido?

**Lo que buscás:** el recorrido real, con sus huecos. Lo que **no** está documentado importa tanto
como lo que sí — anotalo explícitamente.

Si describe un proceso ideal, traelo a tierra: ¿la última vez fue así?

---

## 4. Cómo se escribe y qué no se dice → `voz.md`

**Apertura:** ¿Cómo suena tu marca cuando escribe? Pensá en un mensaje tuyo que te haya salido bien.

Repregunta:

- ¿Hay palabras o frases que nunca usarías? ¿Qué te suena a otro y no a vos?
- ¿Tratás de usted o de vos? ¿Formal o cercano?

**Lo que buscás:** el tono, el vocabulario propio y —sobre todo— **la lista de lo que nunca se
dice**. Esa lista es lo que más rápido mejora el output: es más fácil para el sistema evitar
palabras prohibidas que imitar un tono.

Si no sabe describir su tono, pedile que pegue dos o tres frases suyas que le gusten y deducilo de
ahí, mostrándole qué dedujiste.

---

## Cómo escribir cada archivo

Al cerrar el área, escribí el archivo en `{{WIKI_DIR}}/contexto/` y decilo en voz alta.

**El frontmatter es el mismo que el de cualquier nodo del wiki**, con `type: contexto`. Si le ponés
menos campos, el propio `lint` te lo va a reportar como frontmatter inválido y los `[[wikilinks]]`
entre archivos de contexto no van a resolver, porque resuelven contra `slug`.

```yaml
---
type: contexto
area: <un área del proyecto>
date: AAAA-MM-DD
slug: <igual al nombre del archivo sin .md>
title: "<título humano>"
tags: [<libres, kebab-case>]
status: active
related:
  - <slugs de los otros archivos de contexto>
sources: []
superseded_by: null
---
```

Los archivos de contexto **no llevan fecha en el nombre**: son `que-hacemos.md`, no
`2026-09-09-que-hacemos.md`. Describen lo que el negocio es, no lo que pasó un día. El campo `date`
registra cuándo se escribió o actualizó.

El cuerpo:

- Abre con una línea que resume qué contiene el archivo.
- Usa las palabras del usuario.
- Marca lo que no se sabe con `**Abierto:** ...`.
- Cierra con `## Cross-refs` enlazando a los otros archivos de contexto con `[[slug]]`, y la razón
  en una línea.

Agregá cada archivo a la sección **Contexto del negocio** de `{{WIKI_DIR}}/index.md` en el momento,
no al final.

## Calibrar la profundidad

Leé al usuario.

Si contesta corto, quiere terminar: sacá lo esencial y cerrá. Si se extiende, está pensando en voz
alta y ahí está el mejor material: dejalo.

**Mejor tres archivos honestos que cuatro rellenados.**

## Si hay que cortar

Se puede cortar en cualquier área. Antes de cortar:

1. Escribí el archivo del área en curso con lo que haya.
2. Anotá en `{{WIKI_DIR}}/index.md` qué áreas quedaron pendientes.
3. Decí en una línea cuál es la próxima pregunta, para poder retomar sin repetir.

Un contexto parcial sirve. Una entrevista abandonada, no.
