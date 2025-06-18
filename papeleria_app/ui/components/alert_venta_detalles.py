import flet as ft
from datetime import datetime
from papeleria_app.repositorios.ventas_repo import obtener_venta_by_numVenta


def alert_venta_detalles(page, venta):
    try:
        if len(venta) == 3:
            fecha_venta = venta[0]
            num_venta = venta[1]
            total = venta[2]
        else:
            fecha_venta, num_venta, total, ganancia = venta


        # Obtener detalles de la venta
        detalles = obtener_venta_by_numVenta(num_venta)

        # Construir contenido del diálogo
        content_list = [
            ft.Text(f"📅 Fecha: {fecha_venta.strftime('%d/%m/%Y %H:%M')}", size=16),
            ft.Text(f"🛒 Venta #: {num_venta}", size=16),
            ft.Divider()
        ]

        # Verificar si hay detalles válidos
        if detalles and not isinstance(detalles, tuple):
            content_list.append(ft.Text("📦 Productos:", weight=ft.FontWeight.BOLD, size=14))

            for detalle in detalles:
                cantidad = detalle[1]
                nombre = detalle[3]
                precio_unitario = detalle[4]
                subtotal = detalle[2]

                content_list.append(
                    ft.Text(
                        f"→ ({cantidad}) {nombre} (Precio Unitario: ${precio_unitario:.2f}): ${subtotal:.2f}",
                        size=14
                    )
                )

            content_list.extend([
                ft.Divider(),
                ft.Text(f"Total de la venta: ${total:.2f}",
                        size=16,
                        weight=ft.FontWeight.BOLD,
                        color=ft.Colors.GREEN)
            ])
        else:
            content_list.append(ft.Text("No se encontraron detalles de productos", color=ft.Colors.RED))

        # Crear diálogo
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Detalles de Venta", text_align=ft.TextAlign.CENTER),
            content=ft.Column(content_list, scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo(page))
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            shape=ft.RoundedRectangleBorder(radius=10),
            bgcolor="#0B1D51"
        )

        return dlg

    except Exception as ex:
        print(f"Error creando diálogo: {ex}")
        return ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(f"No se pudieron cargar los detalles: {str(ex)}"),
            actions=[ft.TextButton("Cerrar")]
        )


def cerrar_dialogo(page):
    if page.dialog:
        page.dialog.open = False
        page.update()