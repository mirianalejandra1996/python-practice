# demo_rich.py
from rich.console import Console
from rich.table import Table

consola = Console()

consola.print("[bold magenta]¡Bienvenido a Rich![/bold magenta]")
consola.print()

consola.print("[green]✓[/green] Python instalado")
consola.print("[green]✓[/green] Entorno virtual activo")
consola.print("[green]✓[/green] Rich funcionando")
consola.print()

tabla = Table(title="Mis Librerías Favoritas")
tabla.add_column("Librería", style="cyan")
tabla.add_column("Uso", style="green")
tabla.add_row("requests", "Peticiones HTTP")
tabla.add_row("rich", "Texto formateado en terminal")
tabla.add_row("pandas", "Análisis de datos")

consola.print(tabla)