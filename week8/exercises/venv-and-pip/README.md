# Semana 8 · Modularización — pip y Entornos Virtuales

Notas de la cápsula + ejercicios resueltos. Material de apoyo para repasar.

## Contenido de esta carpeta

| Archivo / carpeta | Ejercicio |
| --- | --- |
| `requirements.txt` | Ejercicios 1 y 2 — dependencias de `requests` generadas con `pip freeze` |
| `demo_rich.py` | Ejercicio 3 — demo de la librería `rich` |
| `gestor_tareas/` | Ejercicio 4 — proyecto completo (venv + `rich` + `requirements.txt` + `main.py`) |
| `venv/`, `venv2/`, `gestor_tareas/venv/` | Entornos virtuales locales (**no se suben a Git**) |

---

## 1. ¿Qué es pip?

**pip** es el gestor de paquetes de Python: instala librerías que otras personas crearon.
Analogía: una tienda de herramientas; en vez de fabricar cada herramienta, la pides y la agregas a tu taller.

```bash
pip install requests
```

```python
import requests

respuesta = requests.get("https://api.github.com")
print(respuesta.status_code)
```

### PyPI — el repositorio de paquetes

Todo lo que instala pip viene de **PyPI** (Python Package Index): <https://pypi.org> — más de 500,000 paquetes.

| Librería | Para qué sirve |
| --- | --- |
| `requests` | Hacer peticiones HTTP |
| `rich` | Texto con colores y formato en terminal |
| `pandas` | Análisis de datos |
| `flask` | Crear aplicaciones web |
| `fastapi` | Crear APIs modernas |
| `pillow` | Manipular imágenes |

### Comandos esenciales

| Comando | Qué hace |
| --- | --- |
| `pip install requests` | Instala un paquete |
| `pip install requests==2.31.0` | Instala una versión específica (útil para igualar la del equipo o un tutorial) |
| `pip uninstall requests` | Desinstala (pide confirmación) |
| `pip list` | Lista paquetes instalados con sus versiones |
| `pip freeze` | Igual que `list` pero en formato `paquete==versión`, listo para `requirements.txt` |
| `pip install -r requirements.txt` | Instala todo lo listado en el archivo |

---

## 2. ¿Qué es un entorno virtual?

Problema: el **Proyecto A** necesita `requests 2.28` y el **Proyecto B** `requests 2.31`. Con un solo Python del sistema no puedes tener las dos versiones a la vez.

Solución: un **entorno virtual** = una copia aislada de Python para cada proyecto, con sus propias librerías y versiones.
Analogía: cajas de herramientas separadas — la del carpintero y la del electricista no se mezclan.

### Crear y usar un entorno virtual

```bash
# 1. Crear (el segundo "venv" es el nombre de la carpeta; por convención venv o .venv)
python -m venv venv

# 2. Activar
source venv/bin/activate        # Mac / Linux
venv\Scripts\activate           # Windows (cmd)
.\venv\Scripts\Activate.ps1     # Windows (PowerShell)
source venv/Scripts/activate    # Windows (Git Bash)

# 3. Instalar librerías (solo quedan dentro del venv)
pip install requests rich

# 4. Guardar dependencias
pip freeze > requirements.txt

# 5. Desactivar
deactivate
```

Con el entorno activo verás `(venv)` al inicio de la terminal. Eso confirma que `pip install` instala **dentro** del entorno, no en el Python del sistema.

---

## 3. requirements.txt

Archivo de texto estándar con las dependencias exactas del proyecto:

```text
requests==2.31.0
rich==13.7.0
certifi==2024.2.2
charset-normalizer==3.3.2
```

**Flujo para compartir un proyecto:**

1. Desarrollas el proyecto con sus librerías.
2. `pip freeze > requirements.txt`
3. Compartes el código + `requirements.txt` (**NO** la carpeta `venv/`).
4. La otra persona crea su propio venv y ejecuta `pip install -r requirements.txt`.

---

## 4. Flujo profesional completo

**Al iniciar un proyecto nuevo:**

