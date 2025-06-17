import flet as ft
from datetime import datetime, timedelta
from papeleria_app.repositorios.ventas_repo import consultar_ventas_por_fecha_empleado, obtener_ventas_por_dia_empleado, \
    obtener_venta_by_numVenta
from papeleria_app.ui.components.alert_venta_detalles import alert_venta_detalles
from papeleria_app.ui.components.header_empleado import header_empleado
from papeleria_app.ui.components.menu_lateral_empleado import menu_lateral_empleado


# Función para formatear fecha
def formatear_fecha_relativa(fecha_venta: datetime) -> str:
    hoy = datetime.now().date()
    fecha_solo_dia = fecha_venta.date()

    if fecha_solo_dia == hoy:
        return "Hoy"
    elif fecha_solo_dia == hoy - timedelta(days=1):
        return "Ayer"
    else:
        return fecha_venta.strftime("%d-%b-%Y")

# Función que regresa la vista del empleado
def empleado_dashboard_view(page):
    #Alert View
    dlg_venta = ft.AlertDialog(
        modal=True,
        title=ft.Text(""),  #
        content=ft.Text(""),
        actions=[]
    )

    page.dialog = dlg_venta  # Asignarlo desde el inicio

    def mostrar_dialogo(venta, e=None):
        dlg_detalle = alert_venta_detalles(page, venta)
        dlg_venta.title = dlg_detalle.title
        dlg_venta.content = dlg_detalle.content
        dlg_venta.bgcolor = dlg_detalle.bgcolor

        dlg_venta.actions = [
            ft.TextButton("Cerrar", on_click=lambda e: cerrar_dialogo())
        ]

        dlg_venta.open = True
        page.update()

    def cerrar_dialogo():
        dlg_venta.open = False
        page.update()

    usuario_data = page.client_storage.get("usuario") # Obtener el usuario loggeado
    user = usuario_data["user"] # Obtener el diccionario del usuario
    id_user = user["id_usuario"] # Obtener su Id

    # Obtener las ventas por día
    ventas_por_dia = obtener_ventas_por_dia_empleado(id_user)

    dias = list(ventas_por_dia.keys()) #Días
    cantidades = list(ventas_por_dia.values()) # Las cantidades vendidas por día

    bar_groups = [] # Cantidades
    bottom_labels = [] # Días

    # Por cantidad por día en ventas por dia agregar el día y la cantidad al eje x
    for i, (dia, cantidad) in enumerate(ventas_por_dia.items()):
        bar_groups.append(
            ft.BarChartGroup(
                x=i,
                bar_rods=[
                    ft.BarChartRod(
                        from_y=0,
                        to_y=cantidad,
                        width=40,
                        color=ft.Colors.BLUE,
                        border_radius=0,
                    ),
                ],
            )
        )
        bottom_labels.append(
            ft.ChartAxisLabel(
                value=i,
                label=ft.Container(ft.Text(dia, color="black"), padding=10)
            )
        )

    #Gráfica de ventas por día
    chart = ft.BarChart(
        bar_groups=bar_groups,
        border=ft.border.all(1, "#8e7db4"),
        left_axis=ft.ChartAxis(
            labels_size=40,
            title=ft.Text("Cantidad vendida", color="#61375d", weight=ft.FontWeight.BOLD),
            title_size=40,
            labels=[
                ft.ChartAxisLabel(
                    value=float(value),  # Convertimos a float primero
                    label=ft.Text(str(int(value)), color="black")  # Mostramos como entero
                )
                for value in range(0, int(max(cantidades)) + 10, 10)  # La mayor cantidad + 10 en el eje y, yendo de 10 en 10
            ]

        ),
        bottom_axis=ft.ChartAxis(
            labels=bottom_labels,
            title=ft.Text("Días", color="#61375d", weight=ft.FontWeight.BOLD),
            labels_size=40,

        ),
        horizontal_grid_lines=ft.ChartGridLines(
            color="#ffdefd", width=1, dash_pattern=[3, 3]
        ),
        tooltip_bgcolor=ft.Colors.with_opacity(0.5, ft.Colors.GREY_300),
        max_y=max(cantidades) + 10,  # Un poco más alto que el máximo
        interactive=True,
        expand=True,

    )

    #Función para filtrar ventas por fecha y mostrarlo en la tabla
    def filtar_by_fecha(e=None, fecha_valor=None):
        fecha = fecha_valor if fecha_valor else e.control.value
        ventas = consultar_ventas_por_fecha_empleado(fecha, id_user)
        tabla_ventas.rows.clear()

        for v in ventas:
            fecha_venta, num_venta, total = v

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
                        ft.DataCell(crear_boton(v))  # Usar la función auxiliar
                    ]
                )
            )

        if e is not None:
            tabla_ventas.update()






    # Header
    header = header_empleado(user)

    #Menu Lateral
    menu_lateral = menu_lateral_empleado()

    mensaje_ventas = ft.Text(
        value=f"Tus ventas",
        size=18,
        color="#231f20"
    )

    #dropdown fecha:
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
        on_change= filtar_by_fecha,


    )

    #Tabla ventas
    tabla_ventas = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Fecha", color="white")),
            ft.DataColumn(ft.Text("Número de Venta", color="white")),
            ft.DataColumn(ft.Text("Total", color="white")),
            ft.DataColumn(ft.Text("Detalles", color="white"))
        ],
        rows=[],
        heading_row_color="#8e7db4",

    )

    # Contenedor para la tabla con scroll
    tabla_container = ft.Container(
        content=ft.Column(
            controls=[tabla_ventas],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True
        ),
        expand=True,
        height=500
    )

    mensaje_grafica = ft.Text(
        value=f"TUS VENTAS DE LA SEMANA",
        weight=ft.FontWeight.BOLD,
        size=18,
        color="#231f20"
    )

    #Contenedor de la tabla con su título
    grafica_con_titulo = ft.Column(
        controls=[
            ft.Container(
                content=mensaje_grafica,
                alignment=ft.alignment.center,
                padding=ft.padding.only(bottom=10)
            ),
            ft.Container(
                content=chart,
                height=400,  # Altura fija para la gráfica
                width=600,  # Ancho fijo para la gráfica
                border=ft.border.all(1, "#8e7db4"),
                border_radius=10,
                padding=10
            )
        ],
        spacing=0,
        expand=True
    )

    # Contenido principal
    contenido_principal = ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            mensaje_ventas,
                            filtro_fecha_dropdown,
                        ],
                        spacing=10,
                    ),
                    padding=ft.padding.only(bottom=10),
                ),
                ft.Row(
                    controls=[
                        tabla_container,
                        grafica_con_titulo

                    ],
                    expand=True,
                    spacing=20,
                )
            ],
            expand=True,
        ),
        bgcolor="#cdf3ff",
        expand=True,
        padding=20,
    )


    layout = ft.Row(
        controls= [
            menu_lateral,
            ft.Column(
                controls=[
                    header,
                    contenido_principal

                ],
                expand=True
            )
        ],
        expand=True,
        spacing=5
    )

    filtar_by_fecha(fecha_valor="hoy")

    return ft.View(
        route="/empleadoDashboard",
        controls=[layout, dlg_venta],
        bgcolor="#cdf3ff",
        padding=0,
        appbar=None,


    )



