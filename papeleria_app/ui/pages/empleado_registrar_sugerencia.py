import flet as ft

from papeleria_app.ui.components.header_empleado import header_empleado
from papeleria_app.models.sugerencia_cliente import SugerenciaCliente

from papeleria_app.repositorios.sugerencia_repo import insert_sugerencia
from papeleria_app.ui.components.menu_lateral_empleado import menu_lateral_empleado


def registro_sugerencia_view(page: ft.Page):
    usuario_data = page.client_storage.get("usuario")
    user = usuario_data["user"]
    user_id = user["id_usuario"]

    dlg_venta = ft.AlertDialog(
        modal=True,
        title=ft.Text("Detalle de venta"),
        content=ft.Text("Espere un momento..."),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: None)]
    )

    # Header y menú lateral
    header = header_empleado(user,page, dlg_venta)
    menu_lateral = menu_lateral_empleado()

    # Entradas
    strong_label_style = ft.TextStyle(color=ft.Colors.BLACK, weight=ft.FontWeight.BOLD)
    strong_text_color = ft.Colors.BLACK
    focus_border_color = ft.Colors.BLUE_400  # o el que prefieras

    producto_input = ft.TextField(
        label="PRODUCTO SUGERIDO",
        width=300,
        label_style=strong_label_style,
        color=strong_text_color,
        border_color=strong_text_color,
        focused_border_color=focus_border_color
    )

    comentario_input = ft.TextField(
        label="COMENTARIO",
        multiline=True,
        max_lines=3,
        width=300,
        label_style=strong_label_style,
        color=strong_text_color,
        border_color=strong_text_color,
        focused_border_color=focus_border_color
    )

    mensaje = ft.Text("", color="red", size=14, text_align=ft.TextAlign.CENTER)

    def registrar(e):
        if producto_input.value.strip() != "" and comentario_input.value.strip() != "":
            sugerencia = SugerenciaCliente(
                producto_sugerido=producto_input.value,
                comentario=comentario_input.value
            )
            exito, msj = insert_sugerencia(sugerencia)
            mensaje.value = msj
            mensaje.color = "green" if exito else "red"
            page.update()
        else:
            mensaje.value = "Los campos no pueden estar vacios"
            mensaje.color = "red"
            page.update()

    def limpiar(e):
        producto_input.value = ""
        comentario_input.value = ""
        mensaje.value = ""
        page.update()

    form_container = ft.Container(
        width=500,
        height=500,
        padding=30,
        border_radius=20,
        bgcolor="#d8d5eb",
        alignment=ft.alignment.center,
        shadow=ft.BoxShadow(
            blur_radius=25,
            color="#aaa",
            spread_radius=1,
            offset=ft.Offset(3, 6)
        ),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[
                ft.Text("SUGERENCIAS DE CLIENTES", size=22, weight=ft.FontWeight.BOLD, color="black"),
                producto_input,
                comentario_input,
                mensaje,
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                    controls=[
                        ft.Container(
                            content=ft.ElevatedButton("GUARDAR", on_click=registrar),
                            width=140,
                            border_radius=30,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=["#cfd8dc", "#90a4ae"]
                            ),
                            shadow=ft.BoxShadow(blur_radius=10, color="#888")
                        ),
                        ft.Container(
                            content=ft.ElevatedButton("LIMPIAR", on_click=limpiar),
                            width=140,
                            border_radius=30,
                            gradient=ft.LinearGradient(
                                begin=ft.alignment.top_left,
                                end=ft.alignment.bottom_right,
                                colors=["#cfd8dc", "#90a4ae"]
                            ),
                            shadow=ft.BoxShadow(blur_radius=10, color="#888")
                        )
                    ]
                )
            ]
        )
    )

    layout = ft.Row(
        expand=True,
        spacing=0,
        controls=[
            menu_lateral,
            ft.Column(
                expand=True,
                spacing=0,
                controls=[
                    header,
                    ft.Container(
                        expand=True,
                        bgcolor="#cdf3ff",
                        alignment=ft.alignment.center,
                        padding=0,
                        margin=0,
                        content=form_container
                    )
                ]
            )
        ]
    )

    return ft.View(
        route="/empleadoRegistrarSugerencia",
        controls=[layout, dlg_venta],
        bgcolor="#cdf3ff",
        padding=0,
        appbar=None,
    )


