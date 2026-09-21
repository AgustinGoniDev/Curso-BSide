# Métricas, formato de `datos.json` y veredicto

## Formato de `datos.json`

Lo armás vos a partir de las queries de Notion y de tu clasificación. Los scripts lo leen y lo enriquecen.

```json
{
  "semana": { "inicio": "2026-09-14", "fin": "2026-09-20", "parcial": false },
  "generado": "2026-09-21",
  "posts": [
    {
      "id": "3df8e29552c38197a8aedf8d1f36efc3",
      "gancho": "Si mañana se va tu cliente más grande, ¿de dónde sale el próximo?",
      "formato": "Texto",
      "fecha": "2026-09-17",
      "impresiones": 2270, "reacciones": 69, "comentarios": 26, "mensajes": 4,
      "lead_ids": ["<id-de-pagina-del-lead>"],
      "tipo": "dolor-icp",
      "fundamento_tipo": "Interpela la dependencia del cliente grande"
    }
  ],
  "pipeline": [
    {
      "id": "<id-de-pagina>",
      "empresa": "Acosta & Rey Contadores",
      "rubro": "Estudio contable B2B", "cargo": "Socia",
      "estado": "Reunión agendada", "origen": "LinkedIn",
      "valor": 1500, "prob": 50,
      "post_ids": ["<id-de-pagina-del-post>"],
      "fit": "fuerte",
      "fundamento_fit": "Rubro y cargo cumplen; $1.500 en rango"
    }
  ]
}
```

- `posts`: todos los posts de la ventana de 5 semanas (las 4 anteriores + la reportada). `id` = ID de página normalizado (ver `notion-schema.md`).
- `pipeline`: **todas** las filas de la base, no solo las atribuidas. `fit` y `fundamento_fit` son obligatorios solo para las filas con `post_ids` dentro de la ventana; para el resto podés omitirlos.
- `valor`, `prob` y `cargo` pueden ser `null`.
- `semana.parcial`: `true` si la semana todavía no cerró.
- Valores válidos: `tipo` ∈ `dolor-icp | educativo-generico | marca-personal`; `fit` ∈ `fuerte | parcial | fuera`.

Flujo:

```bash
python .claude/skills/reporte-semanal-contenido/scripts/calcular_metricas.py datos.json     # agrega "metricas"
# agregás "narrativa" a datos.json
python .claude/skills/reporte-semanal-contenido/scripts/renderizar_reporte.py datos.json reportes/reporte-semanal-AAAA-MM-DD.html
```

`calcular_metricas.py` falla con un mensaje claro si falta `tipo` en un post o `fit` en un lead atribuido de la ventana.

## Formato de `narrativa`

```json
"narrativa": {
  "veredicto": {
    "semaforo": "mixto",
    "frase": "El contenido que trae leads es el que habla del dolor del ICP, pero no es el que más se publica."
  },
  "evidencias": [
    "3 de 4 leads atribuidos en 5 semanas son ICP fuerte",
    "Los 4 posts de más alcance sumaron 0 leads",
    "…"
  ],
  "acciones": {
    "repetir": ["…"],
    "dejar": ["…"],
    "angulos": ["Ángulo 1 derivado de un dolor de cliente.md", "…"]
  },
  "calidad_datos": ["Cada brecha o inconsistencia (podés agregar a las que detecta el script)"],
  "supuestos": ["Ej: las red flags de cliente.md están marcadas como supuesto a validar"]
}
```

`evidencias` son exactamente 3. `acciones.angulos`, de 2 a 3. Los ángulos salen de los dolores de `cliente.md` (pipeline que depende del dueño y de referidos, falta de prospección saliente, no saber qué contenido producir), no de tendencias.

## Definiciones (las calcula el script)

Períodos: **semana** (lunes–domingo reportado), **semana anterior**, **promedio de las 4 semanas previas** (suma ÷ 4) y **ventana de 5 semanas** (las 4 previas + la reportada).

Atribución: un lead pertenece a un post si `pipeline.post_ids` contiene el post **o** `post.lead_ids` contiene el lead. Un lead cuenta una vez por período; en el desglose por tipo o formato, se le acredita a cada post que lo trajo.

| Métrica | Definición |
|---|---|
| Leads atribuidos | Leads únicos cuyos posts caen en el período. |
| Leads ICP | Leads con `fit = fuerte`. `parcial` y `fuera` se informan aparte. |
| % ICP | Leads ICP ÷ leads atribuidos (se muestra siempre con su n). |
| Pipeline atribuido | Suma de `valor` de los leads atribuidos; **ponderado** = Σ valor × prob/100. Los leads sin valor se cuentan aparte, no como cero. |
| Leads ICP / 1.000 imp. | Leads ICP ÷ impresiones × 1.000, por período, por tipo de post y por formato. |
| Peso en impresiones vs peso en leads | Para cada tipo de post: % de las impresiones de la ventana y % de los leads de la ventana. Es el gráfico central: muestra si el alcance y los leads apuntan al mismo lado. |
| Mensajes / post | Mensajes ÷ posts. Señal de intención; las reacciones no lo son. |
| Avance del embudo | Leads atribuidos de la ventana agrupados por `Estado`. |
| Mezcla del pipeline | Por `Origen`: filas, pipeline abierto (estados Contactado, Reunión agendada, Propuesta enviada, En evaluación) en USD y ponderado; y cuánto del pipeline abierto está atribuido a contenido. |

## Semáforo del veredicto

Se calcula sobre la **ventana de 5 semanas** (con ~2 posts por semana, una sola semana casi nunca tiene n suficiente):

| Semáforo | Regla sugerida |
|---|---|
| `sin-datos` | menos de 3 leads atribuidos en la ventana |
| `atrae-icp` | % ICP ≥ 70 % |
| `mixto` | % ICP entre 40 % y 69 % |
| `audiencia-equivocada` | % ICP < 40 % |

El script devuelve `semaforo_sugerido` y, además, `divergencia_alcance_leads` (verdadero cuando el post de más alcance de la ventana no trajo leads y otros de menos alcance sí). Podés cambiar el semáforo si tenés motivo; si lo hacés, escribilo en `narrativa.supuestos`.

Estos umbrales son un punto de partida, no una verdad validada por el negocio: mencionalo si alguien pregunta de dónde salen.

## Límites de muestra

- Mostrar siempre el n absoluto junto a cualquier porcentaje.
- Con n < 3 leads en la ventana, no concluyas sobre tipos de post; describí lo observado.
- Una semana sin leads no prueba que el contenido falle: mirá la ventana.
