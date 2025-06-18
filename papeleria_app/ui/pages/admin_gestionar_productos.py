import flet as ft
from papeleria_app.ui.components.header_empleado import header_empleado
from papeleria_app.ui.components.linear_chart_ventas_semana_actual import GraficaLinealVentas
from papeleria_app.ui.components.menu_lateral_encargado import menu_lateral_encargado
from papeleria_app.repositorios.ventas_repo import (
    ventas_semana_actual,
    ventas_semana_pasada,
    ventas_mes_actual,
    ventas_trimestre_actual
)
from papeleria_app.ui.components.productosTable import ProductosTable


def admin_gestionar_productos(page: ft.Page):
    dlg_usuario = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cargando..."),
        content=ft.Text("Espere un momento"),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: None)]
    )

    usuario_data = page.client_storage.get("usuario")
    user = usuario_data["user"]

    header = header_empleado(user, page, dlg_usuario)
    menu_lateral = menu_lateral_encargado()
    tabla_productos = ProductosTable(page)

    titulo_grafica_ventas = ft.Text("Ventas de esta semana", size=20, weight=ft.FontWeight.BOLD, color="#090040")

    # Gráfica ventas
    datos = ventas_semana_actual()
    grafica_ventas = GraficaLinealVentas(titulo="Ventas Semana Actual", datos=datos, tipo_x="dia")
    container_grafica_venta = ft.Container(
        content=grafica_ventas.construir_grafica(),
        padding=20,
        bgcolor="#ffffff",
        border_radius=20,
        clip_behavior=ft.ClipBehavior.NONE,
        expand=True
    )

    # Función para actualizar la gráfica y el título
    def actualizar_grafica_ventas(nombre, consulta_funcion, tipo_x):
        def handler(e):
            titulo_grafica_ventas.value = nombre
            nuevos_datos = consulta_funcion()
            nueva_grafica = GraficaLinealVentas(titulo=nombre, datos=nuevos_datos, tipo_x=tipo_x)
            container_grafica_venta.content = nueva_grafica.construir_grafica()
            page.update()

        return handler

    # Botones de selección
    botones_grafica_ventas = ft.Row(
        controls=[
            titulo_grafica_ventas,
            ft.ElevatedButton("Esta semana",
                              on_click=actualizar_grafica_ventas("Ventas de esta semana", ventas_semana_actual, "dia")),
            ft.ElevatedButton("Semana pasada",
                              on_click=actualizar_grafica_ventas("Ventas de la semana pasada", ventas_semana_pasada,
                                                                 "dia")),
            ft.ElevatedButton("Este mes",
                              on_click=actualizar_grafica_ventas("Ventas de este mes", ventas_mes_actual, "semana")),
            ft.ElevatedButton("Trimestre",
                              on_click=actualizar_grafica_ventas("Ventas del trimestre", ventas_trimestre_actual,
                                                                 "mes")),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=10,
        wrap=True
    )

    # Contenido principal organizado en pestañas
    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(
                text="Dashboard",
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            botones_grafica_ventas,
                            container_grafica_venta,
                        ],
                        spacing=20,
                        expand=True
                    ),
                    padding=20
                )
            ),
            ft.Tab(
                text="Inventario",
                content=ft.Column(
                    controls=tabla_productos.get_controls(),
                    spacing=20,
                    expand=True,
                    scroll=ft.ScrollMode.AUTO
                ),

            )
        ],
        expand=True,
        label_color= "#090040",
        unselected_label_color="#03A6A1"
    )

    contenido_principal = ft.Container(
        content=tabs,
        padding=ft.padding.only(top=20),
        expand=True
    )

    layout = ft.Row(
        controls=[
            menu_lateral,
            ft.Container(
                ft.Column(
                    controls=[
                        header,
                        contenido_principal
                    ]
                ),
                expand=True
            ),

        ],
        spacing=5,
        expand=True
    )

    return ft.View(
        route="/adminGestionarProductos",
        controls=[layout, dlg_usuario],
        bgcolor="#f2f7fb",
        padding=0,
        appbar=None
    )


