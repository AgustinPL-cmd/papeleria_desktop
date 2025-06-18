import flet as ft

from papeleria_app.repositorios.producto_repo import producto_popular_semana_actual
from papeleria_app.repositorios.usuario_repo import ventas_empleado_semana
from papeleria_app.ui.components.barChart_productos_populares import BarChartProductosPopulares
from papeleria_app.ui.components.header_empleado import header_empleado
from papeleria_app.ui.components.linear_chart_ventas_semana_actual import GraficaLinealVentas
from papeleria_app.ui.components.menu_lateral_encargado import menu_lateral_encargado
from papeleria_app.repositorios.ventas_repo import (
    ventas_semana_actual,
    ventas_semana_pasada,
    ventas_mes_actual,
    ventas_trimestre_actual
)
from papeleria_app.repositorios.producto_repo import (
    producto_popular_semana_actual,
    producto_popular_semana_pasada,
    producto_popular_mes_actual,
    producto_popular_trimestre_actual
)
from papeleria_app.ui.components.pieChartEmpleados import GraficaPieVentas


def admin_dashboard_view(page: ft.Page):
    dlg_usuario = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cargando..."),
        content=ft.Text("Espere un momento"),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: None)]
    )

    usuario_data = page.client_storage.get("usuario")
    user = usuario_data["user"]

    # Texto dinámico del título
    titulo_grafica_ventas = ft.Text("Ventas de esta semana", size=20, weight=ft.FontWeight.BOLD, color="#090040")
    titulo_grafica_productos = ft.Text("Productos", size=20, weight=ft.FontWeight.BOLD, color="#090040")
    titulo_grafica_empleados = ft.Text("Ventas por Empleado (semana)", size=20, weight=ft.FontWeight.BOLD, color="#090040")



    # Datos iniciales
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
            ft.ElevatedButton("Esta semana", on_click=actualizar_grafica_ventas("Ventas de esta semana", ventas_semana_actual, "dia")),
            ft.ElevatedButton("Semana pasada", on_click=actualizar_grafica_ventas("Ventas de la semana pasada", ventas_semana_pasada, "dia")),
            ft.ElevatedButton("Este mes", on_click=actualizar_grafica_ventas("Ventas de este mes", ventas_mes_actual, "semana")),
            ft.ElevatedButton("Trimestre", on_click=actualizar_grafica_ventas("Ventas del trimestre", ventas_trimestre_actual, "mes")),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=10
    )

    productos_populares = producto_popular_semana_actual()
    grafica_productos = BarChartProductosPopulares("Semana", productos_populares)
    container_grafica_productos = ft.Container(
        content=grafica_productos.construir_grafica(),
        padding=20,
        bgcolor="#ffffff",
        border_radius=20,
        clip_behavior=ft.ClipBehavior.NONE,
        expand=True,
        width=550
    )

    # Función para actualizar la gráfica y el título
    def actualizar_grafica_productos(nombre, consulta_funcion):
        def handler(e):
            titulo_grafica_productos.value = nombre
            nuevos_datos = consulta_funcion()
            nueva_grafica = BarChartProductosPopulares(titulo=nombre, datos=nuevos_datos)
            container_grafica_productos.content = nueva_grafica.construir_grafica()
            page.update()

        return handler

    # Botones de selección
    botones_grafica_productos = ft.Row(
        controls=[
            titulo_grafica_productos,
            ft.ElevatedButton("Esta semana",
                              on_click=actualizar_grafica_productos("Productos", producto_popular_semana_actual)),
            ft.ElevatedButton("Semana pasada",
                              on_click=actualizar_grafica_productos("Productos", producto_popular_semana_pasada)),
            ft.ElevatedButton("Este mes",
                              on_click=actualizar_grafica_productos("Productos", producto_popular_mes_actual)),
            ft.ElevatedButton("Trimestre",
                              on_click=actualizar_grafica_productos("Productos", producto_popular_trimestre_actual)),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        spacing=10
    )

    column_productos = ft.Column(
        controls=[
            botones_grafica_productos,
            container_grafica_productos
        ]
    )

    datos_empleados = ventas_empleado_semana()

    # Crear la gráfica
    grafica_pie = GraficaPieVentas(datos_empleados, "Ventas por empleado")
    chart = grafica_pie.crear()

    # Agregar a tu interfaz
    contenedor_empleados = ft.Container(
        content=chart,
        padding=20,
        bgcolor=ft.Colors.WHITE,
        border_radius=20,
        height=400,
        width=550
    )

    column_empleados = ft.Column(
        controls=[
            titulo_grafica_empleados,
            contenedor_empleados
        ]
    )


    header = header_empleado(user, page, dlg_usuario)
    menu_lateral = menu_lateral_encargado()

    contenido_principal = ft.Container(
        content=ft.Column(
            controls=[
                botones_grafica_ventas,
                container_grafica_venta,
                ft.Row(
                    controls=[
                        column_productos,
                        column_empleados,

                    ]
                )
            ],
            spacing=20,
            scroll=ft.ScrollMode.AUTO,  # o ScrollMode.ALWAYS
            expand=True
        ),
        padding=30,

    )

    layout = ft.Row(
        controls=[
            menu_lateral,
            ft.Column(
                controls=[header, contenido_principal],
                expand=True,
                scroll=ft.ScrollMode.ALWAYS
            )
        ],
        expand=True,
        spacing=5
    )

    return ft.View(
        route="/admin_dashboard_view",
        controls=[layout, dlg_usuario],
        bgcolor="#f2f7fb",
        padding=0,
        appbar=None
    )



