import flet as ft
from papeleria_app.repositorios.producto_repo import buscar_productos_por_nombre, eliminar_o_suspender_producto

def eliminar_producto_view(page: ft.Page):

    busqueda_input = ft.TextField(
        label="Buscar producto",
        hint_text="Escribe el nombre del producto",
        on_change=lambda e: actualizar_lista(busqueda_input.value),
        autofocus=True,
        expand=True
    )

    resultado_columna = ft.Column()

    def actualizar_lista(texto):
        productos = buscar_productos_por_nombre(texto)
        resultado_columna.controls.clear()

        for producto in productos:
            fila = ft.Row(
                [
                    ft.Column([
                        ft.Text(f"{producto.nombre}"),
                        ft.Text(f"Estado: {getattr(producto, 'estado', 'activo')}", size=12, italic=True, color=ft.colors.GREY)
                    ], expand=True),
                    ft.IconButton(
                        icon=ft.icons.CANCEL,
                        icon_color=ft.colors.WHITE,
                        bgcolor=ft.colors.RED,
                        tooltip="Eliminar/Suspender",
                        on_click=lambda e, p=producto: eliminar_producto(p)
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
            resultado_columna.controls.append(fila)

        page.update()

    def eliminar_producto(producto):
        confirmado = ft.AlertDialog(
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Seguro que deseas eliminar o suspender '{producto.nombre}'?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.dialog.close()),
                ft.TextButton("Aceptar", on_click=lambda e: confirmar_eliminacion(producto))
            ],
            actions_alignment=ft.MainAxisAlignment.END
        )
        page.dialog = confirmado
        confirmado.open = True
        page.update()

    def confirmar_eliminacion(producto):
        success, mensaje = eliminar_o_suspender_producto(producto.id_producto)
        page.dialog.open = False
        page.snack_bar = ft.SnackBar(ft.Text(mensaje))
        page.snack_bar.open = True
        actualizar_lista(busqueda_input.value)

    return ft.View(
        route="/eliminar_producto",
        controls=[
            ft.Column([
                ft.Text("Eliminar productos", size=24, weight=ft.FontWeight.BOLD),
                busqueda_input,
                resultado_columna
            ])
        ],
        padding=20
    )


def main(page: ft.Page):
    page.title = "Eliminar producto"
    page.bgcolor = "#cdf3ff"
    page.views.clear()
    page.views.append(eliminar_producto_view(page))
    page.update()



ft.app(target=main)
