import flet as ft
from flet.core import row
from flet.core.datatable import DataRow

from papeleria_app.repositorios.usuario_repo import ventas_empleado_semana_actual, ventas_empleado_semana, \
    get_empleados, get_empleado_by_id
from papeleria_app.repositorios.ventas_repo import ventas_semana_actual, ventas_semana_pasada, \
    consultar_ventas_por_fecha_empleado
from papeleria_app.services.empleados_service import edit_empleado
from papeleria_app.ui.components.header_empleado import header_empleado
from papeleria_app.ui.components.linear_chart_empleados_ventas import GraficaLinealPorEmpleado
from papeleria_app.ui.components.menu_lateral_encargado import menu_lateral_encargado
from papeleria_app.repositorios.usuario_repo import (
    ventas_empleado_semana_actual,
    ventas_empleado_semana_pasada,
    ventas_empleado_mes_actual,
    ventas_empleado_trimestre_actual
)
from papeleria_app.ui.components.pieChartEmpleados import GraficaPieVentas
from papeleria_app.ui.pages.alta_de_empleados_view import alta_empleado_view



def admin_gestionar_empleado(page):
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

    datos = ventas_empleado_semana_actual()

    titulo_grafica_empleados = ft.Text("No. de ventas por empleado", size=20, weight=ft.FontWeight.BOLD, color="#090040")


    linear_chart = GraficaLinealPorEmpleado(
        titulo="Ventas por Empleado",
        datos=datos,
        tipo_x="dia",  # puede ser 'dia', 'semana' o 'mes'
        tipo_valor="total_ventas"  # también puede ser 'total_ingresos' o 'ganancia_neta'
    ).construir_grafica()

    container_grafica_empleados = ft.Container(
        content=linear_chart,
        padding=20,
        bgcolor="#ffffff",
        border_radius=20,
        clip_behavior=ft.ClipBehavior.NONE,
        expand=True
    )

    #Tabla de empleados
    def crear_tabla_empleados():
        empleados =  get_empleados()
        if not empleados:
            return ft.Text("No hay usuarios existentes")

        columns = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Activo")),
            ft.DataColumn(ft.Text(""))
        ]

        rows = []

        for emp in empleados:
            activo_icon = ft.Icon(ft.Icons.CHECK_CIRCLE, color="green") if emp["activo"] else ft.Icon(ft.Icons.CANCEL, color="red")
            rows.append(
                DataRow(cells=[
                    ft.DataCell(ft.Text(str(emp["id_usuario"]))),
                    ft.DataCell(ft.Text(str(emp["nombre"]))),
                    ft.DataCell(activo_icon),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            on_click=lambda e, eid=emp["id_usuario"]: abrir_editor(eid)
                        )
                    ),
                ])

            )
        return ft.DataTable(columns=columns, rows=rows, border=ft.border.all(1, "lightgrey"))

    def abrir_editor(emp_id):
        empleado = get_empleado_by_id(emp_id)
        if not empleado:
            return

        nombre_field = ft.TextField(label="Nombre", value=empleado["nombre"])
        activo_switch = ft.Switch(value=bool(empleado["activo"]))

        def guardar(e):
            exito, msg = edit_empleado(emp_id, nombre_field.value, activo_switch.value)
            if exito:
                page.close(dialog)

                tabla_container.content = crear_tabla_empleados()
                page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor="green")
                page.snack_bar.open = True
            else:
                page.snack_bar = ft.SnackBar(content=ft.Text(msg), bgcolor="red")
                page.snack_bar.open = True
            page.update()

        dialog = ft.AlertDialog(
            title=ft.Text(f"Editar Empleado {empleado['nombre']}"),

            content=ft.Column([nombre_field, ft.Text("Activo"), activo_switch], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: page.close(dialog)),
                ft.ElevatedButton("Guardar", on_click=guardar)
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.open(dialog)




    # Función para actualizar la gráfica y el título
    def actualizar_grafica_ventas(nombre, consulta_funcion, tipo_x):
        def handler(e):
            titulo_grafica_empleados.value = nombre
            nuevos_datos = consulta_funcion()
            nueva_grafica = GraficaLinealPorEmpleado(titulo=nombre, datos=nuevos_datos, tipo_x=tipo_x, tipo_valor="total_ventas")
            container_grafica_empleados.content = nueva_grafica.construir_grafica()
            page.update()

        return handler

    # Botones de selección
    botones_grafica_ventas = ft.Row(
        controls=[
            titulo_grafica_empleados,
            ft.ElevatedButton("Esta semana",
                              on_click=actualizar_grafica_ventas("No.de ventas por empleado esta semana", ventas_empleado_semana_actual, "dia")),
            ft.ElevatedButton("Semana pasada",
                              on_click=actualizar_grafica_ventas("No.de ventas por empleado de la semana pasada", ventas_empleado_semana_pasada,
                                                                 "dia")),
        ],
        spacing=30
    )

    datos_empleados = ventas_empleado_semana()

    # Crear la gráfica
    grafica_pie = GraficaPieVentas(datos_empleados, "Ventas por empleado")
    chart = grafica_pie.crear()

    columm_ventas_empleado = ft.Column(
        controls=[
            botones_grafica_ventas,
            container_grafica_empleados,
            chart
        ],
        scroll=ft.ScrollMode.ALWAYS
    )

    #Crear tabla de empleados
    tabla_container = ft.Container(
        content=ft.Column([
            ft.Text("Lista de Empleados", size=20, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=crear_tabla_empleados(),
                border_radius=20,
                bgcolor="white",
                padding=10,
                shadow=ft.BoxShadow(blur_radius=10, color=ft.Colors.GREY_200),
            ),
        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        margin=ft.margin.symmetric(vertical=20),
    )

    tabs = ft.Tabs(
        selected_index=0,
        tabs=[
            ft.Tab(
                text="Dashboard",
                content=ft.Container(
                    content=ft.Column(
                        controls=[
                            botones_grafica_ventas,
                            container_grafica_empleados,
                            chart
                        ],
                        spacing=20,
                        expand=True
                    ),
                    padding=20
                )
            ),
            ft.Tab(
                text="Registrar Empleado",
                content=ft.Container(
                    content=alta_empleado_view(page),
                    padding=20,
                    expand=True
                )
            ),

            ft.Tab(
                text="Editar Empleado",
                content=ft.Container(
                    content=ft.Column([
                        ft.Text("Lista de Empleados", size=20, weight=ft.FontWeight.BOLD),
                        tabla_container,
                    ])
                )
            )
        ],
        expand=True,
        label_color="#090040",
        unselected_label_color="#03A6A1"
    )

    layout = ft.Row(
        controls=[
            menu_lateral,
            ft.Container(
                ft.Column(
                    controls=[
                        header,
                        tabs

                    ],
                    scroll=ft.ScrollMode.ALWAYS
                ),
                expand=True,
            ),

        ],
        spacing=5,
        expand=True
    )

    return ft.View(
        route="/adminGestionarEmpleados",
        controls=[layout, dlg_usuario],
        bgcolor="#f2f7fb",
        padding=0,
        appbar=None
    )


