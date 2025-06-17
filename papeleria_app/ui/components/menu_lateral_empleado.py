import flet as ft

def menu_lateral_empleado():
    # Funciones de redireccionamiento
    def go_empleado(e, button):
        if button == "INICIO":
            e.page.go("/empleado_dashboard_view")
        elif button == "REGISTRAR VENTA":
            e.page.go("/empladoRegistrarVenta")
        else:
            e.page.go("/empleado_registrar_comentario")

    # Botones del menú lateral
    home_button = ft.IconButton(icon=ft.Icons.HOME, bgcolor="#8e7db4", icon_color="#cdf3ff", hover_color="#231f20",
                                icon_size=32, tooltip="INICIO", on_click=lambda e: go_empleado(e, "INICIO"))
    vender_button = ft.IconButton(icon=ft.Icons.ATTACH_MONEY, bgcolor="#8e7db4", icon_color="#cdf3ff",
                                  hover_color="#231f20", icon_size=32, tooltip="REGISTRAR VENTA",
                                  on_click=lambda e: go_empleado(e, "REGISTRAR VENTA"))
    comment_button = ft.IconButton(icon=ft.Icons.QUESTION_ANSWER, bgcolor="#8e7db4", icon_color="#cdf3ff",
                                   hover_color="#231f20", icon_size=32, tooltip="REGISTRAR SUGERENCIA",
                                   on_click=lambda e: go_empleado(e, "REGISTRAR COMENTARIO"))

    menu_lateral = ft.Container(
        content=ft.Column(
            controls=[home_button, vender_button, comment_button],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            expand=True
        ),
        bgcolor="#8e7db4",
        width=90,
        padding=20,
    )

    return menu_lateral