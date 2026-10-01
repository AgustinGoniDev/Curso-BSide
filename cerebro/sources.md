# cerebro — Registro de fuentes externas

> Este wiki opera sin fuentes externas configuradas.
> Para referenciar archivos del proyecto, usar prefijo `repo:<path>` en el frontmatter.
> Para URLs externas, usar prefijo `url:<url>` en el frontmatter.

---

## Archivos del repo referenciados

### claude-md-raiz
- **Path:** `CLAUDE.md`
- **Descripción:** Fuente de verdad principal del negocio — identidad, ICP, oferta, snapshot de clientes/pipeline, framework de Email 1.

### docs-que-hacemos
- **Path:** `docs/ofertas-servicios.md`, `docs/README.md`
- **Descripción:** Detalle de la oferta (retainer, proyectos puntuales) usado para poblar [[que-hacemos]].

### docs-cliente
- **Path:** `docs/icp-clientes.md`
- **Descripción:** ICP, dolor típico, red flags y preguntas de calificación usadas para poblar [[cliente]].

### docs-procesos
- **Path:** `docs/proceso-ventas.md`, `docs/proceso-operativo.md`, `docs/equipo-roles.md`
- **Descripción:** Funnel de ventas, ciclo del retainer y estructura de equipo usados para poblar [[procesos]].

### docs-voz
- **Path:** `docs/voz-y-mensajes.md`
- **Descripción:** Framework de Email 1, tono y mensajes clave usados para poblar [[voz]].

### skill-reporte-semanal-contenido
- **Path:** `.claude/skills/reporte-semanal-contenido/`
- **Descripción:** Skill que cruza Contenido y Pipeline de Notion con el ICP de [[cliente]] y genera el reporte semanal en HTML (`reportes/`). Creada en [[2026-09-23-skill-reporte-semanal-contenido]].

### landing-lumen-lab
- **Path:** `landing/copy.md`, `landing/index.html`
- **Descripción:** Copy aprobado y landing page de Lumen Lab (HTML con el CSS adentro). Creada en [[2026-09-28-landing-page-lumen-lab]].

---

## URLs externas

<!-- Agregar cuando una sesión dependa de una URL externa -->

### notion-pipeline-crm
- **URL:** https://www.notion.so/35b8e29552c38082a59dfba5586c8cd4
- **Descripción:** Pipeline CRM de Lumen Lab (Database ID: 86845970-7077-4fde-8e13-0eac9f61300b). Este wiki no hace fetch automático, pero desde 2026-09-23 Notion está disponible en la sesión por conector MCP (ver [[2026-09-23-skill-reporte-semanal-contenido]]). La carpeta raíz "Lumen Lab" contiene además las bases de Contenido y Reportes semanales.

### notion-contenido
- **URL:** https://app.notion.com/p/a11c3f1de5b447cc91733716a6e51325
- **Descripción:** Base "Contenido Lumen Lab" (data source `c74ccafa-9008-47e7-a413-aa7c73fc5ab2`): posts de LinkedIn con impresiones, reacciones, comentarios, mensajes y relación `Leads` hacia el Pipeline.

### notion-reportes-semanales
- **URL:** https://app.notion.com/p/a24822535f004c0684102b7d8120ec72
- **Descripción:** Base "Reportes semanales" (data source `19878eb9-f8ce-4686-ac2f-e3041e8cae04`): una fila por reporte, con `Semana` y `Generado por` (Manual, Tarea local, Rutina nube).

### repo-github-curso-bside
- **URL:** https://github.com/AgustinGoniDev/Curso-BSide
- **Descripción:** Repo de GitHub de esta carpeta (rama `main`, público desde 2026-09-23 por decisión del usuario). Ver [[2026-09-23-skill-reporte-semanal-contenido]].

### australisai-referencia
- **URL:** https://australisai.tech/
- **Descripción:** Landing de Australis AI usada como referencia de estructura y estilo para la landing de Lumen Lab (solo el sistema de layout; colores y fuente salen de [[identidad-visual]]). Ver [[2026-09-28-landing-page-lumen-lab]].

### vercel-lumen-lab-landing
- **URL:** https://lumen-lab-landing.vercel.app
- **Descripción:** Landing de Lumen Lab publicada en Vercel (proyecto `lumen-lab-landing`, cuenta personal, plan gratuito). Conectada al repo [[sources#repo-github-curso-bside]] con raíz en `landing/`: cada push a `main` la vuelve a publicar. Ver [[2026-09-28-landing-page-lumen-lab]].

### claude-code-goal-docs
- **URL:** https://code.claude.com/docs/en/goal.md
- **Descripción:** Documentación oficial del comando `/goal` de Claude Code (condición de cierre evaluada después de cada vuelta). Ver [[2026-10-01-skills-sincronizadas-y-comando-goal]].
