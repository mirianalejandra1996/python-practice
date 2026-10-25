# main.py
from rich.console import Console
from rich.table import Table

consola = Console()

tareas = [
    {"titulo": "Estudiar pip y venv", "estado": "completada", "prioridad": "alta"},
    {"titulo": "Practicar módulos estándar", "estado": "en progreso", "prioridad": "alta"},
    {"titulo": "Leer PEP 8", "estado": "pendiente", "prioridad": "media"},
    {"titulo": "Hacer entrega semanal", "estado": "pendiente", "prioridad": "alta"},
]

tabla = Table(title="Mis Tareas - Semana 8")
tabla.add_column("Tarea", style="cyan", min_width=30)
tabla.add_column("Estado", justify="center")
tabla.add_column("Prioridad", justify="center")

for tarea in tareas:
    estado = tarea["estado"]
    if estado == "completada":
        estado_fmt = "[green]✓ Completada[/green]"
    elif estado == "en progreso":
        estado_fmt = "[yellow]⏳ En progreso[/yellow]"
    else:
        estado_fmt = "[red]○ Pendiente[/red]"

    prioridad = tarea["prioridad"]
    if prioridad == "alta":
        prioridad_fmt = "[bold red]Alta[/bold red]"
    else:
        prioridad_fmt = "[yellow]Media[/yellow]"

    tabla.add_row(tarea["titulo"], estado_fmt, prioridad_fmt)

consola.print()
consola.print(tabla)
consola.print(f"\n[bold]Total:[/bold] {len(tareas)} tareas")