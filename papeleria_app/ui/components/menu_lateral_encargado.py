import flet as ft

def menu_lateral_encargado():
    # Funciones de redireccionamiento
    def go_empleado(e, button):
        if button == "INICIO":
            e.page.go("/admin_dashboard_view")
        elif button == "REGISTRAR VENTA":
            e.page.go("/empladoRegistrarVenta")
        elif button == "GESTIONAR PRODUCTOS":
            e.page.go("/adminGestionarProductos")
        elif button == "GESTIONAR EMPLEADO":
            e.page.go("/adminGestionarEmpleados")
        elif button == "GESTIONAR VENTAS":
            e.page.go("/admin_gestionar_venta")
        elif button == "REGISTRAR COMPRA":
            e.page.go("/admin_registrar_compra")
        else:
            e.page.go("/empleadoRegistrarSugerencia")

    # Botones del menú lateral
    home_button = ft.IconButton(icon=ft.Icons.HOME, bgcolor="#8e7db4", icon_color="#cdf3ff", hover_color="#231f20",
                                icon_size=32, tooltip="INICIO", on_click=lambda e: go_empleado(e, "INICIO"))

    empleados_button = ft.IconButton(icon=ft.Icons.SUPERVISED_USER_CIRCLE, bgcolor="#8e7db4", icon_color="#cdf3ff",
                                  hover_color="#231f20", icon_size=32, tooltip="GESTIONAR EMPLEADO",
                                  on_click=lambda e: go_empleado(e, "GESTIONAR EMPLEADO"))

    productos_button = ft.IconButton(icon=ft.Icons.INVENTORY, bgcolor="#8e7db4", icon_color="#cdf3ff",
                                   hover_color="#231f20", icon_size=32, tooltip="GESTIONAR PRODUCTOS",
                                   on_click=lambda e: go_empleado(e, "GESTIONAR PRODUCTOS"))

    ventas_button = ft.IconButton(icon=ft.Icons.ATTACH_MONEY, bgcolor="#8e7db4", icon_color="#cdf3ff",
                                     hover_color="#231f20", icon_size=32, tooltip="GESTIONAR VENTAS",
                                     on_click=lambda e: go_empleado(e, "GESTIONAR VENTAS"))

    alertas_button = ft.IconButton(icon=ft.Icons.WARNING_AMBER_ROUNDED, bgcolor="#8e7db4", icon_color="#cdf3ff",
                                  hover_color="#231f20", icon_size=32, tooltip="ALERTAS",
                                  on_click=lambda e: go_empleado(e, "REGISTRAR COMENTARIO"))

    compra_button = ft.IconButton(icon=ft.Icons.SHOPPING_CART, bgcolor="#8e7db4", icon_color="#cdf3ff",
                                   hover_color="#231f20", icon_size=32, tooltip="REGISTRAR COMPRA",
                                   on_click=lambda e: go_empleado(e, "REGISTRAR COMPRA"))


    menu_lateral = ft.Container(
        content=ft.Column(
            controls=[home_button, empleados_button, productos_button, ventas_button, alertas_button, compra_button ],
            spacing=20,
            alignment=ft.MainAxisAlignment.START,
            expand=True
        ),
        bgcolor="#8e7db4",
        width=90,
        padding=20,
    )

    return menu_lateral