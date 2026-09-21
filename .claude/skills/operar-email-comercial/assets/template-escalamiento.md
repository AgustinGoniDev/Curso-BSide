# Template de escalamiento y log

## Mail al dueño

El escalamiento **no es un aviso de "tenés un mail nuevo"**. Es la decisión ya masticada: el dueño
tiene que poder responder con una línea.

**Asunto:** `[DECISIÓN] <nombre> — <qué necesita en 3-4 palabras>`

**Cuerpo:**

```
Quién:        <nombre, empresa, y de qué campaña o hilo viene>
Qué pide:     <una línea, sin rodeos>
Contexto:     <qué se le mandó antes, qué respondió, hace cuánto>
Recomiendo:   <la acción concreta que propongo>
Necesito:     <la decisión exacta: sí/no, un número, una fecha>
```

Reglas:

- **Una sola decisión por mail.** Si hay dos leads, dos mails.
- `Necesito` tiene que ser respondible con una línea. Si el dueño necesita escribir un párrafo para
  contestar, la pregunta está mal formulada.
- Si falta información para recomendar, decilo explícitamente. Nunca inventes contexto.
- Nada de resúmenes largos: el mail entero entra en una pantalla.

### Ejemplo

```
Asunto: [DECISIÓN] Diego Ocampo — precio para cerrar esta semana

Quién:        Diego Ocampo, Ocampo y Asociados. Respondió a la campaña de agosto.
Qué pide:     El precio para firmar esta semana.
Contexto:     Primer contacto. Dice que ya lo hablaron internamente con el socio y el
              contador, y que tienen presupuesto aprobado para arrancar en agosto.
Recomiendo:   Mandarle el rango del paquete base y ofrecerle una llamada de 20 min
              para ajustar alcance antes de cerrar el número.
Necesito:     ¿Le paso el rango o preferís llamarlo vos primero?
```

---

## Log de decisiones

Un bloque por ciclo, al final de `logs/decisiones.md` (más reciente abajo).

```markdown
## <YYYY-MM-DD HH:MM>

Revisados: <N> mails.

| Remitente | Asunto | Clase | Acción | Por qué |
|---|---|---|---|---|
| <quién> | <asunto> | <clase> | archivado / respondido / escalado | <criterio aplicado, una línea> |

Escalados: <N>. Respondidos: <N>. Archivados: <N>.
```

La columna **Por qué** es la que hace auditable el sistema. Nunca dejarla vacía: si no se puede
explicar el criterio en una línea, la clasificación está mal.
