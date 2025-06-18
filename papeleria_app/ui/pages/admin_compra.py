import flet as ft
from datetime import datetime

from openpyxl.styles.alignment import horizontal_alignments

from papeleria_app.repositorios.ventas_repo import insertar_venta, obtener_num_venta_actual
from papeleria_app.ui.components.error_text import Error_text
from papeleria_app.repositorios.producto_repo import buscar_coincidencias, aumentar_stock_producto
from papeleria_app.ui.components.header_empleado import header_empleado
from papeleria_app.ui.components.menu_lateral_empleado import menu_lateral_empleado
from papeleria_app.ui.components.menu_lateral_encargado import menu_lateral_encargado


def admin_registrar_compra(page):
    dlg_venta = ft.AlertDialog(
        modal=True,
        title=ft.Text("Detalle de venta"),
        content=ft.Text("Espere un momento..."),
        actions=[ft.TextButton("Cerrar", on_click=lambda e: None)]
    )

    def limpiar(e=None):
        tabla_productos.rows.clear()
        resetear_buscador()
        mensaje_confirmacion.value = ""

    def registrar_compra(e):
        rows = tabla_productos.rows
        if rows:
            for row in rows:
                valores = []
                for cell in row.cells:
                    if isinstance(cell.content, ft.Text):
                        valores.append(cell.content.value)

                    else:
                        valores.append("[No texto]")
                try:
                    producto = buscar_coincidencias(valores[0])
                    print(valores)
                    commit, mensaje = aumentar_stock_producto(producto[0][0], int(valores[1]))

                    mensaje_confirmacion.value = mensaje
                    mensaje_confirmacion.color = "green"
                    page.update()
                except Exception as e:
                    mensaje = f'Ha ocurrido un error inesperado {e}'
                    return None, mensaje
        limpiar()


    buscador_container = ft.Container()  # Contenedor para el dropdown

    def resetear_buscador():
        nuevo_buscador = ft.Dropdown(
            label="Buscar producto",
            width=300,
            enable_filter=True,
            enable_search=True,
            autofocus=True,
            hint_text="Escribe el nombre del producto...",
            hint_style=ft.TextStyle(color="black"),
            editable=True,
            leading_icon=ft.Icons.SEARCH,
            icon_disabled_color="black",
            border_color="#0B1D51",
            label_style=ft.TextStyle(color="#0B1D51"),
            color="black",
            text_style=ft.TextStyle(color="black"),

        )
        productos = buscar_coincidencias("")
        nuevo_buscador.options = [
            ft.dropdown.Option(key=producto[1], text=f"{producto[1]}: {producto[5]}") for producto in productos
        ]
        buscador_container.content = nuevo_buscador
        globals()['buscador'] = nuevo_buscador  # Actualiza referencia global
        page.update()

    def agregar_producto(e):
        productos = buscar_coincidencias(globals()['buscador'].value)
        if productos and cantidad_input.value:
            producto = productos[0]
            cantidad = int(cantidad_input.value)
            costo = producto[4] * cantidad
            if producto[5] > cantidad:

                def eliminar_fila(e, fila_idx=len(tabla_productos.rows)):
                    try:
                        del tabla_productos.rows[fila_idx]
                    except:
                        del tabla_productos.rows[0]
                    page.update()

                boton_eliminar = ft.IconButton(
                    icon=ft.Icons.DELETE,
                    tooltip="Eliminar",
                    icon_color="red",
                    on_click=lambda e, fila_idx=len(tabla_productos.rows): eliminar_fila(e, fila_idx)
                )
                tabla_productos.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(producto[1], color="black")),
                            ft.DataCell(ft.Text(str(cantidad), color="black")),
                            ft.DataCell(ft.Text(str(producto[4]), color="black")),
                            ft.DataCell(ft.Text(str(costo), color="black")),
                            ft.DataCell(ft.Text(str(producto[5]), color="black")),
                            ft.DataCell(boton_eliminar)
                        ]
                    )
                )

                cantidad_input.value = ""
                resetear_buscador()
                mensaje_confirmacion.value = ""

                page.update()

            else:
                mensaje_confirmacion.value = "Stock insuficiente"
                mensaje_confirmacion.color = "red"
                page.update()

        else:
            mensaje_confirmacion.value = "Producto inexistente"
            mensaje_confirmacion.color = "red"
            page.update()

    usuario_data = page.client_storage.get("usuario")
    user = usuario_data["user"]
    user_id = user["id_usuario"]

    # Header y menú lateral
    header = header_empleado(user, page, dlg_venta)
    menu_lateral = menu_lateral_encargado()

    # Texto para la fecha y para el usuario
    fecha_actual = datetime.now().date()
    fecha_text = ft.Text(
        f'Fecha: {str(fecha_actual)}',
        color="white",
        bgcolor="#8285a2",
        weight=ft.FontWeight.BOLD
    )

    user_text = ft.Text(
        f'Admin: {user["nombre"]}',
        color="white",
        bgcolor="#8285a2",
        weight=ft.FontWeight.BOLD
    )

    cantidad_input = ft.TextField(
        label="Cantidad",
        keyboard_type=ft.KeyboardType.NUMBER,
        input_filter=ft.NumbersOnlyInputFilter(),
        text_size=16,
        label_style=ft.TextStyle(
            color="#0B1D51",
            weight=ft.FontWeight.BOLD,
        ),
        border_color="#8e7db4",
        focused_border_color="white",
        width=110,
        height=40,
        border_radius=10,
        border_width=2,
        content_padding=15,
        cursor_color="#231f20",
        selection_color="white",
        animate_size=100,
        bgcolor="white",
        color="black"
    )

    add_button = ft.IconButton(
        icon=ft.Icons.ADD,
        icon_size=20,
        icon_color="white",
        bgcolor="#0B1D51",
        width=40,
        height=40,
        style=ft.ButtonStyle(
            padding=ft.padding.all(0)
        ),
        on_click=agregar_producto
    )

    tabla_productos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto", color="white")),
            ft.DataColumn(ft.Text("Cantidad", color="white")),
            ft.DataColumn(ft.Text("Costo Unitario", color="white")),
            ft.DataColumn(ft.Text("Costo", color="white")),
            ft.DataColumn(ft.Text("Stock Actual", color="white")),
            ft.DataColumn(ft.Text("Eliminar", color="white"))
        ],
        rows=[],
        heading_row_color="#8e7db4",
    )

    tabla_container = ft.Container(
        content=ft.Column(
            controls=[tabla_productos],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True
        ),
        expand=True,
        height=500
    )

    container_venta = ft.Container(
        content=ft.Row(
            controls=[
                ft.ElevatedButton("REGISTRAR COMPRA", on_click=registrar_compra),
                ft.ElevatedButton("LIMPIAR", on_click=limpiar)
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
            spacing=50
        ),
    )
    mensaje_confirmacion = ft.Text("", color="green", size=16, weight=ft.FontWeight.BOLD)

    # Layout principal
    contenido_principal = ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(content=fecha_text, padding=10, bgcolor="#8285a2"),
                        ft.Container(content=user_text, padding=10, bgcolor="#8285a2")
                    ],
                ),
                ft.Divider(),
                ft.Row(
                    controls=[
                        buscador_container,
                        cantidad_input,
                        add_button,
                        mensaje_confirmacion
                    ],
                    spacing=50
                ),
                ft.Divider(),
                ft.Row(
                    controls=[
                        tabla_container,
                        container_venta
                    ],
                    expand= True,
                    spacing=50,
                    vertical_alignment=ft.CrossAxisAlignment.START

                ),

            ]
        ),
        bgcolor="#d7daf1",
        expand=True,
        padding=20
    )



    layout = ft.Row(
        controls=[
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

    # Inicializar buscador
    resetear_buscador()

    return ft.View(
        route="/admin_registrar_compra",
        controls=[layout, dlg_venta],
        bgcolor="#cdf3ff",
        padding=0,
        appbar=None,
    )