```bash
mkdir mi_proyecto
cd mi_proyecto
python -m venv venv
venv\Scripts\activate             # Windows  (Mac/Linux: source venv/bin/activate)
pip install requests rich
pip freeze > requirements.txt
# crear main.py y programar...
deactivate
```

**Al descargar/clonar un proyecto existente:**

```bash
cd mi_proyecto
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

### .gitignore

Nunca subas `venv/` a Git (es pesada y cada persona genera la suya). Sube `requirements.txt`.

```text
venv/
```

---

## 5. Troubleshooting

**`pip: command not found` / `python not found`**
Python no está en el PATH, o hay que usar `pip3`/`python3` (común en Mac/Linux donde `python` puede ser Python 2).

```bash
pip3 install requests
python -m pip install requests
python3 -m pip install requests
```

**Se instaló en el Python del sistema y no en el venv**
Olvidaste activar el entorno. Revisa que aparezca `(venv)`; si no, actívalo y vuelve a instalar.

**PowerShell: `execution of scripts is disabled on this system`**

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Mac/Linux: `source: command not found`**
Usa bash o zsh (la terminal integrada de VS Code normalmente funciona bien).

**`Permission denied` al instalar**
Estás instalando en el Python del sistema sin permisos. La solución correcta es usar un venv (alternativa: `pip install --user requests`).

---

## 6. Ejercicios

### Ejercicio 1 — Tu primer entorno virtual (Fácil)

Crear una carpeta, un venv, activarlo, instalar `requests` y verificar con `pip list`.

```bash
mkdir practica_pip
cd practica_pip
python -m venv venv
venv\Scripts\activate
pip install requests
pip list
# certifi, charset-normalizer, idna, pip, requests, urllib3
```

> Nota: `requests` trae dependencias propias (`certifi`, `idna`, `urllib3`, `charset-normalizer`); por eso aparecen aunque solo instalaste una librería.

### Ejercicio 2 — requirements.txt (Fácil)

Generar `requirements.txt`, desactivar, crear `venv2`, activarlo e instalar desde el archivo.

```bash
pip freeze > requirements.txt
deactivate
python -m venv venv2
venv2\Scripts\activate
pip install -r requirements.txt
pip list
```

Resultado: [`requirements.txt`](requirements.txt).

### Ejercicio 3 — Usar la librería rich (Medio)

```bash
pip install rich
python demo_rich.py
```

Código: [`demo_rich.py`](demo_rich.py) — título en negrita, lista con colores y una tabla con `Console` y `Table`.

### Ejercicio 4 — Proyecto completo (Medio)

```bash
mkdir gestor_tareas
cd gestor_tareas
python -m venv venv
venv\Scripts\activate
pip install rich
pip freeze > requirements.txt
python main.py
```

Código: [`gestor_tareas/main.py`](gestor_tareas/main.py) — tabla de tareas con estado y prioridad formateados con `rich`.

---

## Resumen

- **pip** instala librerías: `pip install nombre`.
- **PyPI** (pypi.org) es el repositorio con +500,000 paquetes.
- Comandos clave: `pip install`, `pip uninstall`, `pip list`, `pip freeze`.
- Un **venv** es una copia aislada de Python por proyecto: `python -m venv venv` + activar.
- **requirements.txt**: se genera con `pip freeze > requirements.txt` y se instala con `pip install -r requirements.txt`.
- Nunca subas `venv/` a Git; sube `requirements.txt`.
- Flujo: crear proyecto → crear venv → activar → instalar → guardar requirements → codificar.

## Recursos adicionales

- [Python Docs — venv](https://docs.python.org/3/library/venv.html)
- [Python Docs — pip](https://pip.pypa.io/en/stable/user_guide/)
- [PyPI](https://pypi.org)
- [Real Python — Virtual Environments](https://realpython.com/python-virtual-environments-a-primer/)
- [Real Python — What is pip?](https://realpython.com/what-is-pip/)

**Próxima cápsula:** `math` y `random` — módulos estándar para cálculos matemáticos y valores aleatorios.
