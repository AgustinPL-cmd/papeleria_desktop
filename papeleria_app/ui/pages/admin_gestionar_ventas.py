import flet as ft
from datetime import datetime, timedelta
from papeleria_app.repositorios.ventas_repo import (
    ventas_semana_actual,
    ventas_semana_pasada,
    ventas_mes_actual,
    ventas_trimestre_actual,
    consultar_ventas_por_fecha_empleado, consultar_ventas_por_fecha
)
from papeleria_app.ui.components.alert_venta_detalles import alert_venta_detalles
from papeleria_app.ui.components.header_empleado import header_empleado
from papeleria_app.ui.components.menu_lateral_encargado import menu_lateral_encargado
from papeleria_app.ui.components.linear_chart_ventas_semana_actual import GraficaLinealVentas


def formatear_fecha_relativa(fecha_venta: datetime) -> str:
    hoy = datetime.now().date()
    fecha_solo_dia = fecha_venta.date()

    if fecha_solo_dia == hoy:
        return "Hoy"
    elif fecha_solo_dia == hoy - timedelta(days=1):
        return "Ayer"
    else:
        return fecha_venta.strftime("%d-%b-%Y")


def admin_gestionar_venta(page: ft.Page):
    # Configuración de diálogos
    dlg_usuario = ft.AlertDialog(
        modal=True,
        title=ft.Text("Cargando..."),
        content=ft.Text("Espere un momento"),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: None)]
    )

    dlg_venta = ft.AlertDialog(
        modal=True,
        title=ft.Text("Detalle de venta"),
        content=ft.Text("Espere un momento..."),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: None)]
    )
    page.dialog = dlg_venta

    # Funciones para manejar diálogos
    def mostrar_dialogo(venta, e=None):
        dlg_detalle = alert_venta_detalles(page, venta)
        dlg_venta.title = dlg_detalle.title
        dlg_venta.content = dlg_detalle.content
        dlg_venta.bgcolor = dlg_detalle.bgcolor
        dlg_venta.actions = [ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo())]
        dlg_venta.open = True
        page.update()

    def cerrar_dialogo():
        dlg_venta.open = False
        page.update()

    # Obtener datos del usuario
    usuario_data = page.client_storage.get("usuario")
    user = usuario_data["user"]
    id_user = user["id_usuario"]

    # Componentes UI
    header = header_empleado(user, page, dlg_usuario)
    menu_lateral = menu_lateral_encargado()

    # Configuración de la gráfica lineal
    titulo_grafica_ventas = ft.Text("Ventas de esta semana", size=20, weight=ft.FontWeight.BOLD, color="#090040")
    datos = ventas_semana_actual()
    grafica_ventas = GraficaLinealVentas(titulo="Ventas Semana Actual", datos=datos, tipo_x="dia", height=300)

    container_grafica_venta = ft.Container(
        content=grafica_ventas.construir_grafica(),
        padding=20,
        bgcolor="#ffffff",
        border_radius=20,
        clip_behavior=ft.ClipBehavior.NONE,
        expand=True
    )

    # Función para actualizar la gráfica
    def actualizar_grafica_ventas(nombre, consulta_funcion, tipo_x):
        def handler(e):
            titulo_grafica_ventas.value = nombre
            nuevos_datos = consulta_funcion()
            nueva_grafica = GraficaLinealVentas(titulo=nombre, datos=nuevos_datos, tipo_x=tipo_x, height=300)
            container_grafica_venta.content = nueva_grafica.construir_grafica()
            page.update()

        return handler

    # Botones de selección de periodo
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

    # Función para filtrar ventas por fecha y mostrarlo en la tabla
    def filtar_by_fecha(e=None, fecha_valor=None):
        fecha = fecha_valor if fecha_valor else e.control.value
        ventas = consultar_ventas_por_fecha(fecha)
        tabla_ventas.rows.clear()

        for v in ventas:
            fecha_venta, num_venta, total, ganancia = v

            # Función auxiliar para capturar correctamente el valor de v
            def crear_boton(venta_actual):
                return ft.IconButton(
                    icon=ft.Icons.REMOVE_RED_EYE,
                    on_click=lambda e: mostrar_dialogo(venta_actual),
                    tooltip="Ver detalles",
                    data=venta_actual
                )

            tabla_ventas.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(formatear_fecha_relativa(fecha_venta), color="black")),
                        ft.DataCell(ft.Text(str(num_venta), color="black")),
                        ft.DataCell(ft.Text(f"${total:.2f}", color="black")),
                        ft.DataCell(ft.Text(f"${ganancia:.2f}", color="black")),
                        ft.DataCell(crear_boton(v))  # Usar la función auxiliar
                    ]
                )
            )

        if e is not None:
            tabla_ventas.update()


    filtro_fecha_dropdown = ft.Dropdown(
        label="Filtrar por fecha",
        options=[
            ft.dropdown.Option("hoy", "Hoy"),
            ft.dropdown.Option("ayer", "Ayer"),
            ft.dropdown.Option("semana", "Esta semana"),
            ft.dropdown.Option("mes", "Este mes"),
        ],
        value="hoy",
        width=200,
        label_style=ft.TextStyle(color="black", size=18, weight=ft.FontWeight.BOLD),
        color="black",
        on_change=filtar_by_fecha,

    )

    # Tabla ventas
    tabla_ventas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Fecha", color="white")),
            ft.DataColumn(ft.Text("Número de Venta", color="white")),
            ft.DataColumn(ft.Text("Total", color="white")),
            ft.DataColumn(ft.Text("Ganancia", color="white")),
            ft.DataColumn(ft.Text("Detalles", color="white"))
        ],
        rows=[],
        heading_row_color="#8e7db4",

    )

    # Contenedor para la tabla con scroll
    tabla_container = ft.Container(
        content=ft.Column(
            controls=[filtro_fecha_dropdown, tabla_ventas],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True
        ),
        expand=True,
        height=500
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
                text="Historial de Ventas",
                content=ft.Container(
                    content=tabla_container,
                    padding=20
                ),

            )
        ],
        expand=True
    )

    # Layout principal
    layout = ft.Row(
        controls=[
            menu_lateral,
            ft.Column(
                controls=[
                    header,
                    ft.Container(
                        content=tabs,
                        expand=True,
                        padding=ft.padding.only(right=20, top=10)
                    )
                ],
                expand=True,
                spacing=0
            )
        ],
        spacing=5,
        expand=True
    )



    return ft.View(
        route="/admin_gestionar_venta",
        controls=[layout, dlg_usuario, dlg_venta],
        bgcolor="#f2f7fb",
        padding=0,
        appbar=None
    )