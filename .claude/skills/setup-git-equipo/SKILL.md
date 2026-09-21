---
name: setup-git-equipo
description: "Guía paso a paso, pensada para gente no técnica, para dejar la PC lista para trabajar con Git y GitHub y configurar el repositorio de una carpeta: chequea qué falta, instala Git y GitHub CLI, configura la identidad, inicia sesión en GitHub, crea el repo y hace la primera subida (o se conecta a uno que ya existe) e invita al equipo. Usá este skill cuando el usuario diga 'subí esta carpeta a GitHub', 'quiero tener esto en GitHub', 'creá el repo', 'configurame git', 'setup del equipo', 'quiero trabajar en equipo sobre esta carpeta', 'conectame al repo de mi equipo', 'soy nuevo en el equipo, ayudame a configurar esto', '¿tengo todo para usar git?', 'instalá lo que falta para usar git', o cualquier variante que pida versionar una carpeta, compartirla vía GitHub o dejar una máquina lista para colaborar — aunque no mencione la palabra 'git'."
---

# Skill: dejar todo listo para trabajar con Git y GitHub

Este skill acompaña a alguien, que muchas veces no es técnico, desde "tengo una carpeta en
mi PC" hasta "la carpeta está en GitHub y mi equipo puede trabajar sobre ella". No depende de
ningún proyecto en particular: todo lo específico (nombre del repo, cuenta, carpeta) se
descubre o se pregunta.

Tu rol es de guía. Antes de cada paso, explicá en una línea qué vas a hacer y por qué;
después, confirmá el resultado. Muchas veces esto se muestra en vivo, así que lo que más
importa es que se entienda qué está pasando. Evitá la jerga. Si aparece un término (repo,
commit, push), definilo en media línea la primera vez que lo uses.

No crees archivos ni herramientas extra en la carpeta del usuario (scripts, atajos, tareas
programadas). El objetivo es que tenga Git y GitHub funcionando y entienda cómo usarlos. Lo
único que se agrega al repo es el `.gitignore`.

---

## Paso 0 — Diagnóstico

Chequeá todo en silencio y después mostrá un resumen tipo checklist (✅ listo / ❌ falta):

| Chequeo | Comando |
|---|---|
| Git instalado | `git --version` |
| GitHub CLI instalado | `gh --version` |
| Identidad de Git | `git config --global user.name` y `user.email` |
| Sesión en GitHub | `gh auth status` |
| ¿La carpeta ya es un repo? | `git rev-parse --show-toplevel` |
| ¿Tiene remoto? | `git remote -v` |

Con eso, determiná el **escenario**:

- **A — Carpeta nueva a GitHub:** la carpeta no es repo, o es repo sin remoto, y el usuario
  quiere crear el repo en GitHub. Es el caso más común.
- **B — Sumarse a un repo que ya existe:** alguien del equipo ya lo creó y el usuario quiere
  tenerlo en su PC.
- **C — Ya está todo conectado:** hay remoto en GitHub. Solo completá lo que haya salido ❌
  en el checklist y pasá al cierre.

Si no queda claro si es A o B, preguntá: "¿Esta carpeta ya existe en GitHub (la creó alguien
del equipo) o es la primera vez que la subimos?".

Si la carpeta está dentro de **OneDrive, Dropbox o Google Drive**, avisá: la sincronización
de la nube y Git pueden pisarse y generar archivos duplicados o conflictos raros. No es
bloqueante y mucha gente trabaja así, pero conviene saberlo. Si el usuario prefiere mover la
carpeta afuera de la nube, es el momento. No la muevas sin que lo pida.

Saltá los pasos que ya estén resueltos.

---

## Paso 1 — Instalar lo que falte

- **Git:** el programa que lleva el historial de cambios de la carpeta.
- **GitHub CLI (`gh`):** permite hablar con GitHub desde la terminal para iniciar sesión,
  crear repos o invitar gente sin pasar por la web.

**Windows** (winget viene con Windows 10/11):

```
winget install --id Git.Git -e --silent --accept-source-agreements --accept-package-agreements
winget install --id GitHub.cli -e --silent --accept-source-agreements --accept-package-agreements
```

Después de instalar, la terminal actual no ve los programas nuevos hasta refrescar el PATH:

```powershell
$env:PATH = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
```

**Mac:** `brew install git gh`. Si no hay Homebrew, indicá https://brew.sh.
**Linux:** gestor de paquetes (`sudo apt install git gh` o equivalente). Como pide
contraseña, que el usuario lo corra él.

