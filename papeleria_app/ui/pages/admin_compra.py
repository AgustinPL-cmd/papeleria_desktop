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
        cantidad_input.value = ""
        page.update()

    def registrar_compra(e):
        rows = tabla_productos.rows
        if not rows:
            mensaje_confirmacion.value = "No hay productos para registrar"
            mensaje_confirmacion.color = "red"
            page.update()
            return

        # Recorrer filas y aumentar stock de cada producto
        for row in rows:
            # Obtener id_producto desde el metadato de la fila
            id_producto = row.data.get("id_producto") if hasattr(row, "data") else None
            if not id_producto:
                # Alternativa: extraer nombre de la primera celda y buscar producto
                nombre_celda = row.cells[0].content.value
                productos = buscar_coincidencias(nombre_celda)
                if productos:
                    id_producto = productos[0][0]
                else:
                    mensaje_confirmacion.value = f"Producto {nombre_celda} no encontrado"
                    mensaje_confirmacion.color = "red"
                    page.update()
                    return

            cantidad_text = row.cells[1].content.value
            try:
                cantidad = int(cantidad_text)
            except ValueError:
                mensaje_confirmacion.value = f"Cantidad inválida para {nombre_celda}"
                mensaje_confirmacion.color = "red"
                page.update()
                return

            exito, mensaje = aumentar_stock_producto(id_producto, cantidad)
            if not exito:
                mensaje_confirmacion.value = mensaje
                mensaje_confirmacion.color = "red"
                page.update()
                return

        # Si todo ok
        mensaje_confirmacion.value = "Compra registrada correctamente"
        mensaje_confirmacion.color = "green"
        limpiar()  # Vacía la tabla y el buscador
        page.update()

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
            border_color="#0B1D51",
            label_style=ft.TextStyle(color="#0B1D51"),
            color="black",
            text_style=ft.TextStyle(color="black"),
        )
        productos = buscar_coincidencias("")  # Todos los productos activos
        # Crear opciones con key = id_producto, text = nombre + stock
        nuevo_buscador.options = [
            ft.dropdown.Option(key=str(p[0]), text=f"{p[1]} (Stock: {p[5]})")
            for p in productos if p[8] == 1  # asumiendo que índice 8 es 'activo'
        ]
        buscador_container.content = nuevo_buscador
        globals()['buscador'] = nuevo_buscador
        page.update()

    def agregar_producto(e):
        # El valor del dropdown ahora es el ID (string)
        producto_id_str = globals()['buscador'].value
        if not producto_id_str:
            mensaje_confirmacion.value = "Selecciona un producto"
            mensaje_confirmacion.color = "red"
            page.update()
            return

        try:
            producto_id = int(producto_id_str)
        except ValueError:
            mensaje_confirmacion.value = "ID de producto inválido"
            mensaje_confirmacion.color = "red"
            page.update()
            return

        # Obtener producto por ID (usando la función que ya tienes)
        from papeleria_app.repositorios.producto_repo import get_producto_by_id
        producto = get_producto_by_id(producto_id)
        if not producto:
            mensaje_confirmacion.value = "Producto no encontrado"
            mensaje_confirmacion.color = "red"
            page.update()
            return

        # Validar cantidad
        try:
            cantidad = int(cantidad_input.value.strip())
            if cantidad <= 0:
                mensaje_confirmacion.value = "La cantidad debe ser mayor a 0"
                mensaje_confirmacion.color = "red"
                page.update()
                return
        except ValueError:
            mensaje_confirmacion.value = "Cantidad inválida"
            mensaje_confirmacion.color = "red"
            page.update()
            return

        costo_total = producto['precio_unitario_compra'] * cantidad

        # Crear fila en la tabla (guardando el ID en un atributo de la fila)
        boton_eliminar = ft.IconButton(
            icon=ft.Icons.DELETE,
            tooltip="Eliminar",
            icon_color="red",
            on_click=lambda e, idx=len(tabla_productos.rows): eliminar_fila(e, idx)
        )

        nueva_fila = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(producto['nombre_producto'], color="black")),
                ft.DataCell(ft.Text(str(cantidad), color="black")),
                ft.DataCell(ft.Text(f"{producto['precio_unitario_compra']:.2f}", color="black")),
                ft.DataCell(ft.Text(f"{costo_total:.2f}", color="black")),
                ft.DataCell(ft.Text(str(producto['stock_actual']), color="black")),
                ft.DataCell(boton_eliminar)
            ],
            data={"id_producto": producto['id_producto']}  # Guardar ID aquí
        )
        tabla_productos.rows.append(nueva_fila)

        # Limpiar
        cantidad_input.value = ""
        resetear_buscador()
        mensaje_confirmacion.value = "Producto agregado"
        mensaje_confirmacion.color = "green"
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




