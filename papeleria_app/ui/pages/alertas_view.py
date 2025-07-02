import flet as ft
from datetime import datetime
from papeleria_app.repositorios.alertas_repo import obtener_alertas_inventario

def alertas_view(datos_alertas):
    def formatear_fecha(fecha):
        if isinstance(fecha, datetime):
            return fecha.strftime("%Y-%m-%d")
        return str(fecha)

    # Título principal
    titulo = ft.Text(
        "VISUALIZACIÓN DE ALERTAS",
        color="black",
        size=20,
        weight="bold",
        text_align="center"
    )

    # Subtítulo con ícono
    subtitulo = ft.Row(
        [
            ft.Icon(name=ft.Icons.WARNING_AMBER_ROUNDED, color="orange", size=30),
            ft.Text("ALERTA: INVENTARIO BAJO", color="black", size=18, weight="bold")
        ],
        alignment="center"
    )

    # Encabezados de tabla
    encabezados = ft.Row(
        controls=[
            ft.Container(ft.Text("Producto", weight="bold", color="black"), bgcolor="#39D978", padding=10, expand=True),
            ft.Container(ft.Text("Stock actual", weight="bold", color="black"), bgcolor="#39D978", padding=10, expand=True),
            ft.Container(ft.Text("Stock mínimo", weight="bold", color="black"), bgcolor="#39D978", padding=10, expand=True),
            ft.Container(ft.Text("Estado", weight="bold", color="black"), bgcolor="#39D978", padding=10, expand=True),
            ft.Container(ft.Text("Fecha Alerta", weight="bold", color="black"), bgcolor="#39D978", padding=10, expand=True)
        ],
        alignment="center"
    )

    # Filas de la tabla desde la BD
    filas_tabla = []
    for fila in datos_alertas:
        fila_row = ft.Row(
            controls=[
                ft.Container(ft.Text(fila["nombre_producto"]), bgcolor="#E8FFD8", padding=10, expand=True),
                ft.Container(ft.Text(f'{fila["stock_actual"]} unidades'), bgcolor="#E8FFD8", padding=10, expand=True),
                ft.Container(ft.Text(f'{fila["stock_minimo"]} unidades'), bgcolor="#E8FFD8", padding=10, expand=True),
                ft.Container(ft.Text(fila["estado"].upper()), bgcolor="#E8FFD8", padding=10, expand=True),
                ft.Container(ft.Text(formatear_fecha(fila["fecha_alerta"])), bgcolor="#E8FFD8", padding=10, expand=True)
            ],
            alignment="center"
        )
        filas_tabla.append(fila_row)

    # Tarjeta visual
    tarjeta_alerta = ft.Container(
        content=ft.Column(
            [
                subtitulo,
                encabezados,
                *filas_tabla
            ],
            spacing=5
        ),
        padding=20,
        bgcolor="#E5DDF4",
        border_radius=10,
        width=700
    )

    # Vista final
    return ft.View(
        route="/alertas",
        controls=[
            ft.Column(
                [
                    titulo,
                    tarjeta_alerta
                ],
                spacing=20
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        bgcolor="#CCF1FF"
    )


# Solo para pruebas (puedes borrar este bloque después)