Verificá con `git --version` y `gh --version`. Si la instalación automática falla, pasale los
links de descarga manual (https://git-scm.com/downloads, https://cli.github.com) y esperá a
que confirme.

---

## Paso 2 — Identidad de Git

Cada cambio guardado lleva nombre y email del autor, así el equipo sabe quién hizo qué. Si
`user.name` o `user.email` están vacíos, preguntá cómo quiere aparecer (idealmente, el email
de su cuenta de GitHub) y configuralos:

```
git config --global user.name "Nombre Apellido"
git config --global user.email "mail@ejemplo.com"
```

Aprovechá para dejar estos dos ajustes, que evitan confusiones al trabajar en equipo:

```
git config --global init.defaultBranch main
git config --global pull.rebase true
```

Explicale `pull.rebase` en una línea: al traer cambios de otros, pone los tuyos encima en vez
de crear un paso extra de "merge". El historial queda más prolijo.

---

## Paso 3 — Iniciar sesión en GitHub

Si `gh auth status` dice que no hay sesión:

1. Preguntá si ya tiene cuenta de GitHub. Si no tiene, que la cree en
   https://github.com/signup y avise cuando termine.
2. Corré el login **en background**, porque queda esperando a que el usuario termine en el
   navegador:
   ```
   gh auth login --hostname github.com --git-protocol https --web
   ```
3. Leé la salida y mostrale, bien visibles, el **código de un solo uso** (`XXXX-XXXX`) y la
   URL **https://github.com/login/device**, que es donde pega el código y autoriza.
4. Cuando el proceso termine, confirmá con `gh auth status` y decí con qué usuario quedó.
5. Corré `gh auth setup-git` para que Git use esta sesión y no pida contraseña al subir.

Nunca pidas que pegue tokens, contraseñas ni el código en el chat. El código se ingresa en
GitHub, no acá.

---

## Paso 4A — Carpeta nueva a GitHub

Este paso publica archivos, así que antes de subir nada revisá con el usuario **qué** se va a
subir.

1. **`.gitignore`** (la lista de cosas que Git no debe subir). Si no existe, creá uno con lo
   básico y sumá lo que corresponda según lo que haya en la carpeta:
   ```gitignore
   # Secretos y credenciales
   .env
   .env.*
   !.env.example
   *.key
   *.pem
   credentials*.json

   # Sistema operativo y temporales
   Thumbs.db
   desktop.ini
   .DS_Store
   ~$*

   # Dependencias (si aplica)
   node_modules/
   .venv/
   __pycache__/
   ```
2. **Revisión de riesgos:** buscá y mostrá
   - posibles secretos: `.env*`, `*.key`, `*.pem`, `credentials*`, archivos con tokens o
     contraseñas a la vista;
   - archivos de más de 50 MB (GitHub rechaza los de más de 100 MB);
   - cantidad total de archivos y tamaño aproximado.

   Si hay secretos, proponé sumarlos al `.gitignore` antes de seguir. Esto importa: una
   clave que se sube queda en el historial aunque después se borre.
3. **Decisiones del usuario** (preguntá, no asumas):
   - Nombre del repo. Sugerí uno derivado de la carpeta, en minúsculas y con guiones.
   - **Privado o público.** Sugerí privado, que casi siempre es lo que se quiere para trabajo
     de un equipo o de clientes.
   - Si va en su cuenta personal o en una organización (`gh org list` muestra las que tiene).
4. **Crear y subir:**
   ```
   git init                  # solo si la carpeta no era repo
   git add -A
   git commit -m "Primera versión"
   gh repo create <owner>/<nombre> --private --source . --remote origin --push
   ```
   Si ya era repo con commits pero sin remoto, saltá `git init` y el commit, y usá el mismo
   `gh repo create`.
5. Mostrá la URL del repo. `gh repo view --web` lo abre en el navegador, y es un buen momento
   para que vea sus archivos en GitHub.

---

## Paso 4B — Sumarse a un repo existente

1. Pedí la URL o el `dueño/nombre` del repo.
2. Chequeá el acceso con `gh repo view <dueño/nombre>`. Si da error de permisos o "not
   found", el dueño tiene que invitarlo (ver Paso 5). El invitado acepta desde el mail o en
   https://github.com/notifications. Frená ahí hasta que confirme.
3. Según el estado de la carpeta actual:
   - **Carpeta vacía o sin relación con el repo:** preguntá dónde quiere el proyecto y
     clonalo con `gh repo clone <dueño/nombre> [carpeta]`.
   - **La carpeta tiene archivos y el repo remoto está vacío:** seguí el Paso 4A, pero
     conectando al remoto existente (`git remote add origin <url>` y después
     `git push -u origin main`).
   - **Los dos tienen contenido:** no mezcles automáticamente. Explicá las opciones: clonar en
     otra carpeta y copiar a mano lo que falte, o unir historiales (más delicado). Dejá que
     elija.

---

## Paso 5 — Invitar al equipo (opcional, si el usuario es dueño del repo)

Preguntá si quiere sumar compañeros ahora. Por cada usuario de GitHub que te pase:

```
gh api -X PUT repos/<owner>/<repo>/collaborators/<usuario> -f permission=push
```

También se puede hacer desde la web: repo → Settings → Collaborators. Contale qué tiene que
hacer cada invitado: aceptar la invitación y correr este mismo skill en su PC (va a caer en
el escenario B).

---

## Paso 6 — Verificación y cierre

Volvé a mostrar el checklist del Paso 0, ahora todo en ✅, más:
- URL del repo y carpeta local.
- Usuario de GitHub con el que quedó conectado.

Terminá con el uso diario en tres líneas, en palabras simples:
- **Antes de empezar:** traer lo último del equipo (`git pull`), o pedirle a Claude "bajá los
  cambios".
- **Cuando terminás algo:** guardar y subir (`git add -A`, `git commit -m "qué cambié"`,
  `git push`), o pedirle a Claude "subí mis cambios".
- **Si algo se traba:** pedirle a Claude "revisá el estado de git".

---

## Si algo sale mal

- **`git push` rechazado ("fetch first", "non-fast-forward"):** alguien subió antes. Hacé
  `git pull` y reintentá.
- **Conflicto:** mostrá qué archivos están en conflicto (`git status`), explicá en criollo que
  dos personas tocaron lo mismo y resolvelo junto al usuario. Nunca descartes cambios suyos
  sin preguntar.
- **"Permission denied" / 403 al subir:** revisá `gh auth status` y que el usuario sea
  colaborador con permiso de escritura.
- **Archivo demasiado grande:** sacalo del commit (`git rm --cached <archivo>`), sumalo al
  `.gitignore` y reintentá.
- **winget no existe o falla:** instalación manual con los links del Paso 1.
